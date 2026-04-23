from flask import jsonify


def ok(data=None, message="success"):
    return jsonify({"code": 0, "message": message, "data": data if data is not None else {}})


def fail(message="error", code=1, status=400, data=None):
    return jsonify({"code": code, "message": message, "data": data if data is not None else {}}), status


def page_result(pagination, items):
    return {
        "items": items,
        "total": pagination.total,
        "page": pagination.page,
        "page_size": pagination.per_page,
        "pages": pagination.pages,
    }

