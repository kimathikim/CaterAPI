from app.config import Config
from app.extensions import init_extensions
from app.models import storage
from app.routes import register_routes
from flask import Flask

storage.reload()


def create_app(config_class=Config):
    """Factory function for creating a Flask application instance."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    init_extensions(app)

    register_routes(app)

    @app.errorhandler(404)
    def page_not_found(e):
        return {"error": "Not found"}, 404

    @app.errorhandler(500)
    def internal_error(e):
        return {"error": "Internal server error"}, 500

    @app.teardown_appcontext
    def teardown_db(exception):
        storage.close()

    return app
