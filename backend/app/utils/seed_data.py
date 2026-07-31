"""
seed_data.py
--------------
Populates the database with the four roles, five permissions, the
least-privilege RBAC map between them, and one demo user per role
so judges can log in and see RBAC in action immediately.

Run with:  python seed.py
"""

from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.models.user import User
from app.models.ai_agent import AIAgent
from app.auth.hashing import hash_password

ROLES = ["Admin", "Security Analyst", "Employee", "AI Agent"]

PERMISSIONS = [
    "READ_LOGS",
    "VIEW_DASHBOARD",
    "MANAGE_USERS",
    "EXECUTE_AI_AGENT",
    "EXPORT_REPORTS",
]

# Least-privilege mapping: each role gets ONLY what it needs
ROLE_PERMISSION_MAP = {
    "Admin": ["READ_LOGS", "VIEW_DASHBOARD", "MANAGE_USERS", "EXECUTE_AI_AGENT", "EXPORT_REPORTS"],
    "Security Analyst": ["READ_LOGS", "VIEW_DASHBOARD", "EXPORT_REPORTS"],
    "Employee": ["VIEW_DASHBOARD"],
    "AI Agent": ["EXECUTE_AI_AGENT"],
}

# username -> (email, password, role_name)
# Note: use a normal-looking domain, not .local/.test/.invalid -- pydantic's
# EmailStr validator rejects reserved/special-use TLDs.
DEMO_USERS = {
    "admin": ("admin@aisecplatform.com", "Admin@12345", "Admin"),
    "analyst": ("analyst@aisecplatform.com", "Analyst@12345", "Security Analyst"),
    "employee": ("employee@aisecplatform.com", "Employee@12345", "Employee"),
    "agent_service": ("agent@aisecplatform.com", "Agent@12345", "AI Agent"),
}


def seed(db: Session) -> None:
    # --- Roles ---
    role_objs = {}
    for name in ROLES:
        role = db.query(Role).filter(Role.role_name == name).first()
        if not role:
            role = Role(role_name=name)
            db.add(role)
            db.commit()
            db.refresh(role)
        role_objs[name] = role

    # --- Permissions ---
    permission_objs = {}
    for name in PERMISSIONS:
        perm = db.query(Permission).filter(Permission.permission_name == name).first()
        if not perm:
            perm = Permission(permission_name=name)
            db.add(perm)
            db.commit()
            db.refresh(perm)
        permission_objs[name] = perm

    # --- RolePermission mapping ---
    for role_name, perm_names in ROLE_PERMISSION_MAP.items():
        role = role_objs[role_name]
        for perm_name in perm_names:
            perm = permission_objs[perm_name]
            exists = (
                db.query(RolePermission)
                .filter(RolePermission.role_id == role.id, RolePermission.permission_id == perm.id)
                .first()
            )
            if not exists:
                db.add(RolePermission(role_id=role.id, permission_id=perm.id))
    db.commit()

    # --- Demo users ---
    for username, (email, password, role_name) in DEMO_USERS.items():
        existing = db.query(User).filter(User.username == username).first()
        if not existing:
            db.add(
                User(
                    username=username,
                    email=email,
                    hashed_password=hash_password(password),
                    role_id=role_objs[role_name].id,
                )
            )
    db.commit()

    # --- Sample AI agent ---
    if not db.query(AIAgent).filter(AIAgent.agent_name == "SkillBridge-Assistant").first():
        db.add(AIAgent(agent_name="SkillBridge-Assistant", status="active"))
        db.commit()

    print("Seed data inserted successfully.")
    print("Demo logins (username / password):")
    for username, (_, password, role_name) in DEMO_USERS.items():
        print(f"  {username} / {password}  -> role: {role_name}")
