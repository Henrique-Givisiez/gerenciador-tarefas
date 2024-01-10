from flask import Flask, render_template, request, flash, redirect, url_for, g, make_response
from hashlib import sha256
from conn_database import Database

# Cria um app com o Flask
app = Flask(__name__)

# Cria uma chave secreta e criptografa
secret_key = 'Luco@1504'
app.secret_key = sha256(secret_key.encode()).hexdigest()

# Cria os parâmetros para a configuração do app
host = 'localhost'
user = 'root'
password = 'mypassword'
port = "5000"

app.config['MYSQL_HOST'] = host
app.config['MYSQL_PORT'] = port
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = password


database = Database()

@app.before_request
def load_user():
    user_id = request.headers.get('X-User-Id')
    if user_id:
        user = database.accounts.read(user_id)
        g.user = user
    else:
        g.user = None

@app.route("/")
def init():
    return redirect(url_for("signup"))


@app.route("/signup", methods = ["GET", "POST"])
def signup():
    msg = ""
    if request.method == "POST":   
        success, msg = database.accounts.create(username = request.form.get("username"), email = request.form.get("email"), password = request.form.get("password"))
        if success:
            flash(msg)
            return redirect(url_for("login"))
        
    return render_template("signup.html", msg=msg)
        

@app.route("/login", methods = ["GET", "POST"])
def login():


    msg = ""
    
    if request.method == "POST":
        user_id, success, msg = database.accounts.check_auth(email=request.form.get("email"), password=request.form.get("password"))
        
        if success:
            response = make_response("user_loggedin")
            response.headers["X-User-Id"] = str(user_id)
            flash(msg)
            return redirect(url_for("homepage")), response    
        
    return render_template("login.html", msg=msg)


@app.route("/homepage", methods = ["GET"])
def homepage():
    if g.user:
        return render_template("home.html", msg=g.user)
    flash("Você precisa estar logado!")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
