from flask import Blueprint, request
from app.services.message_service import MessageService

messages_bp = Blueprint("messages", __name__)


@messages_bp.route("/messages", methods=["POST"])
def send_message():
    """Send a message between users"""
    data = request.json
    response = MessageService.send_message(data)
    return response, 201 if "message_id" in response else 400


@messages_bp.route("/messages/<message_id>", methods=["GET"])
def get_message(message_id):
    """Get a message by ID"""
    response = MessageService.get_message(message_id)
    return response, 200 if "id" in response else 404


@messages_bp.route("/messages/<sender_id>/<receiver_id>", methods=["GET"])
def list_messages(sender_id, receiver_id):
    """List all messages between two users"""
    response = MessageService.list_messages(sender_id, receiver_id)
    return {"messages": response}, 200


@messages_bp.route("/messages/<message_id>", methods=["DELETE"])
def delete_message(message_id):
    """Delete a message by ID"""
    response = MessageService.delete_message(message_id)
    return response, 200 if "message" in response else 404


@messages_bp.route("/users/<user_id>/messages", methods=["GET"])
def list_user_messages(user_id):
    """List all messages for a specific user"""
    response = MessageService.list_user_messages(user_id)
    return {"messages": response}, 200
