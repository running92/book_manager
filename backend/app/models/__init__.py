from datetime import datetime, date
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db


def now():
    return datetime.utcnow()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    real_name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="reader", index=True)
    phone = db.Column(db.String(30), default="")
    email = db.Column(db.String(120), default="")
    status = db.Column(db.String(20), default="active", index=True)
    created_at = db.Column(db.DateTime, default=now)
    updated_at = db.Column(db.DateTime, default=now, onupdate=now)

    borrow_records = db.relationship("BorrowRecord", back_populates="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "real_name": self.real_name,
            "role": self.role,
            "phone": self.phone,
            "email": self.email,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name_zh = db.Column(db.String(80), nullable=False)
    name_en = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), default="")
    sort_order = db.Column(db.Integer, default=0, index=True)
    created_at = db.Column(db.DateTime, default=now)

    books = db.relationship("Book", back_populates="category", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name_zh": self.name_zh,
            "name_en": self.name_en,
            "description": self.description,
            "sort_order": self.sort_order,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(30), unique=True, nullable=False, index=True)
    title_zh = db.Column(db.String(160), nullable=False, index=True)
    title_en = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    publisher = db.Column(db.String(120), default="")
    publish_date = db.Column(db.String(20), default="")
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), index=True)
    cover_image = db.Column(db.String(255), default="")
    description_zh = db.Column(db.Text, default="")
    description_en = db.Column(db.Text, default="")
    total_stock = db.Column(db.Integer, default=1)
    available_stock = db.Column(db.Integer, default=1, index=True)
    location = db.Column(db.String(80), default="")
    status = db.Column(db.String(20), default="available", index=True)
    created_at = db.Column(db.DateTime, default=now)
    updated_at = db.Column(db.DateTime, default=now, onupdate=now)

    category = db.relationship("Category", back_populates="books")
    borrow_records = db.relationship("BorrowRecord", back_populates="book", lazy=True)

    def to_dict(self, include_detail=True):
        data = {
            "id": self.id,
            "isbn": self.isbn,
            "title_zh": self.title_zh,
            "title_en": self.title_en,
            "author": self.author,
            "publisher": self.publisher,
            "publish_date": self.publish_date,
            "category_id": self.category_id,
            "category": self.category.to_dict() if self.category else None,
            "cover_image": self.cover_image,
            "total_stock": self.total_stock,
            "available_stock": self.available_stock,
            "location": self.location,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_detail:
            data.update(
                {
                    "description_zh": self.description_zh,
                    "description_en": self.description_en,
                }
            )
        return data


class BorrowRecord(db.Model):
    __tablename__ = "borrow_records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False, index=True)
    borrow_date = db.Column(db.Date, nullable=False, default=date.today, index=True)
    due_date = db.Column(db.Date, nullable=False, index=True)
    return_date = db.Column(db.Date)
    status = db.Column(db.String(20), default="borrowed", index=True)
    remark = db.Column(db.String(255), default="")
    created_at = db.Column(db.DateTime, default=now)
    updated_at = db.Column(db.DateTime, default=now, onupdate=now)

    user = db.relationship("User", back_populates="borrow_records")
    book = db.relationship("Book", back_populates="borrow_records")

    __table_args__ = (
        db.Index("idx_borrow_user_book_status", "user_id", "book_id", "status"),
    )

    def refresh_overdue(self):
        if self.status == "borrowed" and self.due_date < date.today():
            self.status = "overdue"

    def to_dict(self):
        self.refresh_overdue()
        return {
            "id": self.id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "borrow_date": self.borrow_date.isoformat() if self.borrow_date else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "return_date": self.return_date.isoformat() if self.return_date else None,
            "status": self.status,
            "remark": self.remark,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "user": self.user.to_dict() if self.user else None,
            "book": self.book.to_dict(False) if self.book else None,
        }


class OperationLog(db.Model):
    __tablename__ = "operation_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    action = db.Column(db.String(80), nullable=False)
    detail = db.Column(db.String(255), default="")
    created_at = db.Column(db.DateTime, default=now, index=True)

