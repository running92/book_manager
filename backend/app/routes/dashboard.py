from datetime import date, timedelta

from flask import Blueprint
from flask_jwt_extended import get_jwt, jwt_required
from sqlalchemy import func

from app.models import Book, BorrowRecord, Category, User
from app.utils.decorators import current_user
from app.utils.response import ok

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/stats")
@jwt_required()
def stats():
    claims = get_jwt()
    user = current_user()
    if claims.get("role") == "admin":
        recent = BorrowRecord.query.order_by(BorrowRecord.created_at.desc()).limit(6).all()
        distribution = (
            Category.query.outerjoin(Book)
            .with_entities(Category.name_zh, Category.name_en, func.count(Book.id).label("value"))
            .group_by(Category.id)
            .order_by(Category.sort_order.asc())
            .all()
        )
        today = date.today()
        trend = []
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            count = BorrowRecord.query.filter(BorrowRecord.borrow_date == day).count()
            trend.append({"date": day.isoformat(), "count": count})
        return ok(
            {
                "book_total": Book.query.count(),
                "available_total": Book.query.with_entities(func.sum(Book.available_stock)).scalar() or 0,
                "borrowed_total": BorrowRecord.query.filter(BorrowRecord.status.in_(["borrowed", "overdue"])).count(),
                "user_total": User.query.count(),
                "current_borrow_total": BorrowRecord.query.filter(BorrowRecord.status.in_(["borrowed", "overdue"])).count(),
                "record_total": BorrowRecord.query.count(),
                "recent_records": [item.to_dict() for item in recent],
                "category_distribution": [{"name_zh": x.name_zh, "name_en": x.name_en, "value": x.value} for x in distribution],
                "borrow_trend": trend,
            }
        )

    current_records = BorrowRecord.query.filter(BorrowRecord.user_id == user.id, BorrowRecord.status.in_(["borrowed", "overdue"])).order_by(BorrowRecord.due_date.asc()).all()
    return ok(
        {
            "recommended_books": [b.to_dict(False) for b in Book.query.filter(Book.status == "available", Book.available_stock > 0).limit(6).all()],
            "new_books": [b.to_dict(False) for b in Book.query.filter(Book.status == "available").order_by(Book.created_at.desc()).limit(6).all()],
            "my_current": [r.to_dict() for r in current_records],
            "reminders": [r.to_dict() for r in current_records if r.status == "overdue" or r.due_date <= date.today() + timedelta(days=3)],
        }
    )

