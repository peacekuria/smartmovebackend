from flask import request
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.utils.response import error_response


def check_auth():
    """
    Optional global middleware check.
    Can be used in app.before_request to protect all routes except auth.
    """
    # List of endpoints that don't require authentication
    open_endpoints = ["auth.login", "auth.register", "static"]

    if request.endpoint in open_endpoints:
        return None

    try:
        verify_jwt_in_request()
    except Exception as e:
        return error_response("Missing or invalid authentication token", 401)
from functools import wraps
from flask import request, jsonify, current_app
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Assuming current_app.config['SECRET_KEY'] is set and used for JWT encoding
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            # You might want to fetch the user from the database here
            request.user_id = data.get('user_id')
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated
