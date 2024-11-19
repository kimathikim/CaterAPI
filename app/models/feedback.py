# models/feedback.py

from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import Base, BaseClass


class Feedback(Base, BaseClass):
    """Feedback model for storing client feedback"""

    __tablename__ = "feedback"
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    service_id = Column(String(60), ForeignKey("services.id"), nullable=False)
    rating = Column(Float, nullable=False)
    comment = Column(String(500))

    user = relationship("Users", back_populates="feedback")
    service = relationship("Service", back_populates="feedback")

    def __init__(self, **kwargs):
        """Initializes the feedback model"""
        super().__init__(**kwargs)
