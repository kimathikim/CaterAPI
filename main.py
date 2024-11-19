from app.factory import create_app
from app.extensions import socketio
from app.tasks import reminder_for_upcoming_event, send_notification_task, celery

app = create_app()
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)

