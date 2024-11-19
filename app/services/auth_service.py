from datetime import timedelta
from app.models import storage
from app.models.user import Users
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash


def hash_password(password):
    """Hashes the user password"""
    return generate_password_hash(password)


class AuthService:
    @staticmethod
    def register(data):
        """Handles user registration"""
        email = data.get("email")
        existing_user = storage.get_by_email(Users, email)

        if existing_user:
            return {"error": "User with this email already exists."}, 409

        try:
            data["password"] = hash_password(data["password"])
            user = Users(**data)
            user.save()
            return {"id": user.id, "email": user.email, "role": user.role}, 201
        except Exception as e:
            return {"error": str(e)}, 404

    @staticmethod
    def login(data):
        """Handles user login and token generation"""
        email = data.get("email")
        password = data.get("password")

        user = storage.get_by_email(Users, email)

        if not user or not check_password_hash(user.password, password):
            return {"error": "Invalid credentials"}

        access_token = create_access_token(
            identity=user.id, expires_delta=timedelta(hours=1)
        )

        return {"access_token": access_token, "user_role": user.role}

    @staticmethod
    def get_user_by_id(user_id):
        """Retrieves a user by their ID"""
        user = storage.get(Users, user_id)
        if not user:
            return {"error": "User not found"}

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }
    @staticmethod
    def check_for_errors(data):
        """Checks for any errors in the provided data"""
        errors = {}

        if not data.get("email"):
            errors["email"] = "Email is required"
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", data.get("email")):
            errors["email"] = "Invalid email format"

        if not data.get("password"):
            errors["password"] = "Password is required"
        elif len(data.get("password")) < 8:
            errors["password"] = "Password must be at least 8 characters long"

        if not data.get("name"):
            errors["name"] = "Name is required"

        if errors:
            return {"errors": errors}, 400
        return None
