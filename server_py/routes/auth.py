import logging

from flask import Blueprint, g, jsonify, request

from errors import ApiError
from services.auth_service import authenticate, create_token, login_required, register_user

bp = Blueprint("auth", __name__)
log = logging.getLogger("resume.auth")


def _body() -> dict:
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ApiError(400, "Send a JSON body.")
    return data


def _field(data: dict, key: str) -> str:
    value = data.get(key)
    return value if isinstance(value, str) else ""


@bp.post("/signup")
def signup():
    data = _body()
    email, password = _field(data, "email"), _field(data, "password")
    if not email or not password:
        raise ApiError(400, "Email and password are required.")
    user = register_user(email, password, _field(data, "name"))
    log.info("[%s] SIGNUP new user id=%s email=%s stored in DB", g.req_id, user.id, user.email)
    return jsonify({"token": create_token(user), "user": user.to_dict()}), 201


@bp.post("/login")
def login():
    data = _body()
    email, password = _field(data, "email"), _field(data, "password")
    if not email or not password:
        raise ApiError(400, "Email and password are required.")
    try:
        user = authenticate(email, password)
    except ApiError:
        log.warning("[%s] LOGIN failed for email=%s", g.req_id, email.strip().lower())
        raise
    log.info("[%s] LOGIN ok user id=%s email=%s (last_login_at updated in DB)", g.req_id, user.id, user.email)
    return jsonify({"token": create_token(user), "user": user.to_dict()})


@bp.get("/me")
@login_required
def me():
    return jsonify({"user": g.user.to_dict()})
