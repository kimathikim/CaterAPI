"""BaseModel class for the catering management system"""

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from app.utils.date_time import format_datetime, parse_datetime

Base = declarative_base()


class BaseClass:
    """This will be inherited by all model classes in the project"""

    id = Column(
        String(60),
        primary_key=True,
        default=lambda: str(uuid4()),
        unique=True,
        nullable=False,
    )
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    def __init__(self, **kwargs):
        """Initializes the base model class"""
        self.id = str(uuid4())
        self.created_at = self.updated_at = datetime.now()
        for key, value in kwargs.items():
            if key != "__class__":
                setattr(self, key, value)

        if "created_at" in kwargs and isinstance(kwargs["created_at"], str):
            self.created_at = parse_datetime(kwargs["created_at"])
        if "updated_at" in kwargs and isinstance(kwargs["updated_at"], str):
            self.updated_at = parse_datetime(kwargs["updated_at"])

    def save(self):
        """Updates `updated_at` and saves the instance to the database"""
        from app.models import storage

        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Returns a dictionary representation of the instance"""
        new_dict = self.__dict__.copy()
        new_dict.pop("_sa_instance_state", None)
        new_dict["created_at"] = format_datetime(self.created_at)
        new_dict["updated_at"] = format_datetime(self.updated_at)
        new_dict["__class__"] = self.__class__.__name__
        return new_dict

    def delete(self):
        """Deletes the instance from the database"""
        from app.models import storage

        storage.delete(self)
        storage.save()
