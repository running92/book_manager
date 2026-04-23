import os
import uuid

from flask import Blueprint, current_app, request

from app.utils.decorators import admin_required
from app.utils.response import fail, ok

uploads_bp = Blueprint("uploads", __name__)

ALLOWED = {"png", "jpg", "jpeg", "gif", "webp"}


@uploads_bp.post("/cover")
@admin_required
def upload_cover():
    file = request.files.get("file")
    if not file or not file.filename:
        return fail("file is required")
    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED:
        return fail("unsupported file type")
    filename = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(path)
    return ok({"url": f"/uploads/{filename}"})

