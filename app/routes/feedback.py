# routes/feedback.py

from flask import Blueprint, request
from app.services.feedback_service import FeedbackService

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['POST'])
def create_feedback():
    """Submit feedback for services"""
    data = request.json
    response = FeedbackService.create_feedback(data)
    return response, 201 if "feedback_id" in response else 400

@feedback_bp.route('/feedback/<feedback_id>', methods=['GET'])
def get_feedback(feedback_id):
    """Get feedback by ID"""
    response = FeedbackService.get_feedback(feedback_id)
    return response, 200 if "id" in response else 404

@feedback_bp.route('/feedback', methods=['GET'])
def list_feedback():
    """List all feedback"""
    response = FeedbackService.list_feedback()
    return {"feedback": response}, 200

@feedback_bp.route('/users/<user_id>/feedback', methods=['GET'])
def list_feedback_by_user(user_id):
    """List feedback submitted by a specific user"""
    response = FeedbackService.list_feedback_by_user(user_id)
    return {"feedback": response}, 200

