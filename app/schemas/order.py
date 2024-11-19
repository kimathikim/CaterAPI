# schemas/order.py

from marshmallow import Schema, fields

class OrderSchema(Schema):
    id = fields.String(dump_only=True)
    user_id = fields.String(required=True)
    service_id = fields.String(required=True)
    guest_count = fields.Integer(required=True)
    notes = fields.String(allow_none=True)
    status = fields.String(dump_only=True, default="Pending")
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)

