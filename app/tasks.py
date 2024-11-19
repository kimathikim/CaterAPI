from app.config import Config
from app.models import storage
from app.services.notification_service import NotificationService
from celery import Celery

celery = Celery(__name__)
celery.conf.update(
    {
        "broker_url": Config.CELERY_BROKER_URL,
        "result_backend": Config.CELERY_RESULT_BACKEND,
        "broker_use_ssl": {"ssl_cert_reqs": "CERT_NONE"},
        "result_backend_use_ssl": {"ssl_cert_reqs": "CERT_NONE"},
    }
)


@celery.task
def send_notification_task(user_id, message):
    """Background task to send notifications to a user"""
    # Perform the import within the task function
    from app.factory import create_app

    # Create a Flask app instance for the context
    app = create_app()

    with app.app_context():
        print(f"Sending notification to user {user_id}: {message}")
        try:
            NotificationService.send_notification(user_id, message)
            print("Notification sent successfully")
        except Exception as e:
            print(f"Error sending notification: {e}")


@celery.task
def reminder_for_upcoming_event(event_id):
    """Reminds users of an upcoming event"""
    from app.factory import create_app
    from app.models.booking import Booking

    app = create_app()

    with app.app_context():
        event = storage.get(Booking, event_id)
        if event:
            for attendee in event.attendees:
                NotificationService.send_notification(
                    attendee.id, f"Reminder for upcoming event: {event.name}"
                )
            print(f"Reminders sent for event {event.name}")
        else:
            print("Event not found")
