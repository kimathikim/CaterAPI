from sqlalchemy import Column, String
from werkzeug.security import generate_password_hash
from app.models.base_model import Base, BaseClass
from sqlalchemy.orm import relationship
from app.models.message import Messages


class Users(Base, BaseClass):
    """User model for the catering management system"""

    __tablename__ = "users"
    name = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    role = Column(String(50), nullable=False)

    orders = relationship("Order", back_populates="user")
    bookings = relationship("Booking", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    feedback = relationship("Feedback", back_populates="user")
    sent_messages = relationship(
        "Messages", foreign_keys=[Messages.sender_id], back_populates="sender"
    )

    received_messages = relationship(
        "Messages", foreign_keys=[Messages.receiver_id], back_populates="receiver"
    )
    tasks = relationship("Task", back_populates="assigned_user")

    def __init__(self, **kwargs):
        """Initializes the user model"""
        super().__init__(**kwargs)

    @staticmethod
    def hash_password(password):
        """Hashes the user password"""
        return generate_password_hash(password)
