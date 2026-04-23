from sqlalchemy import or_
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.models import BorrowRecord, User
from app.utils.decorators import admin_required, current_user
from app.utils.response import fail, ok, page_result
from extensions import db

users_bp = Blueprint("users", __name__)


@users_bp.get("")
@admin_required
def list_users():
    page = int(request.args.get("page", 1))
    page_size = min(int(request.args.get("page_size", 10)), 100)
    keyword = (request.args.get("keyword") or "").strip()
    role = request.args.get("role")
    status = request.args.get("status")
    query = User.query
    if keyword:
        like = f"%{keyword}%"
        query = query.filter(or_(User.username.like(like), User.real_name.like(like), User.email.like(like)))
    if role:
        query = query.filter(User.role == role)
    if status:
        query = query.filter(User.status == status)
    pagination = query.order_by(User.created_at.desc()).paginate(page=page, per_page=page_size, error_out=False)
    return ok(page_result(pagination, [item.to_dict() for item in pagination.items]))


@users_bp.post("")
@admin_required
def create_user():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or "123456"
    if not username or not data.get("real_name"):
        return fail("username and real name are required")
    if User.query.filter_by(username=username).first():
        return fail("username already exists", 4001, 400)
    user = User(
        username=username,
        real_name=data["real_name"].strip(),
        role=data.get("role") or "reader",
        phone=(data.get("phone") or "").strip(),
        email=(data.get("email") or "").strip(),
        status=data.get("status") or "active",
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return ok(user.to_dict())


@users_bp.put("/<int:user_id>")
@jwt_required()
def update_user(user_id):
    actor = current_user()
    if not actor:
        return fail("user not found", 404, 404)
    user = User.query.get_or_404(user_id)
    data = request.get_json() or {}
    if actor.role != "admin" and actor.id != user.id:
        return fail("forbidden", 403, 403)
    user.real_name = (data.get("real_name") or user.real_name).strip()
    user.phone = (data.get("phone") or "").strip()
    user.email = (data.get("email") or "").strip()
    if actor.role == "admin":
        user.role = data.get("role") or user.role
        user.status = data.get("status") or user.status
    db.session.commit()
    return ok(user.to_dict())


@users_bp.delete("/<int:user_id>")
@admin_required
def delete_user(user_id):
    actor = current_user()
    user = User.query.get_or_404(user_id)
    if actor and actor.id == user.id:
        return fail("cannot delete current user", 4002, 400)
    if BorrowRecord.query.filter_by(user_id=user.id).first():
        user.status = "disabled"
        db.session.commit()
        return ok(user.to_dict(), "user has borrow records and was disabled")
    db.session.delete(user)
    db.session.commit()
    return ok()


@users_bp.put("/<int:user_id>/reset-password")
@admin_required
def reset_password(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json() or {}
    password = data.get("password") or "123456"
    if len(password) < 6:
        return fail("password must be at least 6 characters")
    user.set_password(password)
    db.session.commit()
    return ok()

