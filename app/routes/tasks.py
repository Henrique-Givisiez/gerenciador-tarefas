from flask import Blueprint, request, jsonify
from database.database import Database

tasks_bp = Blueprint("tasks_bp", __name__)

database = Database()


# Create task route
@tasks_bp.route("/create", methods=['POST'])
def create_task():
    data = request.json
    task_id = database.tasks.create(data["user_id"], data["task_category"], data["task_description"], data["task_date"], data["task_status"])
    return jsonify(task_id) if task_id else ("", 404)

# Read task details route
@tasks_bp.route("/read/<int:user_id>", methods=["GET"])
def read_all_tasks(user_id: int):
    task_data = database.tasks.read(user_id)
    return jsonify(task_data) if task_data else ("", 404)

# Update task route
@tasks_bp.route("/update/<int:task_id>", methods=["PUT"])
def update_task(task_id: int):
    data = request.json
    success = database.tasks.update(task_id, data["new_category"], data["new_description"], data["new_date"], data["new_status"])
    return jsonify({"success": success}), (201 if success else 400)

# Delete task route
@tasks_bp.route("/delete/<int:task_id>", methods=['DELETE'])
def delete_task(task_id: int):
    success = database.tasks.delete(task_id)
    return jsonify({"success": success}), (201 if success else 400)
