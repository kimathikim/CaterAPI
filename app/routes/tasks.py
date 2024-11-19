# routes/tasks.py

from flask import Blueprint, request
from app.services.task_service import TaskService

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task for a caterer"""
    data = request.json
    response = TaskService.create_task(data)
    return response, 201 if "task_id" in response else 400

@tasks_bp.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """Get a task by ID"""
    response = TaskService.get_task(task_id)
    return response, 200 if "id" in response else 404

@tasks_bp.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task"""
    data = request.json
    response = TaskService.update_task(task_id, data)
    return response, 200 if "task" in response else 404

@tasks_bp.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task by ID"""
    response = TaskService.delete_task(task_id)
    return response, 200 if "message" in response else 404

@tasks_bp.route('/tasks', methods=['GET'])
def list_tasks():
    """List all tasks"""
    response = TaskService.list_tasks()
    return {"tasks": response}, 200

@tasks_bp.route('/tasks/<user_id>', methods=['GET'])
def list_tasks_by_user(user_id):
    """List tasks assigned to a specific user"""
    response = TaskService.list_tasks_by_user(user_id)
    return {"tasks": response}, 200

