from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship
from app.models.base_model import Base, BaseClass


class Service(Base, BaseClass):
    """Service model for services offered by the catering company"""

    __tablename__ = "services"
    name = Column(String(128), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    availability = Column(String(50), default="available")

    orders = relationship("Order", back_populates="service")
    feedback = relationship("Feedback", back_populates="service")


    def __init__(self, **kwargs):
        """Initializes the service model"""
        super().__init__(**kwargs)
