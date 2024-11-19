from flask_jwt_extended import get_jwt_identity, jwt_required
from app.tasks import reminder_for_upcoming_event, send_notification_task
from flask import Blueprint, jsonify, request
from app.services.notification_service import NotificationService

notifications_bp = Blueprint("notifications", __name__)



@notifications_bp.route("/send_notification", methods=["POST"])
@jwt_required()
def send_notification():
    data = request.json
    if data is None or "user_id" not in data or "message" not in data:
        return jsonify({"error": "Missing required fields: user_id, message"}), 400

    user_id = data.get("user_id")
    message = data.get("message")

    send_notification_task.delay(user_id, message)

    return jsonify({"status": "Notification task has been queued."}), 202


@notifications_bp.route("/send_event_reminder/<string:event_id>", methods=["GET"])
@jwt_required()
def send_event_reminder(event_id):
    reminder_for_upcoming_event.delay(event_id)

    return jsonify({"status": "Event reminder task has been queued."}), 202


@notifications_bp.route("/notifications", methods=["POST"])
@jwt_required()
def create_notification():
    data = request.json
    if not data or not data.get("user_id") or not data.get("message"):
        return jsonify({"error": "Missing required fields: user_id, message"}), 400

    response = NotificationService.create_notification(data)
    return jsonify({"notification": response}), 201


@notifications_bp.route("/notifications", methods=["GET"])
@jwt_required()
def get_notifications():
    user_id = get_jwt_identity()
    notifications = NotificationService.get_notification(user_id)

    return notifications


@notifications_bp.route(
    "/notifications/mark_as_read/<string:notification_id>", methods=["PUT"]
)
@jwt_required()
def mark_as_read(notification_id):
    """Mark a notification as read for the authenticated user"""
    response = NotificationService.mark_as_read(notification_id)
    if "error" in response:
        return jsonify(response), 404
    return jsonify(response), 200
