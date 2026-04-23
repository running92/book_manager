import os

from flask import Flask, send_from_directory

from app.routes import register_blueprints
from app.services.seed import seed_demo_data
from app.utils.response import fail, ok
from config import Config
from extensions import cors, db, jwt


def create_app():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    dist_dir = os.path.abspath(os.path.join(root_dir, "frontend", "dist"))
    app = Flask(__name__, static_folder=dist_dir, static_url_path="")
    app.config.from_object(Config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    register_blueprints(app)

    with app.app_context():
        db.create_all()
        seed_demo_data(False)

    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    @app.route("/api/health")
    def health():
        return ok({"status": "ok"})

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def spa_fallback(path):
        if path.startswith("api/"):
            return fail("not found", 404, 404)
        index_file = os.path.join(dist_dir, "index.html")
        if os.path.exists(index_file):
            return send_from_directory(dist_dir, "index.html")
        return ok(
            {
                "message": "Frontend dist not found. Run `cd frontend && npm run build`.",
                "api": "/api/health",
            }
        )

    @app.errorhandler(404)
    def not_found(_):
        return fail("not found", 404, 404)

    @app.errorhandler(Exception)
    def internal_error(error):
        app.logger.exception(error)
        return fail("internal server error", 500, 500)

    return app

