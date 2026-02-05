import jwt
from functools import wraps
from flask import request, current_app, g
from app.utils.response import error
from app.models.user import User, UserRole

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return error("Authentication Token is missing!", 401)

        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            user_id = payload['user_id']
            user = User.query.get(user_id)
            if not user:
                return error("User not found!", 401)
            g.current_user = user # Store the whole user object in g
        except jwt.ExpiredSignatureError:
            return error("Token is expired!", 401)
        except jwt.InvalidTokenError:
            return error("Token is invalid!", 401)
        except KeyError:
            return error("Token is missing user_id!", 401)

        return f(*args, **kwargs)
    return decorated_function

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # This decorator should be stacked AFTER @jwt_required
            if not hasattr(g, 'current_user'):
                return error("Authentication required.", 401)
            
            user = g.current_user
            # .value gets the string representation of the enum, e.g., 'customer'
            if user.role.value not in roles:
                return error("User does not have the required permissions.", 403)

            # Pass the user object to the decorated function
            kwargs['current_user'] = user
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # This decorator should be stacked AFTER @jwt_required
        if not hasattr(g, 'current_user'):
            return error("Authentication required. Use @jwt_required before @admin_required.", 401)
        
        user = g.current_user
        if user.role != UserRole.ADMIN:
            return error("Administrator access required.", 403)
        
        # Pass the user object to the decorated function
        kwargs['current_user'] = user
        return f(*args, **kwargs)
    return decorated_function