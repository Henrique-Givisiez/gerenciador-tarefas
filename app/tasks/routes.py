from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for
from database.database import Database
from auth.routes import logado

database = Database()

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/create-task", methods = ["POST"])
def createTask():
    if session["id"]:
        data = request.form.to_dict()
        result = database.tasks.create(user_id=session["id"], task_type=data["task_type"], 
                                    task_description=data["task_description"], task_date=data["task_date"])
        success = result[0]
        if success:
            tasks_data = result[1]
            return jsonify(tasks_data)
        
        msg = result[1]
        return render_template("homepage.html", msg=msg)

    return redirect(url_for(f"auth.login"))


@tasks_bp.route("/homepage/read-tasks", methods=["GET"])
def readTasks():
    if session["id"]:
        user_id = session["id"]
        result = database.tasks.read(user_id=user_id)
        success = result[0]
        if success:
            task_json = result[1]
            return jsonify(task_json)
        
        msg = result[1]
        return render_template("homepage.html", msg=msg)
    
    return redirect(url_for(f"auth.login"))


@tasks_bp.route("/update-task", methods=["PUT"])
def updateTask():
    data = request.form.to_dict()
    result = database.tasks.update(data=data)
    success = result[0]                                   
    msg = result[1]
    if success:
        print(msg)
        
    return render_template("homepage.html", msg=msg)


@tasks_bp.route("/delete-task/<task_id>", methods=["DELETE"])
def deleteTask(task_id: int):
    result = database.tasks.delete(task_id=task_id)
    success = result[0]
    if success:
        return success
    msg = result[1]
    return render_template("homepage.html", msg=msg)
    