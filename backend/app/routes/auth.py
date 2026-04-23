from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required

from app.models import User
from app.utils.decorators import current_user
from app.utils.response import fail, ok
from extensions import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return fail("invalid username or password", 1001, 401)
    if user.status != "active":
        return fail("user disabled", 1002, 403)
    token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
    return ok({"token": token, "user": user.to_dict()})


@auth_bp.get("/me")
@jwt_required()
def me():
    user = current_user()
    if not user:
        return fail("user not found", 1003, 404)
    return ok(user.to_dict())


@auth_bp.put("/profile")
@jwt_required()
def update_profile():
    user = current_user()
    if not user:
        return fail("user not found", 1003, 404)
    data = request.get_json() or {}
    user.real_name = (data.get("real_name") or user.real_name).strip()
    user.phone = (data.get("phone") or "").strip()
    user.email = (data.get("email") or "").strip()
    db.session.commit()
    return ok(user.to_dict())


@auth_bp.put("/change-password")
@jwt_required()
def change_password():
    user = current_user()
    data = request.get_json() or {}
    old_password = data.get("old_password") or ""
    new_password = data.get("new_password") or ""
    if not user or not user.check_password(old_password):
        return fail("old password is incorrect", 1004, 400)
    if len(new_password) < 6:
        return fail("password must be at least 6 characters", 1005, 400)
    user.set_password(new_password)
    db.session.commit()
    return ok()

