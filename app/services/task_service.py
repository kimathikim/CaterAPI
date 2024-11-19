# services/task_service.py

from app.models.task import Task
from app.models import storage

class TaskService:

    @staticmethod
    def create_task(data):
        """Create a new task for catering staff"""
        try:
            task = Task(**data)
            storage.new(task)
            storage.save()
            return {"message": "Task created successfully", "task_id": task.id}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_task(task_id):
        """Get task details by ID"""
        task = storage.get(Task, task_id)
        if not task:
            return {"error": "Task not found"}

        return task.to_dict()

    @staticmethod
    def update_task(task_id, data):
        """Update an existing task"""
        task = storage.get(Task, task_id)
        if not task:
            return {"error": "Task not found"}

        try:
            task = storage.update(task, data)
            return {"message": "Task updated successfully"}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_task(task_id):
        """Delete a task by ID"""
        task = storage.get(Task, task_id)
        if not task:
            return {"error": "Task not found"}

        try:
            storage.delete(task)
            storage.save()
            return {"message": "Task deleted successfully"}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def list_tasks():
        """List all tasks"""
        tasks = storage.all(Task)
        return [task.to_dict() for task in tasks]

    @staticmethod
    def assign_task(task_id, caterer_id):
        """Assign a task to a specific caterer"""
        task = storage.get(Task, task_id)
        if not task:
            return {"error": "Task not found"}

        try:
            task.caterer_id = caterer_id
            storage.save()
            return {"message": f"Task assigned to caterer {caterer_id} successfully"}
        except Exception as e:
            return {"error": str(e)}

