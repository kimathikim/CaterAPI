# routes/user.py

from flask import Blueprint, request
from app.services.user_service import UserService

user_bp = Blueprint("user", __name__)


@user_bp.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """Get a user by ID"""
    response = UserService.get_user(user_id)
    return response, 200 if "id" in response else 404


@user_bp.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """Update a user's information"""
    data = request.json
    response = UserService.update_user(user_id, data)
    return response, 200 if "user" in response else 404


@user_bp.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete a user account"""
    response = UserService.delete_user(user_id)
    return response, 200 if "message" in response else 404


@user_bp.route("/users", methods=["GET"])
def list_users():
    """List all users"""
    response = UserService.list_users()
    return {"users": response}, 200
