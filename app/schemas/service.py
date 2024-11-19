# schemas/service.py

from marshmallow import Schema, fields

class ServiceSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    price = fields.Float(required=True)
    availability = fields.Boolean(required=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)

