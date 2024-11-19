# schemas/task.py

from marshmallow import Schema, fields

class TaskSchema(Schema):
    id = fields.String(dump_only=True)
    assigned_to = fields.String(required=True)
    task_description = fields.String(required=True)
    due_date = fields.DateTime(required=True)
    status = fields.String(dump_only=True, default="Pending")
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)

