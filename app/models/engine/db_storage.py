#!/usr/bin/env python3
"""DBStorage class for the catering management system"""

import os
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, func
from app.models.user import Users
from app.models.service import Service
from app.models.order import Order
from app.models.booking import Booking
from app.models.feedback import Feedback
from app.models.notification import Notification
from app.models.message import Messages
from app.models.base_model import Base
from dotenv import load_dotenv

load_dotenv()


class DBStorage:
    """DBStorage class for managing database interactions"""

    __engine = None
    __session = None

    def __init__(self):
        """Initializes the DBStorage instance and sets up the engine"""
        self.__engine = create_engine(
            "mysql+pymysql://{}:{}@{}/{}".format(
                os.getenv("MYSQL_USER"),
                os.getenv("MYSQL_PWD"),
                os.getenv("MYSQL_HOST"),
                os.getenv("MYSQL_DB"),
            ),
            pool_pre_ping=True,
        )

        if os.getenv("ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def reload(self):
        """Create all tables in the database and start the current database session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def all(self, cls=None):
        """Query on the current database session all objects of the given class"""
        classes = [Users, Service, Order, Booking,
                   Feedback, Notification, Messages]
        if cls and cls in classes and self.__session:
            return self.__session.query(cls).all()
        else:
            all_objects = []
            for class_ in classes:
                if self.__session:
                    all_objects.extend(self.__session.query(class_).all())
            return all_objects

    def new(self, obj):
        """Add the object to the current database session"""
        if obj and self.__session:
            self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        if self.__session:
            self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj and self.__session:
            self.__session.delete(obj)

    def close(self):
        """Close the current database session"""
        if self.__session:
            self.__session.remove()

    def get(self, cls, id):
        """Get an object based on its class and ID"""
        if cls and id and self.__session:
            return self.__session.query(cls).get(id)
        return None

    def get_by_email(self, cls, email):
        """Get an object based on its class and email"""
        if cls and email and self.__session:
            return self.__session.query(cls).filter_by(email=email).first()
        return None

    def get_all_by_user(self, cls, user_id):
        """Get all objects for a given user based on the class"""
        if cls and user_id and self.__session:
            return self.__session.query(cls).filter_by(user_id=user_id).all()
        return []

    def update(self, obj, data):
        """Update an object's attributes with provided data"""
        if obj and data:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            self.save()

    def search(self, cls, search_term):
        """Search for a term in all columns of the given class"""
        if cls and search_term:
            from sqlalchemy import or_

            columns = [column for column in cls.__table__.columns]
            if self.__session:
                query = self.__session.query(cls).filter(
                    or_(*[column.ilike(f"%{search_term}%")
                        for column in columns])
                )
                return query.all()
        return []

    def get_messages(self, sender_id, receiver_id):
        """Get all messages between two users"""
        from app.models.message import Messages
        from sqlalchemy import or_, and_

        if self.__session:
            return (
                self.__session.query(Messages)
                .filter(
                    or_(
                        and_(
                            Messages.sender_id == sender_id,
                            Messages.receiver_id == receiver_id,
                        ),
                        and_(
                            Messages.sender_id == receiver_id,
                            Messages.receiver_id == sender_id,
                        ),
                    )
                )
                .order_by(Messages.timestamp.asc())
                .all()
            )

    def count(self, cls, filters=None):
        """Count the number of objects in storage for a given class"""

        if cls and self.__session:
            query = self.__session.query(func.count(cls.id))
            if filters:
                for key, value in filters.items():
                    query = query.filter(getattr(cls, key) == value)
            return query.scalar()
        return 0

    def count_orders_by_status(self, status):
        """Count the number of orders by status"""
        from app.models.order import Order

        if self.__session:
            return (
                self.__session.query(func.count(Order.id))
                .filter(Order.status == status)
                .scalar()
            )

    def count_feedbacks(self):
        """Count the number of feedback entries"""
        from app.models.feedback import Feedback

        if self.__session:
            return self.__session.query(func.count(Feedback.id)).scalar()

    def count_bookings_by_date_range(self, start_date, end_date):
        """Count the number of bookings within a given date range"""
        from app.models.booking import Booking

        if self.__session:
            return (
                self.__session.query(func.count(Booking.id))
                .filter(
                    Booking.event_date >= start_date, Booking.event_date <= end_date
                )
                .scalar()
            )

    def get_average(self, cls, field):
        """Get the average value for a given field of a class"""
        if cls and field and self.__session:
            return self.__session.query(func.avg(getattr(cls, field))).scalar()
        return 0
