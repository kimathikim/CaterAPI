from app.models.order import Order
from app.models import storage
from app.schemas.order import OrderSchema


class OrderService:
    @staticmethod
    def create_order(data):
        """Create a new order"""
        schema = OrderSchema()
        errors = schema.validate(data)
        if errors:
            return {"status": "failure", "errors": errors}, 400

        order = Order(**data)
        order.save()

        return {
            "status": "success",
            "message": "Order created successfully",
            "order": schema.dump(order),
        }, 201

    @staticmethod
    def list_orders_by_user(user_id):
        """List all orders for a specific user"""
        orders = storage.search(Order, {"user_id": user_id})
        schema = OrderSchema(many=True)
        return {
            "orders": schema.dump(orders),
            "status_code": 200,
        }

    @staticmethod
    def change_order_status(order_id, status, user_id):
        """Change the status of an order"""
        order = storage.get(Order, order_id)
        if not order or order.user_id != user_id:
            return {
                "status": "failure",
                "message": "Order not found or access denied",
            }, 404

        order.status = status
        order.save()
        return {
            "status": "success",
            "message": "Order status updated successfully",
        }, 200

    @staticmethod
    def get_order_by_id(order_id, user_id):
        """Retrieve an order by ID"""
        order = storage.get(Order, order_id)
        if not order or order.user_id != user_id:
            return {
                "status": "failure",
                "message": "Order not found or access denied",
            }, 404

        schema = OrderSchema()
        return {
            "status": "success",
            "order": schema.dump(order),
            "status_code": 200,
        }

    @staticmethod
    def update_order(order_id, data, user_id):
        """Update an existing order"""
        order = storage.get(Order, order_id)
        if not order or order.user_id != user_id:
            return {
                "status": "failure",
                "message": "Order not found or access denied",
            }, 404

        updated_order = storage.update(order, data)
        schema = OrderSchema()
        return {
            "status": "success",
            "message": "Order updated successfully",
            "order": schema.dump(updated_order),
        }, 200

    @staticmethod
    def delete_order(order_id, user_id):
        """Delete an order by ID"""
        order = storage.get(Order, order_id)
        if not order or order.user_id != user_id:
            return {
                "status": "failure",
                "message": "Order not found or access denied",
            }, 404

        storage.delete(order)
        return {"status": "success", "message": "Order deleted successfully"}, 200
