from app.models.base_model import Base, BaseClass
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Time, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, time


class Booking(Base, BaseClass):
    """Booking model for storing event bookings and getting the user details"""

    __tablename__ = "bookings"
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False, index=True)
    services = Column(JSON, nullable=False)  # Store list of services as JSON
    event_name = Column(String(128), nullable=True)  # Optional event name
    event_date = Column(DateTime(timezone=True), nullable=False)  # Timezone aware
    event_time = Column(Time, nullable=False)
    event_location = Column(String(255), nullable=False)
    guest_count = Column(Integer, nullable=False)
    special_instructions = Column(Text, nullable=True)
    manager_id = Column(String(60), nullable=True)
    manager_name = Column(String(60), nullable=True)
    status = Column(String(60), nullable=False, default="Pending")
    total_cost = Column(Integer, nullable=False)  # Total cost of the booking

    user = relationship("Users", back_populates="bookings")

    def to_dicto(self):
        """Convert the Booking object to a dictionary, serializing datetime and time fields."""
        booking_dict = {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": self.user.name if self.user else None,
            "services": self.services,
            "event_name": self.event_name,
            "manager_name": self.manager_name,
            "manager_id": self.manager_id,
            "event_date": self.event_date.isoformat()
            if isinstance(self.event_date, datetime)
            else None,
            "event_time": self.event_time.strftime("%H:%M:%S")
            if isinstance(self.event_time, time)
            else None,
            "event_location": self.event_location,
            "status": self.status,
            "guest_count": self.guest_count,
            "special_instructions": self.special_instructions,
            "total_cost": self.total_cost,
        }
        return booking_dict
