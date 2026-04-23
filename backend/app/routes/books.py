from sqlalchemy import or_
from flask import Blueprint, request
from flask_jwt_extended import get_jwt, jwt_required

from app.models import Book, BorrowRecord
from app.utils.decorators import admin_required
from app.utils.response import fail, ok, page_result
from extensions import db

books_bp = Blueprint("books", __name__)


def book_payload(data, book=None):
    target = book or Book()
    required = ["isbn", "title_zh", "title_en", "author"]
    for field in required:
        if not (data.get(field) or "").strip():
            raise ValueError(f"{field} is required")
    target.isbn = data["isbn"].strip()
    target.title_zh = data["title_zh"].strip()
    target.title_en = data["title_en"].strip()
    target.author = data["author"].strip()
    target.publisher = (data.get("publisher") or "").strip()
    target.publish_date = (data.get("publish_date") or "").strip()
    target.category_id = data.get("category_id") or None
    target.cover_image = (data.get("cover_image") or "").strip()
    target.description_zh = data.get("description_zh") or ""
    target.description_en = data.get("description_en") or ""
    target.total_stock = max(0, int(data.get("total_stock") or 0))
    target.available_stock = max(0, int(data.get("available_stock") if data.get("available_stock") is not None else target.total_stock))
    target.available_stock = min(target.available_stock, target.total_stock)
    target.location = (data.get("location") or "").strip()
    target.status = data.get("status") or "available"
    return target


@books_bp.get("")
@jwt_required()
def list_books():
    claims = get_jwt()
    page = int(request.args.get("page", 1))
    page_size = min(int(request.args.get("page_size", 10)), 100)
    keyword = (request.args.get("keyword") or "").strip()
    category_id = request.args.get("category_id")
    status = request.args.get("status")

    query = Book.query
    if claims.get("role") != "admin":
        query = query.filter(Book.status == "available")
    elif status:
        query = query.filter(Book.status == status)
    if keyword:
        like = f"%{keyword}%"
        query = query.filter(or_(Book.isbn.like(like), Book.title_zh.like(like), Book.title_en.like(like), Book.author.like(like)))
    if category_id:
        query = query.filter(Book.category_id == int(category_id))

    pagination = query.order_by(Book.created_at.desc()).paginate(page=page, per_page=page_size, error_out=False)
    return ok(page_result(pagination, [item.to_dict(False) for item in pagination.items]))


@books_bp.get("/<int:book_id>")
@jwt_required()
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return ok(book.to_dict(True))


@books_bp.post("")
@admin_required
def create_book():
    data = request.get_json() or {}
    if Book.query.filter_by(isbn=(data.get("isbn") or "").strip()).first():
        return fail("isbn already exists", 3001, 400)
    try:
        book = book_payload(data)
    except ValueError as exc:
        return fail(str(exc))
    db.session.add(book)
    db.session.commit()
    return ok(book.to_dict(True))


@books_bp.put("/<int:book_id>")
@admin_required
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json() or {}
    exists = Book.query.filter(Book.isbn == (data.get("isbn") or "").strip(), Book.id != book.id).first()
    if exists:
        return fail("isbn already exists", 3001, 400)
    try:
        book_payload(data, book)
    except ValueError as exc:
        return fail(str(exc))
    db.session.commit()
    return ok(book.to_dict(True))


@books_bp.delete("/<int:book_id>")
@admin_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if BorrowRecord.query.filter_by(book_id=book.id).first():
        book.status = "disabled"
        db.session.commit()
        return ok(book.to_dict(False), "book has borrow records and was disabled")
    db.session.delete(book)
    db.session.commit()
    return ok()

