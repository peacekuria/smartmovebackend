from flask import jsonify

class APIError(Exception):
    """Base class for custom API exceptions."""
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class BadRequestError(APIError):
    """Custom exception for Bad Request (400) errors."""
    status_code = 400

class UnauthorizedError(APIError):
    """Custom exception for Unauthorized (401) errors."""
    status_code = 401

class ForbiddenError(APIError):
    """Custom exception for Forbidden (403) errors."""
    status_code = 403

class NotFoundError(APIError):
    """Custom exception for Not Found (404) errors."""
    status_code = 404

class ConflictError(APIError):
    """Custom exception for Conflict (409) errors."""
    status_code = 409

class InternalServerError(APIError):
    """Custom exception for Internal Server Error (500) errors."""
    status_code = 500

def register_error_handlers(app):
    """Registers custom error handlers with the Flask application."""
    @app.errorhandler(APIError)
    def handle_api_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(400)
    def handle_bad_request(e):
        return jsonify({"status": "error", "message": "Bad Request"}), 400

    @app.errorhandler(401)
    def handle_unauthorized(e):
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    @app.errorhandler(403)
    def handle_forbidden(e):
        return jsonify({"status": "error", "message": "Forbidden"}), 403

    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({"status": "error", "message": "Not Found"}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        return jsonify({"status": "error", "message": "Method Not Allowed"}), 405

    @app.errorhandler(500)
    def handle_internal_server_error(e):
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500
