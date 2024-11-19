from app.models import storage
from app.models.feedback import Feedback


class FeedbackService:
    @staticmethod
    def add_feedback(data):
        """Add feedback for an order or booking"""
        try:
            feedback = Feedback(**data)
            storage.new(feedback)
            storage.save()
            return {
                "message": "Feedback added successfully",
                "feedback_id": feedback.id,
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_feedback(feedback_id):
        """Get feedback details by ID"""
        feedback = storage.get(Feedback, feedback_id)
        if not feedback:
            return {"error": "Feedback not found"}

        return feedback.to_dict()

    @staticmethod
    def list_feedbacks():
        """List all feedback"""
        feedbacks = storage.all(Feedback)
        return [feedback.to_dict() for feedback in feedbacks]

    @staticmethod
    def delete_feedback(feedback_id):
        """Delete feedback by ID"""
        feedback = storage.get(Feedback, feedback_id)
        if not feedback:
            return {"error": "Feedback not found"}

        try:
            storage.delete(feedback)
            storage.save()
            return {"message": "Feedback deleted successfully"}
        except Exception as e:
            return {"error": str(e)}
