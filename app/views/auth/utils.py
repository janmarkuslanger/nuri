from functools import wraps
from flask import abort, redirect, url_for, request
from flask_login import current_user


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
