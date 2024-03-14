from flask import Blueprint, redirect, url_for, request, render_template, session
from database.database import Database
from permissions_decorator import requires_login
import requests

database = Database()

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def index():
    return redirect(url_for("auth.signup"))


@auth_bp.route("/signup", methods = ["GET", "POST"])
def signup():
    msg = ""
    if request.method == "POST":   
        success, msg = database.accounts.create(username = request.form.get("username"), email = request.form.get("email"), password = request.form.get("password"))
        if success:
            session["msg_signup_success"] = msg
            return redirect(url_for("auth.login"))
        
    return render_template("signup.html", msg=msg)


@auth_bp.route("/login", methods = ["GET", "POST"])
def login():

    msg_signup_success = session["msg_signup_success"]
    session["msg_signup_success"] = ""
    
    if request.method == "POST":
        user_id, msg, success = database.accounts.check_auth(email=request.form.get("email"), password=request.form.get("password"))
        if success:
            url = "http://127.0.0.1.5000/login"
            header = {"User-id": user_id}
            response = requests.get(url=url, headers=header)
            session['id'] = user_id
            session["msg_login_success"] = msg
            return redirect(url_for(f"auth.homepage"))
    
    return render_template("login.html", msg=msg_signup_success)


@auth_bp.route("/logout", methods = ["POST"])
def logout():   
    try:
        user_id = session["id"]
        if user_id:
            session["id"] = None
            return render_template("homepage.html")
    except Exception as error:
        return f"Ocorreu um erro: {error}"


@auth_bp.route("/homepage", methods = ["GET"])
@requires_login()
def homepage():
    msg_login_success = session["msg_login_success"]
    return render_template("homepage.html", msg=msg_login_success)


@auth_bp.route("/sobre-o-criador", methods = ["GET"])
@requires_login()
def criador_page():
    return render_template("criador_page.html")

