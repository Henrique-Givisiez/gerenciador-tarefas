from flask import Flask, render_template, request, flash, redirect, url_for
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

loggedin = False

@app.route("/")
def init():
    return redirect(url_for("signup"))


@app.route("/signup", methods = ["GET", "POST"])
def signup():
    msg = ""
    if request.method == "POST":   
        success, msg = database.accounts.create(username = request.form.get("username"), email = request.form.get("email"), password = request.form.get("password"))
        if success:
            return redirect(url_for("login"))
        
    return render_template("signup.html", msg=msg)
        

@app.route("/login", methods = ["GET", "POST"])
def login():
    global loggedin

    msg = ""
    
    if request.method == "POST":
        data = request.json
        success, msg = database.accounts.check_auth(email=data["email"], password=data["password"])
        
        if success:
            loggedin = True
            flash(msg)
            return redirect(url_for("homepage"))    
        
    return render_template("login.html", msg=msg)




if __name__ == "__main__":
    app.run(debug=True)
