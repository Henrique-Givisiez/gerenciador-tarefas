from flask import Flask, render_template, request, redirect, url_for, session, redirect, jsonify
from flask_mysqldb import MySQL 
import MySQLdb.cursors
import re 

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
            return render_template('login.html', msg = msg) 
    elif request.method == 'POST': 
        msg = 'Por favor, preencha os campos!'
    return render_template('registrar.html', msg=msg)

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



@app.route("/homepage", methods =['GET','POST'])
def homepage():
    if logado:
        if request.method == 'GET':
            inicializaTarefas()
        return render_template("home.html")
    return redirect(url_for('login'))

@app.route("/inicializa-tarefas")
def inicializaTarefas():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM tarefas WHERE usuario_id = %s", (session['id'], ))
    data_user_tarefas = cursor.fetchall()
    tarefas_do_usuario = {}
    for indice, tarefa_tupla in enumerate(data_user_tarefas):
        dict_tarefa = {
            "categoria": tarefa_tupla["nome_tarefa"],
            "descricao": tarefa_tupla["descricao_tarefa"],
            "data": tarefa_tupla["data_tarefa"].strftime("%d/%m/%y"),
            "ID": tarefa_tupla['id']
        }
        tarefas_do_usuario["tarefa_"+str(indice)] = dict_tarefa
    return jsonify(tarefas_do_usuario)

@app.route("/adiciona-tarefa", methods=['POST'])
def adicionaTarefa():
    if request.method == 'POST':
        nome_tarefa = request.form.get("nomeTarefa")
        descricao_tarefa = request.form.get("descricaoTarefa")
        data_tarefa = request.form.get("data")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM tarefas WHERE nome_tarefa = % s', (nome_tarefa, )) 
        tarefa_bd = cursor.fetchone() 

        if not tarefa_bd: 
            cursor.execute('INSERT INTO tarefas VALUES (NULL, % s, %s, %s, %s)', (session['id'], nome_tarefa, descricao_tarefa, data_tarefa, )) 
            mysql.connection.commit()
            tarefa_submetida = {
                "categoria": nome_tarefa,
                "descricao": descricao_tarefa,
                "data": data_tarefa,
                "ID": cursor.lastrowid
                }
            return jsonify(tarefa_submetida)
            
@app.route("/editar-tarefa", methods=['POST'])
def editarTarefa():
    if request.method == 'POST':
        # Busca o id da tarefa a ser editada o qual será enviado pelo javascript
        id_tarefa_editada = request.form.get('id_tarefa_editada')

        # Busca os novos valores do formulário
        nova_categoria_tarefa = request.form.get('nova_tarefa')
        nova_descricao_tarefa = request.form.get('nova_descricao_tarefa')
        nova_data_tarefa = request.form.get("nova_data")

        # Conecta ao BD e faz as alterações necessárias para alterar tabela contendo as tarefas a serem editadas
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            # Atualiza a tabela tarefas com os novos valores atualizados 
            cursor.execute('UPDATE tarefas SET nome_tarefa=%s,descricao_tarefa=%s,data_tarefa=%s WHERE id=%s',(nova_categoria_tarefa, nova_descricao_tarefa, nova_data_tarefa, id_tarefa_editada, ))
            mysql.connection.commit()
            nova_tarefa = {
                "novaCategoria": nova_categoria_tarefa,
                "novaDescricao": nova_descricao_tarefa,
                "novaData": nova_data_tarefa,
                "id": id_tarefa_editada
            }
            return jsonify(nova_tarefa)
        except Exception as error:
            mysql.connection.rollback()
            return jsonify({'error': str(error)}), 500
        finally:
            cursor.close()
            
@app.route("/excluir-tarefa", methods=['POST'])
def excluirTarefa():
    id_tarefa_excluida = request.form.get("tarefa_excluida")
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("DELETE FROM tarefas WHERE id= %s", (id_tarefa_excluida, ))
        mysql.connection.commit()
        return jsonify({"message": "Tarefa excluída com sucesso"})
    except Exception as error:
        mysql.connection.rollback()
        return jsonify({"error": str(error)}), 500
    finally:
        cursor.close()
        
@app.route("/sobre-o-criador")
def sobreMim():
    if logado:
        return render_template("sobre-o-criador.html")
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)