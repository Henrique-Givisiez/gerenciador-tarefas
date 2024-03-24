from flask import Blueprint, redirect, url_for, request, render_template, session
from database.database import Database

database = Database()

auth_bp = Blueprint("auth", __name__)

logado = False

@auth_bp.route("/")
def index():
    return redirect(url_for("auth.signup"))


@auth_bp.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        success, msg= database.accounts.create(username = request.form.get("username"), email = request.form.get("email"), password = request.form.get("password"))
        if success:
            return redirect(url_for("auth.login"))
        else:
            return msg
        
    return render_template("signup.html")


@auth_bp.route("/login", methods = ["GET", "POST"])
def login():
    global logado

    if request.method == "POST":
        user_id, msg, success = database.accounts.check_auth(email=request.form.get("email"), password=request.form.get("password"))
        if success:
            session['id'] = user_id
            logado = True
            return redirect(url_for(f"auth.homepage"))

        else:
            return msg
        
    return render_template("login.html")


@auth_bp.route("/logout", methods = ["POST"])
def logout():   
    global logado
    try:
        user_id = session["id"]
        if user_id and logado:
            session["id"] = None
            logado = False
            return redirect(url_for(f"auth.signup"))
        
        return redirect(url_for(f"auth.login"))
    
    except Exception as error:
        return f"Ocorreu um erro: {error}"


@auth_bp.route("/homepage", methods = ["GET"])
def homepage():
    global logado
    if logado:
        return render_template("homepage.html")

    return redirect(url_for(f"auth.login"))


@auth_bp.route("/sobre-o-criador", methods = ["GET"])
def criadorPage():
    global logado
    if logado:
        return render_template("sobre-o-criador.html")

    return redirect(url_for(f"auth.login"))
