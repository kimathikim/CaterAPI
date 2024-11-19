from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import redis
import os
from flask import Flask
from app.routes import register_routes
from app.models import storage
from app.config import Config
from flask import request
from flask_socketio import emit, join_room, disconnect
from app.extensions import socketio
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_private_room(sender_id, receiver_id):
    """Generate a consistent private room name for the sender and receiver."""
    return f"private_{min(sender_id, receiver_id)}_{max(sender_id, receiver_id)}"


@socketio.on("connect")
def handle_connect():
    """Handle WebSocket connection."""
    user_id = request.args.get("user_id")
    logging.info(f"User {user_id} connected via WebSocket")
    if not user_id:
        logging.warning("Connection rejected: Missing user_id")
        disconnect()


@socketio.on("join_private_room")
def join_private_room(data):
    """Handle user joining a private room."""
    sender_id = data.get("sender_id")
    receiver_id = data.get("receiver_id")

    if not sender_id or not receiver_id:
        logging.error("join_private_room: Missing sender_id or receiver_id")
        return

    try:
        room = get_private_room(sender_id, receiver_id)
        join_room(room)
        logging.info(f"User {sender_id} joined private room {room}")
        emit("room_joined", {"room": room, "status": "success"}, room=room)
    except Exception as e:
        logging.error(f"Failed to join private room: {str(e)}")
        emit("room_joined", {"status": "error", "message": str(e)})


@socketio.on("send_private_message")
def ws_send_private_message(data):
    """Handle sending a private message."""
    sender_id = data.get("sender_id")
    text = data.get("text")
    receiver_id = data.get("receiver_id")

    if not sender_id or not text or not receiver_id:
        logging.error("send_private_message: Missing sender_id, text, or receiver_id")
        return

    try:
        room = get_private_room(sender_id, receiver_id)
        message = {
            "authorId": sender_id,
            "authorName": data.get("sender_name", "Unknown"),
            "text": text,
            "timestamp": datetime.utcnow().isoformat(),
        }
        emit("receive_private_message", message, room=room)
        logging.info(f"Message sent to room {room} from {sender_id}: {text}")
    except Exception as e:
        logging.error(f"Error sending private message: {str(e)}")


@socketio.on("disconnect")
def handle_disconnect():
    """Handle WebSocket disconnection."""
    logging.info("Client disconnected")


storage.reload()


load_dotenv()

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
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    socketio.init_app(
        app,
        ping_interval=25,
        ping_timeout=120,
        async_mode="eventlet",
        cors_allowed_origins="*",
    )
    mail.init_app(app)


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


app = create_app()
if __name__ != "__main__":
    application = app

