from flask import Flask, render_template, request, redirect, url_for, session, redirect
from flask_mysqldb import MySQL 
import MySQLdb.cursors
import re 
from time import sleep
import json

app = Flask(__name__)

app.secret_key = 'givisiez'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Luco@1504'
app.config['MYSQL_DB'] = 'bd_gerenciador_de_tarefas'

mysql = MySQL(app)


logado = False

@app.route("/")
def home():
    return render_template("registrar.html")


@app.route("/login", methods = ['POST','GET'])
def login():
    global logado
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
            session['usuario'] = conta['usuario'] 
            logado = True
            msg = 'Bem vindo!'
            return redirect(url_for('homepage'))
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



@app.route("/sobre-o-criador")
def sobreMim():
    if logado:
        return render_template("sobre-o-criador.html")
    return redirect(url_for('login'))

@app.route("/homepage", methods =['GET','POST'])
def homepage():
    if logado:
        msg=''
        if request.method == 'POST' and 'nomeTarefa' in request.form: 
            nome_tarefa = request.form['nomeTarefa']
            descricao_tarefa = request.form['descricaoTarefa']
            data_tarefa = request.form['data']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
            cursor.execute('SELECT * FROM tarefas WHERE nome_tarefa = % s', (nome_tarefa, )) 
            tarefa_bd = cursor.fetchone() 
            if not tarefa_bd: 
                cursor.execute('INSERT INTO tarefas VALUES (NULL, % s, %s, %s, %s)', (session['id'], nome_tarefa, descricao_tarefa, data_tarefa, )) 
                mysql.connection.commit()
                return retornaTarefa()
            else:
                msg='Essa tarefa já está na sua lista!' 
        return render_template("home.html", msg=msg)
    return redirect(url_for('login'))

def retornaTarefa():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM tarefas WHERE usuario_id = %s", (session['id'], ))
    data_user_tarefas = cursor.fetchall()
    tarefas_dict= {session['usuario']: []}
    for data in data_user_tarefas:
        tarefas_dict[session['usuario']].append([data['nome_tarefa'], data['descricao_tarefa'], (data['data_tarefa']).strftime("%d/%m/%Y")])
    for item in tarefas_dict[session['usuario']]:
        nome_tarefa, descricao_tarefa, data_tarefa = item[0], item[1], item[2]
    return render_template("home.html",nome_tarefa=nome_tarefa, descricao_tarefa=descricao_tarefa, data_tarefa=data_tarefa)

@app.route('/logout') 
def logout(): 
    global logado
    if logado:
        session.pop('loggedin', None) 
        session.pop('id', None) 
        session.pop('username', None) 
        logado = False
        return redirect(url_for('login')) 
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)