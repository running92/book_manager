from app.routes.auth import auth_bp
from app.routes.books import books_bp
from app.routes.borrow_records import borrow_bp
from app.routes.categories import categories_bp
from app.routes.dashboard import dashboard_bp
from app.routes.uploads import uploads_bp
from app.routes.users import users_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(books_bp, url_prefix="/api/books")
    app.register_blueprint(categories_bp, url_prefix="/api/categories")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(borrow_bp, url_prefix="/api/borrow-records")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    app.register_blueprint(uploads_bp, url_prefix="/api/upload")

