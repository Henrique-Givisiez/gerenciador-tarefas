from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for  # Importa os módulos necessários do Flask
from database.database import Database  # Importa a classe Database do módulo database.database

database = Database()  # Cria uma instância da classe Database

tasks_bp = Blueprint("tasks", __name__)  # Cria um blueprint chamado "tasks"

@tasks_bp.route("/create-task", methods=["POST"])
def createTask():
    if session["id"]:  # Verifica se o usuário está logado
        data = request.form.to_dict()  # Obtém os dados do formulário
        result = database.tasks.create(user_id=session["id"], task_type=data["task_type"], 
                                       task_description=data["task_description"], task_date=data["task_date"])  # Cria uma nova tarefa
        success = result[0]  # Indica se a operação foi bem-sucedida
        msg = result[1]  # Mensagem de retorno
        return jsonify({"status": msg, "success": success})  # Retorna um JSON com o status e o sucesso da operação

    return redirect(url_for("auth.login"))  # Redireciona para a rota de login se o usuário não estiver logado

@tasks_bp.route("/homepage/read-tasks", methods=["GET"])
def readTasks():
    if session["id"]:  # Verifica se o usuário está logado
        user_id = session["id"]  # Obtém o ID do usuário
        result = database.tasks.read(user_id=user_id)  # Lê as tarefas do usuário
        success = result[0]  # Indica se a operação foi bem-sucedida
        if success:
            task_json = result[1]  # Obtém as tarefas em formato JSON
            return jsonify(task_json)  # Retorna as tarefas como JSON
        
        msg = result[1]  # Mensagem de erro
        return render_template("homepage.html", msg=msg)  # Renderiza o template da página inicial com a mensagem de erro
    
    return redirect(url_for("auth.login"))  # Redireciona para a rota de login se o usuário não estiver logado

@tasks_bp.route("/update-task", methods=["POST"])
def updateTask():
    data = request.form.to_dict()  # Obtém os dados do formulário
    result = database.tasks.update(data=data)  # Atualiza a tarefa
    success = result[0]  # Indica se a operação foi bem-sucedida
    msg = result[1]  # Mensagem de retorno
    if success:
        return jsonify({"status": msg, "success": success})


@tasks_bp.route("/delete-task", methods=["POST"])
def deleteTask():
    try:
        data = request.form.to_dict()  # Obtém os dados do formulário
        task_id = data["task_id"]  # Obtém o ID da tarefa
        result = database.tasks.delete(task_id=task_id)  # Deleta a tarefa
        success = result[0] # Indica se a operação foi bem-sucedida
        msg = result[1] # Mensagem de retorno
        if success:
            return jsonify({"status": msg, "success": success})
    
    except Exception as err:
        return f"Ocorreu um erro: {err}"