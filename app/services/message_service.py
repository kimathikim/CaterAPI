from app.extensions import socketio
from app.models import storage
from app.models.message import Messages


class MessageService:
    @staticmethod
    def send_message(data):
        """Send a message between users"""
        try:
            message = Messages(**data)
            message.save()
            # Emit the message via socket.io to the receiver
            socketio.emit("new_message", message.to_dict(), room=data["receiver_id"])
            return {"message": "Message sent successfully", "message_id": message.id}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_message(message_id):
        """Get message details by ID"""
        message = storage.get(Messages, message_id)
        if not message:
            return {"error": "Message not found"}

        return message.to_dict()

    @staticmethod
    def list_messages(sender_id, receiver_id):
        """List all messages between two users"""
        messages = storage.get_messages(sender_id, receiver_id)
        if not messages:
            return {"error": "No messages found"}
        return [message.to_dict() for message in messages]

    @staticmethod
    def delete_message(message_id):
        """Delete a message by ID"""
        message = storage.get(Messages, message_id)
        if not message:
            return {"error": "Message not found"}

        try:
            storage.delete(message)
            storage.save()
            return {"message": "Message deleted successfully"}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def list_user_messages(user_id):
        """List all messages for a specific user"""
        messages = storage.search(Messages, {"sender_id": user_id})
        return [message.to_dict() for message in messages]
