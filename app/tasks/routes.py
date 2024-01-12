from flask import Blueprint, redirect, url_for, request, render_template, session
from app.database.database import Database
from app.auth.routes import loggedin
database = Database()

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/create-task", methods = ["POST"])
def createTask():

    result = database.tasks.create(user_id=session["id"], task_type=request.form.get("task_type"), 
                                   task_description=request.form.get("task_description"), task_date=request.form.get("task_date"))
    if result[0]:
        
