import jwt
from functools import wraps
from flask import request, jsonify, current_app, g
from app.utils.response import error

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
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            g.current_user = data['user_id'] # Assuming user_id is stored in the token
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
            if not hasattr(g, 'current_user'):
                return error("User not authenticated.", 401)

            # Placeholder for actual role checking logic
            # This would typically involve fetching user roles from the DB
            # and comparing them with the required 'roles'.
            # For now, we'll assume any authenticated user passes for migration.
            # You'll need to implement actual role fetching and checking here.
            # Example:
            # user = User.query.get(g.current_user)
            # if user and user.role in roles:
            #     return f(*args, **kwargs)
            # return error("User does not have the required role.", 403)

            return f(*args, **kwargs) # Temporarily allow all authenticated users
        return decorated_function
    return decorator