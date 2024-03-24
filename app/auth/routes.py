from flask import Blueprint, redirect, url_for, request, render_template, session  # Importa os módulos necessários do Flask
from database.database import Database  # Importa a classe Database do módulo database.database

database = Database()  # Cria uma instância da classe Database

auth_bp = Blueprint("auth", __name__)  # Cria um blueprint chamado "auth"

logado = False  # Variável global para controlar o status de login

@auth_bp.route("/")
def index():
    return redirect(url_for("auth.signup"))  # Redireciona para a rota de cadastro

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        success, msg = database.accounts.create(username=request.form.get("username"), email=request.form.get("email"), password=request.form.get("password"))
        if success:
            return redirect(url_for("auth.login"))  # Redireciona para a página de login após o cadastro bem-sucedido
        else:
            return msg  # Retorna uma mensagem de erro em caso de falha no cadastro
        
    return render_template("signup.html")  # Renderiza o template de cadastro

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    global logado

    if request.method == "POST":
        user_id, msg, success = database.accounts.check_auth(email=request.form.get("email"), password=request.form.get("password"))
        if success:
            session['id'] = user_id  # Define a sessão com o ID do usuário autenticado
            logado = True  # Define logado como True
            return redirect(url_for("auth.homepage"))  # Redireciona para a página inicial após o login bem-sucedido
        else:
            return msg  # Retorna uma mensagem de erro em caso de falha no login
        
    return render_template("login.html")  # Renderiza o template de login

@auth_bp.route("/logout", methods=["POST"])
def logout():   
    global logado
    try:
        user_id = session["id"]  # Obtém o ID do usuário da sessão
        if user_id and logado:
            session["id"] = None  # Remove o ID da sessão
            logado = False  # Define logado como False
            return redirect(url_for("auth.signup"))  # Redireciona para a página de cadastro após o logout
        return redirect(url_for("auth.login"))  # Redireciona para a página de login caso o usuário não esteja logado
    
    except Exception as error:
        return f"Ocorreu um erro: {error}"  # Retorna uma mensagem de erro em caso de exceção

@auth_bp.route("/homepage", methods=["GET"])
def homepage():
    global logado
    if logado:
        return render_template("homepage.html")  # Renderiza a página inicial se o usuário estiver logado
    return redirect(url_for("auth.login"))  # Redireciona para a página de login caso o usuário não esteja logado

@auth_bp.route("/sobre-o-criador", methods=["GET"])
def criadorPage():
    global logado
    if logado:
        return render_template("sobre-o-criador.html")  # Renderiza a página "Sobre o Criador" se o usuário estiver logado
    return redirect(url_for("auth.login"))  # Redireciona para a página de login caso o usuário não esteja logado
