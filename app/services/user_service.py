from werkzeug.security import check_password_hash
from app.models import storage
from app.models.user import Users


class UserService:
    @staticmethod
    def get_user(user_id):
        """Retrieve a user by their ID"""
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
    def update_user(user_id, data):
        """Update user information"""
        user = storage.get(Users, user_id)
        if not user:
            return {"error": "User not found"}

        user = storage.update(user, data)
        return {"user": UserService.get_user(user_id)}

    @staticmethod
    def delete_user(user_id):
        """Delete a user"""
        user = storage.get(Users, user_id)
        if not user:
            return {"error": "User not found"}

        storage.delete(user)
        storage.save()

        return {"message": "User deleted successfully"}

    @staticmethod
    def list_users():
        """List all users"""
        users = storage.all(Users)
        user_list = []
        for user in users:
            user_list.append(
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at,
                }
            )

        return user_list

    @staticmethod
    def verify_user(email, password):
        """Verify user's email and password"""
        user = storage.get_by_email(Users, email)
        if user and check_password_hash(user.password, password):
            return {
                "user_id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
            }
        return {"error": "Invalid credentials"}
