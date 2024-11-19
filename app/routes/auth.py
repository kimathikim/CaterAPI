# routes/auth.py
from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from app.schemas.user import UserSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError


auth_bp = Blueprint("auth", __name__)

# Endpoint to register a new user
user_schema = UserSchema()


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    print(data)
    if not data:
        return jsonify({"error": "Invalid data provided"}), 400
    try:
        validated_data = user_schema.load(data)
        print(validated_data)
    except ValidationError as err:
        print(err)
        return {"errors": err.messages}, 400

    response = AuthService.register(validated_data)
    return response


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data provided"}), 400

    response = AuthService.login(data)
    if response.get("error"):
        return jsonify(response), 401

    return jsonify(
        {
            "message": "Login successful",
            "access_token": response["access_token"],
            "user_role": response["user_role"],
        }
    ), 200


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    """hello"""
    current_user_id = get_jwt_identity()
    response = AuthService.get_user_by_id(current_user_id)
    if response.get("error"):
        return jsonify(response), 404

    return jsonify({"user": response}), 200
