from functools import wraps
from flask import abort, redirect, url_for, request
from flask_login import current_user
from nuri.models import Access


def roles_required(*required_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("auth.login", next=request.url))
            if current_user.role not in required_roles:
                return redirect(url_for("auth.login", next=request.url))
            return func(*args, **kwargs)

        return wrapper

    return decorator


def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("x-api-key")
        if not api_key:
            abort(401, description="Missing API key")

        access = Access.query.filter_by(api_key=api_key).first()
        if not access:
            abort(403, description="Invalid or unauthorized API key")

        return f(*args, **kwargs)

    return decorated_function
