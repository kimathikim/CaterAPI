from marshmallow import Schema, fields


class BookingSchema(Schema):
    id = fields.String(dump_only=True)
    user_id = fields.String(required=True)
    services = fields.List(fields.String(), required=True)  # List of services
    event_name = fields.String(required=False)
    event_date = fields.DateTime(required=True)
    event_time = fields.Time(required=True)
    event_location = fields.String(required=True)
    guest_count = fields.Integer(required=True)
    special_instructions = fields.String(allow_none=True)
    status = fields.String(dump_only=True, default="Pending")
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
