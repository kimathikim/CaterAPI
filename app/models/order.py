from app.models.base_model import Base, BaseClass
from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship


class Order(Base, BaseClass):
    """Order model for catering orders"""

    __tablename__ = "orders"
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    service_id = Column(String(60), ForeignKey("services.id"), nullable=False)
    status = Column(String(50), default="pending")
    total_cost = Column(Float, nullable=False)
    notes = Column(String(500))

    user = relationship("Users", back_populates="orders")
    service = relationship("Service", back_populates="orders")

    def __init__(self, **kwargs):
        """Initializes the order model"""
        super().__init__(**kwargs)
