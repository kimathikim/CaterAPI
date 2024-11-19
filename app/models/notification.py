from datetime import datetime
from app.models.base_model import Base, BaseClass
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship


class Notification(Base, BaseClass):
    __tablename__ = "notifications"

    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    message = Column(String(255), nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("Users", back_populates="notifications")

    def __init__(self, **kwargs):
        """Initializes the Notification class"""
        super().__init__(**kwargs)
