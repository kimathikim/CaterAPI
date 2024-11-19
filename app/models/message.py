# models/message.py

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base_model import Base, BaseClass


class Messages(Base, BaseClass):
    """Message model for storing messages between users"""

    __tablename__ = "messages"
    sender_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    receiver_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    content = Column(String(500), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    sender = relationship(
        "Users", foreign_keys=[sender_id], back_populates="sent_messages"
    )
    receiver = relationship(
        "Users", foreign_keys=[receiver_id], back_populates="received_messages"
    )

    def __init__(self, **kwargs):
        """Initializes the message model"""
        super().__init__(**kwargs)
