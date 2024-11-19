from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.services.booking_service import BookingService

bookings_bp = Blueprint("bookings", __name__)


@bookings_bp.route("/bookings", methods=["POST"])
@jwt_required()
def create_booking():
    """Create a new booking for an event"""
    user_id = get_jwt_identity()
    data = request.json
    print(data)
    if data is None:
        return {"error": "No data provided"}, 400

    # Attach authenticated user's ID
    data["user_id"] = user_id
    response = BookingService.create_booking(data)
    return response, 201 if "booking_id" in response else 400


@bookings_bp.route("/bookings/<booking_id>", methods=["GET"])
@jwt_required()
def get_booking(booking_id):
    """Get a booking by ID"""
    user_id = get_jwt_identity()
    response = BookingService.get_booking(booking_id, user_id)
    return response, 200 if "id" in response else 404


@bookings_bp.route("/bookings/<booking_id>", methods=["PUT"])
@jwt_required()
def update_booking(booking_id):
    """Update an existing booking"""
    user_id = get_jwt_identity()
    data = request.json
    response = BookingService.update_bookings(booking_id, data, user_id)
    return response, 200


@bookings_bp.route("/bookings/<booking_id>", methods=["DELETE"])
@jwt_required()
def delete_booking(booking_id):
    """Delete a booking by ID"""
    user_id = get_jwt_identity()
    response = BookingService.delete_booking(booking_id, user_id)
    return response, 200 if "message" in response else 404


@bookings_bp.route("/bookings", methods=["GET"])
@jwt_required()
def list_bookings():
    """List all bookings for the authenticated user"""
    user_id = get_jwt_identity()
    response = BookingService.list_bookings_by_user(user_id)
    return {"bookings": response}


@bookings_bp.route("/bookings/all", methods=["GET"])
@jwt_required()
def list_all_bookings():
    """List all bookings for all users"""
    # check for filters
    date = request.args.get("date")
    status = request.args.get("status")
    if date:
        response = BookingService.list_all_bookings_by_date(date)
        print(response)
        return {"bookings": response}
    if status:
        response = BookingService.list_all_bookings_by_status(status)
        print(response)
        return {"bookings": response}
    response = BookingService.list_all_bookings()
    print(response)
    return {"bookings": response}
