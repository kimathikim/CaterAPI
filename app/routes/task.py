# routes/tasks.py

from flask import Blueprint, request
from app.services.task_service import TaskService

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
    """Create a new task for a caterer"""
    data = request.json
    if not data or not data.get("assignee_id") or not data.get("description") or not data.get("due_date"):
        return {"error": "Missing required fields: assignee_id, description, due_date"}, 400

    response = TaskService.create_task(
        assignee_id=data["assignee_id"],
        description=data["description"],
        due_date=data["due_date"]
    )
    return response, 201

@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    """Get all tasks or filter by assignee_id"""
    assignee_id = request.args.get("assignee_id")
    tasks = TaskService.get_tasks(assignee_id=assignee_id)
    return {"tasks": tasks}, 200

@tasks_bp.route("/tasks/<string:task_id>", methods=["PUT"])
def update_task(task_id):
    """Update a task"""
    data = request.json
    if not data:
        return {"error": "Missing data for updating task"}, 400

    response = TaskService.update_task(task_id, data)
    return response, 200 if "error" not in response else 404

@tasks_bp.route("/tasks/complete/<string:task_id>", methods=["PUT"])
def complete_task(task_id):
    """Mark a task as completed"""
    response = TaskService.complete_task(task_id)
    return response, 200 if "error" not in response else 404

