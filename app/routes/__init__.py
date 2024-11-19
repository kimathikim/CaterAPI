
from app.routes.auth import auth_bp
from app.routes.orders import orders_bp
from app.routes.tasks import tasks_bp
from app.routes.notification import notifications_bp
from app.routes.messages import messages_bp
from app.routes.bookings import bookings_bp
from app.routes.user import user_bp


def register_routes(app):
    """Register all blueprints with the Flask app"""
    app.register_blueprint(auth_bp, url_prefix="/api/v1")
    app.register_blueprint(orders_bp, url_prefix="/api/v1")
    app.register_blueprint(tasks_bp, url_prefix="/api/v1")
    app.register_blueprint(notifications_bp, url_prefix="/api/v1")
    app.register_blueprint(messages_bp, url_prefix="/api/v1")
    app.register_blueprint(bookings_bp, url_prefix="/api/v1")
    app.register_blueprint(user_bp, url_prefix="/api/v1")
