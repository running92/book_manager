from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.models import Book, Category
from app.utils.decorators import admin_required
from app.utils.response import fail, ok
from extensions import db

categories_bp = Blueprint("categories", __name__)


@categories_bp.get("")
@jwt_required()
def list_categories():
    categories = Category.query.order_by(Category.sort_order.asc(), Category.id.asc()).all()
    return ok([item.to_dict() for item in categories])


@categories_bp.post("")
@admin_required
def create_category():
    data = request.get_json() or {}
    if not data.get("name_zh") or not data.get("name_en"):
        return fail("category name is required")
    category = Category(
        name_zh=data["name_zh"].strip(),
        name_en=data["name_en"].strip(),
        description=(data.get("description") or "").strip(),
        sort_order=int(data.get("sort_order") or 0),
    )
    db.session.add(category)
    db.session.commit()
    return ok(category.to_dict())


@categories_bp.put("/<int:category_id>")
@admin_required
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    data = request.get_json() or {}
    category.name_zh = (data.get("name_zh") or category.name_zh).strip()
    category.name_en = (data.get("name_en") or category.name_en).strip()
    category.description = (data.get("description") or "").strip()
    category.sort_order = int(data.get("sort_order") or 0)
    db.session.commit()
    return ok(category.to_dict())


@categories_bp.delete("/<int:category_id>")
@admin_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if Book.query.filter_by(category_id=category.id).first():
        return fail("category has books and cannot be deleted", 2001, 400)
    db.session.delete(category)
    db.session.commit()
    return ok()

