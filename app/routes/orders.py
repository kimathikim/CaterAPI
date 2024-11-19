from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.services.order_service import OrderService

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/orders", methods=["POST"])
@jwt_required()
def create_order():
    """Create a new order"""
    data = request.json
    user_id = get_jwt_identity()
    if not data:
        return {"error": "Invalid data provided"}, 400
    data["user_id"] = user_id  # Add authenticated user's ID to the order data
    response = OrderService.create_order(data)
    return response


@orders_bp.route("/orders/<order_id>", methods=["GET"])
@jwt_required()
def get_order(order_id):
    """Get an order by ID"""
    user_id = get_jwt_identity()
    response = OrderService.get_order_by_id(order_id, user_id)
    return response


@orders_bp.route("/orders/<order_id>", methods=["PUT"])
@jwt_required()
def update_order(order_id):
    """Update an existing order"""
    user_id = get_jwt_identity()
    data = request.json
    response = OrderService.update_order(order_id, data, user_id)
    return response


@orders_bp.route("/orders/<order_id>", methods=["DELETE"])
@jwt_required()
def delete_order(order_id):
    """Delete an order"""
    user_id = get_jwt_identity()
    response = OrderService.delete_order(order_id, user_id)
    return response


@orders_bp.route("/orders", methods=["GET"])
@jwt_required()
def list_orders():
    """List all orders for the authenticated user"""
    user_id = get_jwt_identity()
    response = OrderService.list_orders_by_user(user_id)
    return response


@orders_bp.route("/orders/<order_id>/status", methods=["PATCH"])
@jwt_required()
def change_order_status(order_id):
    """Change the status of an order"""
    user_id = get_jwt_identity()
    data = request.json
    if not data or not data.get("status"):
        return {"error": "Missing required field: status"}, 400

    response = OrderService.change_order_status(order_id, data.get("status"), user_id)
    return response
