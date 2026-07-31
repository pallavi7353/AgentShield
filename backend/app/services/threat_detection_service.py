"""
threat_detection_service.py
-----------------------------
Lightweight, explainable rule-based detector for three attack classes
relevant to CYBR-03:

1. Prompt Injection - attempts to override the agent's instructions
   ("ignore previous instructions", "you are now DAN", etc.)
2. Data Exfiltration Attempt - prompts that ask the agent to reveal,
   dump, or output sensitive data (passwords, API keys, secrets)
   even though no actual secret value is present in the prompt yet.
3. Sensitive Data Leakage - prompts/responses that already contain
   patterns resembling secrets (API keys, passwords, card numbers,
   SSNs, private keys).

This is intentionally rule-based (not a black box) so it's easy to
explain to judges and easy for Member 2 (AI module) to plug into --
the AI/LLM call in the pipeline can call `analyze_prompt()` BEFORE
sending a prompt to the model, and `analyze_response()` AFTER, to
block leakage in either direction.

For a hackathon-grade demo this keyword/regex approach is a
legitimate, deliberately simple baseline. It can be swapped later for
an ML classifier without changing the API contract.
"""

import re
from dataclasses import dataclass
from typing import Optional

# Patterns commonly seen in prompt-injection attempts
INJECTION_PATTERNS = [
    r"ignore (all|any|your|previous|prior) instructions",
    r"disregard (all|any|your|previous|prior) (instructions|rules)",
    r"you are now",
    r"act as (an? )?(unrestricted|jailbroken|dan)",
    r"reveal (your|the) (system prompt|instructions|hidden prompt)",
    r"bypass (your|the) (rules|restrictions|filters)",
    r"pretend (you|to) (have no|ignore) (restrictions|rules)",
    r"override (your|system) (settings|instructions)",
]

# Patterns where a prompt is *asking* the agent to output/reveal
# sensitive data, even though no actual secret value is present yet.
# This is distinct from SENSITIVE_DATA_PATTERNS below, which catches
# an actual secret *appearing* in text (e.g. in a leaked response).
DATA_REQUEST_PATTERNS = [
    r"(output|reveal|show|give|send|list|dump|display|print) (all |every |the )?"
    r"(user |users'? )?(password|api[_-]?key|secret|credential|token|private key)",
]

# Patterns commonly indicating sensitive data (secrets/PII) in text
SENSITIVE_DATA_PATTERNS = [
    (r"api[_-]?key\s*[:=]\s*\S+", "API_KEY"),
    (r"password\s*[:=]\s*\S+", "PASSWORD"),
    (r"\b\d{3}-\d{2}-\d{4}\b", "SSN"),
    (r"\b(?:\d[ -]*?){13,16}\b", "CARD_NUMBER"),
    (r"-----BEGIN (RSA|OPENSSH|PRIVATE) KEY-----", "PRIVATE_KEY"),
    (r"\bAKIA[0-9A-Z]{16}\b", "AWS_ACCESS_KEY"),
]


@dataclass
class ThreatAssessment:
    attack_type: str          # "PROMPT_INJECTION" | "DATA_EXFILTRATION_ATTEMPT" | "DATA_LEAKAGE" | "NONE"
    risk_score: int           # 0-100
    blocked: bool
    matched_pattern: Optional[str] = None


def _scan_injection(text: str) -> Optional[str]:
    lowered = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, lowered):
            return pattern
    return None


def _scan_data_request(text: str) -> Optional[str]:
    lowered = text.lower()
    for pattern in DATA_REQUEST_PATTERNS:
        if re.search(pattern, lowered):
            return pattern
    return None


def _scan_sensitive_data(text: str) -> Optional[str]:
    for pattern, label in SENSITIVE_DATA_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return label
    return None


def analyze_prompt(prompt: str, high_risk_threshold: int = 70) -> ThreatAssessment:
    """
    Analyze an inbound prompt (user/agent -> AI model) for
    prompt-injection attempts, requests for sensitive data, and
    sensitive data being *submitted*.
    """
    injection_match = _scan_injection(prompt)
    if injection_match:
        return ThreatAssessment(
            attack_type="PROMPT_INJECTION",
            risk_score=90,
            blocked=90 >= high_risk_threshold,
            matched_pattern=injection_match,
        )

    data_request_match = _scan_data_request(prompt)
    if data_request_match:
        return ThreatAssessment(
            attack_type="DATA_EXFILTRATION_ATTEMPT",
            risk_score=85,
            blocked=85 >= high_risk_threshold,
            matched_pattern=data_request_match,
        )

    leak_match = _scan_sensitive_data(prompt)
    if leak_match:
        return ThreatAssessment(
            attack_type="DATA_LEAKAGE",
            risk_score=80,
            blocked=80 >= high_risk_threshold,
            matched_pattern=leak_match,
        )

    return ThreatAssessment(attack_type="NONE", risk_score=0, blocked=False)


def analyze_response(response_text: str, high_risk_threshold: int = 70) -> ThreatAssessment:
    """
    Analyze an outbound AI response for sensitive data that is about
    to be exposed to the user -- this is the "before confidential
    data is exposed" check called for in the problem statement.
    """
    leak_match = _scan_sensitive_data(response_text)
    if leak_match:
        return ThreatAssessment(
            attack_type="DATA_LEAKAGE",
            risk_score=95,
            blocked=95 >= high_risk_threshold,
            matched_pattern=leak_match,
        )
    return ThreatAssessment(attack_type="NONE", risk_score=0, blocked=False)