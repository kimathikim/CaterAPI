# analytics.py
# pyright: ignore[
# pylint: disable=E1101
# pylint: disable
# pylint: disable
# pylint: disable
# ]
from flask import Blueprint, jsonify
from app.services.user_analytics_service import UserAnalyticsService

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/analytics/summary", methods=["GET"])
def get_summary():
    """Endpoint to get a summary of key analytics data"""
    summary = UserAnalyticsService.get_summary()
    return jsonify(summary)


@analytics_bp.route("/analytics/orders", methods=["GET"])
def get_order_stats():
    """Endpoint to get statistics on orders"""
    stats = UserAnalyticsService.get_order_stats()
    return jsonify(stats)


@analytics_bp.route("/analytics/bookings", methods=["GET"])
def get_booking_stats():
    """Endpoint to get statistics on bookings"""
    stats = UserAnalyticsService.get_booking_stats()
    return jsonify(stats)


@analytics_bp.route("/analytics/feedback", methods=["GET"])
def get_feedback_stats():
    """Endpoint to get statistics on feedback received"""
    stats = UserAnalyticsService.get_feedback_stats()
    return jsonify(stats)


@analytics_bp.route("/analytics/user-activity", methods=["GET"])
def get_user_activity_stats():
    """Endpoint to get statistics on user activity"""
    stats = UserAnalyticsService.get_user_activity_stats()
    return jsonify(stats)
