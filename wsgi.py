import logging
from datetime import datetime

from flask import request
from flask_socketio import emit, join_room

from app.extensions import socketio
from app.factory import create_app

app = create_app()


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
websocket_logger = logging.getLogger("websockets")
websocket_logger.setLevel(logging.DEBUG)

# Utility function to create private room names


def get_private_room(sender_id, receiver_id):
    """Generate a consistent private room name for the sender and receiver."""
    return f"private_{min(sender_id, receiver_id)}_{max(sender_id, receiver_id)}"


# WebSocket Events


@socketio.on("connect")
def handle_connect():
    """Handle WebSocket connection."""
    user_id = request.args.get("user_id")
    if not user_id:
        logging.warning("Connection rejected: Missing user_id")
        return False  # Reject connection
    logging.info(f"User {user_id} connected via WebSocket")
    emit("connect_success", {"user_id": user_id})


@socketio.on("join_private_room")
def join_private_room(data):
    """Handle user joining a private room."""
    sender_id = data.get("sender_id")
    receiver_id = data.get("receiver_id")

    if not sender_id or not receiver_id:
        logging.error("join_private_room: Missing sender_id or receiver_id")
        emit(
            "error", {"status": "error",
                      "message": "Missing sender_id or receiver_id"}
        )
        return

    try:
        room = get_private_room(sender_id, receiver_id)
        join_room(room)
        logging.info(f"User {sender_id} joined private room {room}")
        emit("user_joined", {"user_id": sender_id}, room=room)
        emit("room_joined", {"room": room,
             "status": "success"}, to=request.sid)
    except Exception as e:
        logging.error(f"Failed to join private room: {str(e)}")
        emit("error", {"status": "error", "message": str(e)})


@socketio.on("send_private_message")
def ws_send_private_message(data):
    """Handle sending a private message."""
    sender_id = data.get("sender_id")
    text = data.get("text")
    receiver_id = data.get("receiver_id")

    if not sender_id or not text or not receiver_id:
        logging.error(
            "send_private_message: Missing sender_id, text, or receiver_id")
        emit(
            "error",
            {"status": "error", "message": "Missing sender_id, text, or receiver_id"},
        )
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
        emit("error", {"status": "error", "message": str(e)})


@socketio.on("disconnect")
def handle_disconnect():
    """Handle WebSocket disconnection."""
    user_id = request.args.get("user_id")
    logging.info(f"User {user_id} disconnected")
    jls_extract_var = emit
    jls_extract_var("user_disconnected", {"user_id": user_id}, broadcast=True)


application = app
