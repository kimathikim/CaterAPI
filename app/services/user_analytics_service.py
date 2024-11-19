from app.models import storage
from app.models.user import Users
from app.models.booking import Booking
from app.models.order import Order
from datetime import datetime, timedelta


class UserAnalyticsService:
    @staticmethod
    def get_summary():
        """Get a summary of key metrics"""
        total_orders = storage.count("Order")
        total_bookings = storage.count("Booking")
        total_feedbacks = storage.count("Feedback")
        total_users = storage.count("Users")

        summary = {
            "total_orders": total_orders,
            "total_bookings": total_bookings,
            "total_feedbacks": total_feedbacks,
            "total_users": total_users,
        }

        return summary

    @staticmethod
    def get_order_stats():
        """Get statistics on orders"""
        completed_orders = storage.count(
            "Order", filters={"status": "completed"})
        pending_orders = storage.count("Order", filters={"status": "pending"})
        canceled_orders = storage.count(
            "Order", filters={"status": "canceled"})

        order_stats = {
            "completed_orders": completed_orders,
            "pending_orders": pending_orders,
            "canceled_orders": canceled_orders,
        }

        return order_stats

    @staticmethod
    def get_booking_stats():
        """Get statistics on bookings"""
        upcoming_bookings = storage.count(
            "Booking", filters={"event_date": {"$gte": datetime.now()}}
        )
        past_bookings = storage.count(
            "Booking", filters={"event_date": {"$lt": datetime.now()}}
        )

        booking_stats = {
            "upcoming_bookings": upcoming_bookings,
            "past_bookings": past_bookings,
        }

        return booking_stats

    @staticmethod
    def get_feedback_stats():
        """Get statistics on feedback received"""
        total_feedbacks = storage.count("Feedback")
        avg_rating = storage.get_average("Feedback", "rating")

        feedback_stats = {
            "total_feedbacks": total_feedbacks,
            "average_rating": avg_rating,
        }

        return feedback_stats

    @staticmethod
    def get_user_activity_stats():
        """Get statistics on user activity"""
        total_users = storage.count("Users")
        active_users = storage.count(
            "Users",
            filters={"last_login": {"$gte": datetime.now() - timedelta(days=7)}},
        )
        new_signups = storage.count(
            "Users",
            filters={"created_at": {
                "$gte": datetime.now() - timedelta(days=30)}},
        )

        user_activity_stats = {
            "total_users": total_users,
            "active_users_last_7_days": active_users,
            "new_signups_last_30_days": new_signups,
        }

        return user_activity_stats

    @staticmethod
    def get_user_count():
        """Get the total number of users"""
        users = storage.all(Users)
        return {"total_users": len(users)}

    @staticmethod
    def get_most_popular_service():
        """Get the most frequently booked service"""
        bookings = storage.all(Booking)
        service_counts = {}

        for booking in bookings:
            service = booking.service_id
            if service in service_counts:
                service_counts[service] += 1
            else:
                service_counts[service] = 1

        most_popular_service = max(service_counts, key=service_counts.get)
        return {
            "most_popular_service": most_popular_service,
            "count": service_counts[most_popular_service],
        }

    @staticmethod
    def get_order_summary():
        """Get the summary of all orders"""
        orders = storage.all(Order)
        completed_orders = len(
            [order for order in orders if order.status == "completed"]
        )
        pending_orders = len(
            [order for order in orders if order.status == "pending"])

        return {
            "total_orders": len(orders),
            "completed_orders": completed_orders,
            "pending_orders": pending_orders,
        }
