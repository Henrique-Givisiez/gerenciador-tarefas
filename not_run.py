from flask import Flask, render_template, request, flash, redirect, url_for, session
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
    query_read_tasks_by_user = "SELECT * FROM tarefas WHERE usuario_id = %s"
    database.cursor.execute(query_read_tasks_by_user, (3))
    user_tasks = database.cursor.fetchall()
    dict_tasks = {}
    for task in user_tasks:
        dict_tasks[task[0]] = task 

    print(dict_tasks)
    return "ok"


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

    global loggedin

    msg = ""
    
    if request.method == "POST":
        user_id, msg, success = database.accounts.check_auth(email=request.form.get("email"), password=request.form.get("password"))
        if success:
            loggedin = True
            session['id'] = user_id
            return render_template("home.html", msg=msg)
    
    return render_template("login.html", msg=msg)



@app.route("/homepage", methods = ["GET"])
def homepage():
    if loggedin:
        return render_template("home.html")
    flash("Você precisa estar logado!")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
