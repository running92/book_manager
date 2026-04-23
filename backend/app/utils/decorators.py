from functools import wraps

from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from app.models import User
from app.utils.response import fail


def current_user():
    user_id = get_jwt_identity()
    if not user_id:
        return None
    return User.query.get(int(user_id))


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return fail("forbidden", 403, 403)
        return fn(*args, **kwargs)

    return wrapper

