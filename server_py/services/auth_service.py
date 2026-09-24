import os
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import g, request

from database import User, db
from errors import ApiError

JWT_ALGORITHM = "HS256"
JWT_EXPIRES_HOURS = int(os.getenv("JWT_EXPIRES_HOURS", "24"))
MIN_PASSWORD_LEN = 8


def _secret() -> str:
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise ApiError(500, "JWT_SECRET is not configured on the server.")
    return secret


def create_token(user: User) -> str:
    now = datetime.now(timezone.utc)
    payload = {"sub": str(user.id), "iat": now, "exp": now + timedelta(hours=JWT_EXPIRES_HOURS)}
    return jwt.encode(payload, _secret(), algorithm=JWT_ALGORITHM)


def register_user(email: str, password: str, name: str) -> User:
    email = email.strip().lower()
    if "@" not in email or "." not in email.split("@")[-1]:
        raise ApiError(400, "Enter a valid email address.")
    if len(password) < MIN_PASSWORD_LEN:
        raise ApiError(400, f"Password must be at least {MIN_PASSWORD_LEN} characters.")
    if User.query.filter_by(email=email).first():
        raise ApiError(409, "Account already exists.")

    user = User(email=email, name=name.strip() or email.split("@")[0])
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def authenticate(email: str, password: str) -> User:
    user = User.query.filter_by(email=email.strip().lower()).first()
    # Same message for unknown email and wrong password so accounts can't be enumerated.
    if user is None or not user.check_password(password):
        raise ApiError(401, "Invalid credentials.")
    user.last_login_at = datetime.now(timezone.utc)
    db.session.commit()
    return user


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            raise ApiError(401, "Authentication required. Please log in.")
        try:
            payload = jwt.decode(header[7:], _secret(), algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise ApiError(401, "Session expired. Please log in again.")
        except jwt.InvalidTokenError:
            raise ApiError(401, "Invalid session token.")

        user = db.session.get(User, int(payload["sub"]))
        if user is None:
            raise ApiError(401, "Account no longer exists.")
        g.user = user
        return fn(*args, **kwargs)

    return wrapper
