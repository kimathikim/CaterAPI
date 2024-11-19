# schemas/feedback.py

from marshmallow import Schema, fields

class FeedbackSchema(Schema):
    id = fields.String(dump_only=True)
    user_id = fields.String(required=True)
    feedback = fields.String(required=True)
    rating = fields.Float(required=True)
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)

