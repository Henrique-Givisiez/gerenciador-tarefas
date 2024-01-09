from flask import Flask, render_template, request
from hashlib import sha256
from conn_database import get_db_connection
from accounts import Accounts
from tasks import Tasks
# Cria um app com o Flask
app = Flask(__name__)

# Cria uma chave secreta e criptografa
secret_key = 'Luco@1504'
app.secret_key = sha256(secret_key.encode()).hexdigest()

# Cria os parâmetros para a configuração do app
host = 'localhost'
user = 'root'
password = 'mypassword'
port = "5500"

app.config['MYSQL_HOST'] = host
app.config['MYSQL_PORT'] = port
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = password

# Faz a conexão com a database
conn = get_db_connection()

account = Accounts()
task = Tasks()

@app.route("/")
def init():
    return render_template("signup.html")

@app.route("/signup", methods = ["POST"])
def create_user():
    msg = ""
    
    data = request.json
    
    success, msg = account.create(username = data["username"], email = data["email"], password = data["password"])

    if success:
        return render_template("login.html", msg=msg)
    
    return render_template("signup.html", msg=msg)
        


if __name__ == "__main__":
    app.run(debug=True)
