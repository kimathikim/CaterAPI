from app.models.user import Users
from app.models.notification import Notification
from app.models import storage
from app.extensions import mail, socketio
from flask_mail import Message
from flask import current_app


def send_email_notification(to, subject, body):
    """Send an email notification"""
    msg = Message(
        subject, sender=current_app.config["MAIL_DEFAULT_SENDER"], recipients=[to]
    )

    msg.body = body

    try:
        mail.send(msg)
        print(f"Email sent to {to}")
        return {"status": "success", "message": "Email sent successfully"}
    except Exception as e:
        return {"status": "failure", "message": str(e)}


class NotificationService:
    @staticmethod
    def create_notification(data):
        """Create a new notification"""
        try:
            notification = Notification(**data)
            storage.new(notification)
            storage.save()
            socketio.emit("notification", notification.to_dict(), room=data["user_id"])
            return {
                "message": "Notification created successfully",
                "notification_id": notification.id,
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_notification(notification_id):
        """Get notification details by ID"""
        notification = storage.get(Notification, notification_id)
        if not notification:
            return {"error": "Notification not found"}

        return notification.to_dict()

    @staticmethod
    def list_notifications(user_id):
        """List all notifications for a specific user"""
        try:
            notifications = storage.search(Notification, {"user_id": user_id})
            return {
                "notifications": [
                    notification.to_dict() for notification in notifications
                ],
                "status_code": 200,
            }
        except Exception as e:
            return {"error": str(e), "status_code": 500}

    @staticmethod
    def mark_as_read(notification_id):
        """Mark a notification as read"""
        notification = storage.get(Notification, notification_id)
        if not notification:
            return {"error": "Notification not found"}

        try:
            notification.is_read = True
            storage.save()
            return {"message": "Notification marked as read"}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_notification(notification_id):
        """Delete a notification by ID"""
        notification = storage.get(Notification, notification_id)
        if not notification:
            return {"error": "Notification not found"}

        try:
            storage.delete(notification)
            storage.save()
            return {"message": "Notification deleted successfully"}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def send_notification(user_id, message):
        """Send a notification to the user"""
        from app.tasks import send_notification_task
        user = storage.get(Users, user_id)
        if user:
            # Queue the task to send an email notification asynchronously
            send_notification_task.delay(user.email, message)
            print(f"Notification task queued for {user.email}")
            return {"status": "success", "message": "Notification task queued"}
        else:
            return {"status": "failure", "message": "User not found"}

    @staticmethod
    def send_real_time_notification(event, data):
        """Send real-time notifications to connected clients"""
        try:
            socketio.emit(event, data)
            return {"status": "success", "message": "Real-time notification sent"}
        except Exception as e:
            return {"status": "failure", "message": str(e)}
