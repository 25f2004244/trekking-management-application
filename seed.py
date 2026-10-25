from model import db, user as user_model

SAMPLE_ACCOUNTS = [
    {"username": "Admin", "email": "admin@trek", "password": "admin", "role": "admin", "is_approved": True},

    {"username": "Staff_1", "email": "s1@trek", "password": "s1", "role": "staff", "is_approved": True},
    {"username": "Staff_2", "email": "s2@trek", "password": "s2", "role": "staff", "is_approved": True},
    {"username": "Staff_3", "email": "s3@trek", "password": "s3", "role": "staff", "is_approved": True},

    {"username": "Staff_requested_1", "email": "sr1@trek", "password": "sr1", "role": "staff", "is_approved": False},
    {"username": "Staff_requested_2", "email": "sr2@trek", "password": "sr2", "role": "staff", "is_approved": False},

    {"username": "Staff_blocked_1", "email": "sb1@trek", "password": "sb1", "role": "staff", "is_approved": True, "is_active": False},
    {"username": "Staff_blocked_2", "email": "sb2@trek", "password": "sb2", "role": "staff", "is_approved": True, "is_active": False},

    {"username": "User_1", "email": "u1@trek", "password": "u1", "role": "user", "is_approved": True},
    {"username": "User_2", "email": "u2@trek", "password": "u2", "role": "user", "is_approved": True},
    {"username": "User_3", "email": "u3@trek", "password": "u3", "role": "user", "is_approved": True},

    {"username": "User_blocked_1", "email": "ub1@trek", "password": "ub1", "role": "user", "is_approved": True, "is_active": False},
    {"username": "User_blocked_2", "email": "ub2@trek", "password": "ub2", "role": "user", "is_approved": True, "is_active": False},
]


def seed_database():
    for acc in SAMPLE_ACCOUNTS:
        if user_model.query.filter_by(email=acc["email"]).first():
            continue  # already exists, leave it untouched

        db.session.add(user_model(
            username=acc["username"],
            email=acc["email"],
            password=acc["password"],
            role=acc["role"],
            is_approved=acc.get("is_approved", False),
            is_active=acc.get("is_active", True),
        ))
        print(f"Created: {acc['username']} ({acc['role']})")

    db.session.commit()