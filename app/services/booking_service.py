from app.models import storage
from app.models.booking import Booking
from app.models.user import Users


class BookingService:
    @staticmethod
    def create_booking(data):
        """Create a new booking"""
        try:
            services = data.get("services", [])
            if not services:
                return {"error": "Missing services"}

            total_cost = sum(
                service["price"] * service.get("quantity", 1) for service in services
            )

            booking_data = {
                "user_id": data["user_id"],
                "services": services,
                "event_name": data.get("event_name"),
                "event_date": data["date"],
                "event_time": data["time"],
                "event_location": data["event_location"],
                "guest_count": data["guest_count"],
                "special_instructions": data.get("special_instructions"),
                "total_cost": total_cost,
            }
            print(booking_data)
            booking = Booking(**booking_data)
            booking.save()
            return {"message": "Booking created successfully", "booking_id": booking.id}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_booking(booking_id, user_id):
        """Get booking details by ID for authenticated user"""
        booking = storage.get(Booking, booking_id)
        if not booking or booking.user_id != user_id:
            return {"error": "Booking not found or access denied"}

        return booking.to_dicto()

    @staticmethod
    def update_bookings(booking_id, data, user_id):
        """Update an existing booking"""
        booking = storage.get(Booking, booking_id)
        user = storage.get(Users, user_id)
        if user:
            data["manager_id"] = (user_id,)
            data["manager_name"] = user.name

        if not booking:
            return {"error": "Booking not found or access denied!!!!"}
        try:
            booking = storage.update(booking, data)
            if not booking:
                return {"error": "Booking update failed"}
            return {
                "message": "Booking updated successfully",
                "booking": booking.to_dicto(),
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_booking(booking_id, user_id):
        """Delete a booking by ID for authenticated user"""
        booking = storage.get(Booking, booking_id)
        if not booking or booking.user_id != user_id:
            return {"error": "Booking not found or access denied"}

        storage.delete(booking)
        return {"message": "Booking deleted successfully"}

    @staticmethod
    def list_bookings_by_user(user_id):
        """List bookings for a specific authenticated user"""
        user = storage.get(Users, user_id)
        if not user:
            return {"error": "User not found"}, 404
        if not user.bookings:
            return {"message": "No bookings found"}, 200
        return [booking.to_dicto() for booking in user.bookings], 200

    @staticmethod
    def list_all_bookings():
        """List all bookings for all users"""
        bookings = storage.all(Booking)
        if not bookings:
            return {"message": "No bookings found"}, 200
        return [booking.to_dicto() for booking in bookings], 200

    @staticmethod
    def list_all_bookings_by_date(date):
        """List all bookings by date"""
        bookings = storage.all(Booking)
        if not bookings:
            return {"message": "No bookings found"}, 200
        return [
            booking.to_dicto() for booking in bookings if booking.event_date == date
        ], 200

    @staticmethod
    def list_all_bookings_by_status(status):
        """List all bookings by status"""
        bookings = storage.all(Booking)
        if not bookings:
            return {"message": "No bookings found"}, 200
        return [
            booking.to_dicto() for booking in bookings if booking.status == status
        ], 200
