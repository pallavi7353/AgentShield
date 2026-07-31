"""
security_middleware.py
------------------------
Cross-cutting security concerns applied to every request:
- Adds standard security response headers
- Logs unhandled exceptions instead of leaking stack traces to clients
- Tags each response with a processing-time header (useful for
  spotting abnormal latency, e.g. an agent stuck in a loop)
"""

import time
import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger("security_middleware")


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        try:
            response = await call_next(request)
        except Exception as exc:  # noqa: BLE001
            logger.exception("Unhandled exception processing request: %s", exc)
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error."},
            )

        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response
