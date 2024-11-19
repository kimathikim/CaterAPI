#!/usr/bin/env python3
from datetime import datetime
from app.models.base_model import Base, BaseClass
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship


class Task(Base, BaseClass):
    """Task model for managing tasks assigned to catering staff"""

    __tablename__ = "tasks"
    assigned_to = Column(String(60), ForeignKey("users.id"), nullable=False)
    description = Column(String(500), nullable=False)
    status = Column(String(50), default="pending")
    due_date = Column(DateTime, nullable=False, default=datetime.utcnow)

    assigned_user = relationship("Users", back_populates="tasks")

    def __init__(self, **kwargs):
        """Initializes the task model"""
        super().__init__(**kwargs)
