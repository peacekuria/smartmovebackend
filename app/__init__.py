from flask import Flask, jsonify
from app.config import Config
from app.extensions import db, migrate, cors, bcrypt
from app.utils.errors import register_error_handlers
import os


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Configure CORS from environment variable
    frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost:5173')
    cors.init_app(app, resources={r"/api/*": {"origins": frontend_url}})
    
    bcrypt.init_app(app)

    # Register blueprints with /api prefix
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    from app.routes.booking import booking_bp
    from app.routes.mover import mover_bp
    from app.routes.review import review_bp
    from app.routes.admin import admin_bp
    from app.routes.chat import chat_bp
    from app.routes.inventory import inventory_bp
    from app.routes.maps import maps_bp
    from app.routes.notification import notification_bp
    from app.routes.payments import payment_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(booking_bp, url_prefix='/api/bookings')
    app.register_blueprint(mover_bp, url_prefix='/api/movers')
    app.register_blueprint(review_bp, url_prefix='/api/reviews')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
    app.register_blueprint(maps_bp, url_prefix='/api/maps')
    app.register_blueprint(notification_bp, url_prefix='/api/notifications')
    app.register_blueprint(payment_bp, url_prefix='/api/payments')

    # Register error handlers
    register_error_handlers(app)

    # Health check endpoint for Render/load balancers
    @app.route('/health', methods=['GET'])
    def health_check():
        """Basic health check - returns 200 if app is running."""
        return jsonify({"status": "ok"}), 200

    @app.route('/health/ready', methods=['GET'])
    def readiness_check():
        """Readiness check - verifies database connectivity."""
        try:
            db.session.execute(db.text('SELECT 1'))
            return jsonify({"status": "ready", "database": "connected"}), 200
        except Exception as e:
            return jsonify({"status": "not ready", "database": "disconnected", "error": str(e)}), 503

    return app
