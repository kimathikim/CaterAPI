from app.factory import create_app
from app.extensions import socketio
from app.tasks import reminder_for_upcoming_event, send_notification_task, celery

application = create_app()
if __name__ == "__main__":
    # Running with SocketIO, useful for debugging locally
    socketio.run(application, host="0.0.0.0", port=5001, debug=True)
