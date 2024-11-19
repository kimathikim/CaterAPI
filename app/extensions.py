import os
import redis
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

load_dotenv()

# Initialize Flask extensions
ma = Marshmallow()
jwt = JWTManager()
socketio = SocketIO()
db = SQLAlchemy()
mail = Mail()
redis_client = redis.Redis()
redis_client = redis.from_url(os.getenv("REDIS_URI"))
cors = CORS()


def init_extensions(app):
    """
    Initialize all extensions with the given Flask application.
    """
    ma.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    socketio.init_app(
        app,
        ping_interval=25,
        ping_timeout=120,
        async_mode="eventlet",
        cors_allowed_origins="*",
        path="socket.io",  # Set custom path without leading slash
    )
    mail.init_app(app)
