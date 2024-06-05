from flask import Blueprint, redirect, url_for, request, render_template, session, jsonify # Importa os módulos necessários do Flask
from database.database import Database  # Importa a classe Database do módulo database.database

database = Database()  # Cria uma instância da classe Database

auth_bp = Blueprint("auth", __name__)  # Cria um blueprint chamado "auth"


@auth_bp.route("/")
def index():
    return redirect(url_for("auth.signup"))  # Redireciona para a rota de cadastro

@auth_bp.route("/signup", methods=["GET", "POST"])

def signup():
    try:
        if request.method == "POST":
            success, msg = database.accounts.create(username=request.form.get("username"), email=request.form.get("email"), password=request.form.get("password"))
            return jsonify({"success": success, "msg": msg})
        
        return render_template("signup.html")  # Renderiza o template de cadastro
        
    except Exception as err:
        return f"Ocorreu um erro: {err}"
    
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            user_id, msg, success = database.accounts.check_auth(email=request.form.get("email"), password=request.form.get("password"))
            if success:
                session['id'] = user_id  # Define a sessão com o ID do usuário autenticado
            return jsonify({"success": success, "msg": msg}) 
            
        return render_template("login.html")  # Renderiza o template de login

    except Exception as err:
        return f"Ocorre um erro: {err}"
    
@auth_bp.route("/logout", methods=["POST"])
def logout():   
    try:
        try:
            if session["id"]:
                session.pop("id", None)
                return redirect(url_for("auth.signup"))  # Redireciona para a página de cadastro após o logout

        except KeyError:
            return redirect(url_for("auth.login"))  # Redireciona para a página de login caso o usuário não esteja logado
    
    except Exception as error:
        return f"Ocorreu um erro: {error}"  # Retorna uma mensagem de erro em caso de exceção

@auth_bp.route("/homepage", methods=["GET"])
def homepage():
    try:
        if session["id"]:
            return render_template("homepage.html")  # Renderiza a página inicial se o usuário estiver logado
    
    except KeyError:
        return redirect(url_for("auth.login"))  # Redireciona para a página de login caso o usuário não esteja logado

@auth_bp.route("/sobre-o-criador", methods=["GET"])
def criadorPage():
    try:
        if session["id"]:
            return render_template("sobre-o-criador.html")  # Renderiza a página "Sobre o Criador" se o usuário estiver logado

    except KeyError:
        return redirect(url_for("auth.login"))  # Redireciona para a página de login caso o usuário não esteja logado
  