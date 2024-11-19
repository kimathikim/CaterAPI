# schemas/user.py

from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1))
    email = fields.String(required=True, validate=validate.Email())
    password = fields.String(
        load_only=True, required=True, validate=validate.Length(min=6)
    )
    role = fields.String(
        required=True, validate=validate.OneOf(["Client", "Catering Manager"])
    )
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
