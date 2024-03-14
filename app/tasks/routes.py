from flask import Blueprint, jsonify, request, render_template, session
from database.database import Database
from permissions_decorator import requires_login

database = Database()

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/create-task", methods = ["POST"])
@requires_login()
def createTask():
    data = request.form.to_dict()
    result = database.tasks.create(user_id=session["id"], task_type=data["task_type"], 
                                   task_description=data["task_description"], task_date=data["task_date"])
    success = result[0]
    if success:
        tasks_data = result[1]
        return jsonify(tasks_data)
    
    msg = result[1]
    return render_template("homepage.html", msg=msg)


@tasks_bp.route("/homepage/read-tasks", methods=["GET"])
@requires_login()
def readTasks():
    user_id = session["id"]
    result = database.tasks.read(user_id=user_id)
    success = result[0]
    if success:
        task_json = result[1]
        return jsonify(task_json)
    
    msg = result[1]
    return render_template("homepage.html", msg=msg)


@tasks_bp.route("/update-task", methods=["PUT"])
@requires_login()
def updateTask():
    data = request.form.to_dict()
    result = database.tasks.update(task_id=data["task_id"], new_task_type=data["new_task_type"], new_task_descriprion=data["new_task_description"],
                                   new_task_date=data["new_task_date"], new_task_status=data["new_task_status"])
    success = result[0]                                   
    if success:
        return success
    msg = result[1]
    return render_template("homepage.html", msg=msg)


@tasks_bp.route("/delete-task/<task_id>", methods=["DELETE"])
@requires_login()
def deleteTask(task_id: int):
    result = database.tasks.delete(task_id=task_id)
    success = result[0]
    if success:
        return success
    msg = result[1]
    return render_template("homepage.html", msg=msg)
    