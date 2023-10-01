from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL 
import MySQLdb.cursors
import re 
from time import sleep
app = Flask(__name__)

app.secret_key = 'givisiez'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Luco@1504'
app.config['MYSQL_DB'] = 'gerenciador_tarefas_contas'

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("registrar.html")

@app.route('/logout') 
def logout(): 
    session.pop('loggedin', None) 
    session.pop('id', None) 
    session.pop('username', None) 
    return redirect(url_for('login')) 

@app.route("/login", methods = ['POST','GET'])
def login():
    msg = ''
    msg_erro='Insira suas credenciais!'
    if request.method == 'POST' and 'email' in request.form and 'senha' in request.form: 
        email = request.form['email'] 
        senha = request.form['senha'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM contas WHERE email = % s AND senha = % s', (email, senha, )) 
        conta = cursor.fetchone() 
        if conta: 
            session['loggedin'] = True
            session['id'] = conta['id'] 
            session['email'] = conta['email'] 
            msg = 'Bem vindo!'
            return render_template('home.html', msg = msg) 
        else: 
            msg_erro = 'Credenciais inválidas, tente novamente!'
    return render_template('login.html', msg_erro = msg_erro) 
    
@app.route('/register', methods =['GET', 'POST']) 
def register(): 
    msg = '' 
    if request.method == 'POST' and 'usuario' in request.form and 'senha' in request.form and 'email' in request.form : 
        usuario = request.form['usuario'] 
        senha = request.form['senha'] 
        email = request.form['email'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM contas WHERE usuario = % s', (usuario, )) 
        account = cursor.fetchone() 
        if account: 
            msg = 'Essa conta já exisste!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
            msg = 'Endereço de email inválido!'
        elif not re.match(r'[A-Za-z0-9]+', usuario): 
            msg = 'Usuário só deve conter números e letras!'
        elif not usuario or not senha or not email: 
            msg = 'Por favor, preencha os campos!'
        else: 
            cursor.execute('INSERT INTO contas VALUES (NULL, % s, % s, % s)', (usuario, senha, email, )) 
            mysql.connection.commit() 
            msg = 'Conta criada com sucesso! Insira seus dados no campo de login para entrar.'
            sleep(0.5)
            return render_template('login.html', msg = msg) 
    elif request.method == 'POST': 
        msg = 'Por favor, preencha os campos!'
    return render_template('registrar.html', msg=msg)

@app.route("/tarefas")
def tarefas():
    return render_template("tarefas.html")

if __name__ == "__main__":
    app.run(debug=True)