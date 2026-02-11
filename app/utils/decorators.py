import jwt
from functools import wraps
from flask import request, current_app, g
from app.utils.response import error_response
from app.models.user import User, UserRole


def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return error_response("Authentication Token is missing!", 401)

        try:
            payload = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )

            # 1. Get the user ID from 'sub' (matches your AuthService)
            user_id = payload.get("sub")

            if not user_id:
                return error_response("Token is missing user_id!", 401)

            # 2. Fetch the user from the database
            user = User.query.get(user_id)
            if not user:
                return error_response("User not found!", 401)

            # 3. Store in Flask 'g' for global access within the request
            g.current_user = user

            # 4. FIX: Pass the user into kwargs so the route function receives it
            # This solves: TypeError: create_booking() missing 1 required positional argument
            kwargs["current_user"] = user

        except jwt.ExpiredSignatureError:
            return error_response("Token is expired!", 401)
        except jwt.InvalidTokenError:
            return error_response("Token is invalid!", 401)

        return f(*args, **kwargs)

    return decorated_function


def roles_required(*roles):
    """
    Decorator for checking specific user roles.
    Expects to be placed AFTER @jwt_required.
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(g, "current_user"):
                return error_response("Authentication required.", 401)

            user = g.current_user
            if user.role.value not in roles:
                return error_response(
                    "User does not have the required permissions.", 403
                )

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    """
    Shortcut decorator for Admin-only access.
    Expects to be placed AFTER @jwt_required.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, "current_user"):
            return error_response("Authentication required.", 401)

        user = g.current_user
        if user.role != UserRole.ADMIN:
            return error_response("Administrator access required.", 403)

        return f(*args, **kwargs)

    return decorated_function
