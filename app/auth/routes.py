from flask import Blueprint, redirect, url_for, request, render_template, session
from app.database.database import Database

database = Database()

auth_bp = Blueprint("auth", __name__)

loggedin = False

@auth_bp.route("/")
def index():
    return redirect(url_for("signup"))


@auth_bp.route("/signup", methods = ["GET", "POST"])
def signup():
    msg = ""
    if request.method == "POST":   
        success, msg = database.accounts.create(username = request.form.get("username"), email = request.form.get("email"), password = request.form.get("password"))
        if success:
            session["msg_signup_success"] = msg
            return redirect(url_for("login"))
        
    return render_template("signup.html", msg=msg)


@auth_bp.route("/login", methods = ["GET", "POST"])
def login():

    global loggedin

    msg_signup_success = session["msg_signup_success"]
    session["msg_signup_success"] = ""
    
    if request.method == "POST":
        user_id, msg, success = database.accounts.check_auth(email=request.form.get("email"), password=request.form.get("password"))
        if success:
            loggedin = True
            session['id'] = user_id
            session["msg_login_success"] = msg
            return redirect(url_for(f"homepage"))
    
    return render_template("login.html", msg=msg_signup_success)


@auth_bp.route("/homepage", methods = ["GET"])
def homepage():
    global loggedin

    if loggedin:
        msg_login_success = session["msg_login_success"]
        return render_template("home.html", msg=msg_login_success)
    
    return render_template("login.html", msg="Usuário não logado!")


@auth_bp.route("sobre-o-criador", methods = ["GET"])
def criador_page():
    global loggedin

    if loggedin:
        return render_template("criador_page.html")

    return render_template("login.html", msg="Usuário não logado!")