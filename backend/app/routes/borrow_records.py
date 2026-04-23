from datetime import date, timedelta

from flask import Blueprint, request
from flask_jwt_extended import get_jwt, jwt_required
from sqlalchemy import or_

from app.models import Book, BorrowRecord, User
from app.utils.decorators import admin_required, current_user
from app.utils.response import fail, ok, page_result
from extensions import db

borrow_bp = Blueprint("borrow_records", __name__)


def refresh_overdue_records():
    records = BorrowRecord.query.filter(BorrowRecord.status == "borrowed", BorrowRecord.due_date < date.today()).all()
    for record in records:
        record.status = "overdue"
    if records:
        db.session.commit()


def record_query():
    refresh_overdue_records()
    query = BorrowRecord.query.join(User).join(Book)
    status = request.args.get("status")
    keyword = (request.args.get("keyword") or "").strip()
    user_id = request.args.get("user_id")
    book_id = request.args.get("book_id")
    if status:
        query = query.filter(BorrowRecord.status == status)
    if user_id:
        query = query.filter(BorrowRecord.user_id == int(user_id))
    if book_id:
        query = query.filter(BorrowRecord.book_id == int(book_id))
    if keyword:
        like = f"%{keyword}%"
        query = query.filter(or_(User.username.like(like), User.real_name.like(like), Book.title_zh.like(like), Book.title_en.like(like), Book.isbn.like(like)))
    return query


@borrow_bp.get("")
@admin_required
def list_records():
    page = int(request.args.get("page", 1))
    page_size = min(int(request.args.get("page_size", 10)), 100)
    pagination = record_query().order_by(BorrowRecord.created_at.desc()).paginate(page=page, per_page=page_size, error_out=False)
    return ok(page_result(pagination, [item.to_dict() for item in pagination.items]))


@borrow_bp.get("/my")
@jwt_required()
def my_records():
    user = current_user()
    page = int(request.args.get("page", 1))
    page_size = min(int(request.args.get("page_size", 10)), 100)
    pagination = record_query().filter(BorrowRecord.user_id == user.id).order_by(BorrowRecord.created_at.desc()).paginate(page=page, per_page=page_size, error_out=False)
    return ok(page_result(pagination, [item.to_dict() for item in pagination.items]))


@borrow_bp.post("/borrow")
@jwt_required()
def borrow_book():
    actor = current_user()
    claims = get_jwt()
    data = request.get_json() or {}
    user_id = int(data.get("user_id") or actor.id)
    if claims.get("role") != "admin" and user_id != actor.id:
        return fail("forbidden", 403, 403)
    user = User.query.get(user_id)
    book = Book.query.get(data.get("book_id"))
    if not user or user.status != "active":
        return fail("user disabled or not found", 5001, 400)
    if not book or book.status != "available":
        return fail("book unavailable", 5002, 400)
    if book.available_stock <= 0:
        return fail("book has no available stock", 5003, 400)
    active = BorrowRecord.query.filter(BorrowRecord.user_id == user.id, BorrowRecord.book_id == book.id, BorrowRecord.status.in_(["borrowed", "overdue"])).first()
    if active:
        return fail("duplicate active borrow is not allowed", 5004, 400)
    due_days = int(data.get("due_days") or 30)
    record = BorrowRecord(user_id=user.id, book_id=book.id, borrow_date=date.today(), due_date=date.today() + timedelta(days=due_days), remark=(data.get("remark") or "").strip())
    book.available_stock -= 1
    db.session.add(record)
    db.session.commit()
    return ok(record.to_dict())


@borrow_bp.post("/return/<int:record_id>")
@jwt_required()
def return_book(record_id):
    actor = current_user()
    claims = get_jwt()
    record = BorrowRecord.query.get_or_404(record_id)
    if claims.get("role") != "admin" and record.user_id != actor.id:
        return fail("forbidden", 403, 403)
    if record.status == "returned":
        return fail("record already returned", 5005, 400)
    record.status = "returned"
    record.return_date = date.today()
    if record.book:
        record.book.available_stock = min(record.book.total_stock, record.book.available_stock + 1)
    db.session.commit()
    return ok(record.to_dict())

