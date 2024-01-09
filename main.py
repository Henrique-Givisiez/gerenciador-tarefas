# Importação de bibliotecas e módulos necessários
from flask import Flask, render_template, request, redirect, url_for, session, redirect, jsonify
import pymysql
import re 
from hashlib import sha256

# Cria o app
app = Flask(__name__)

# Cria uma chave secreta e criptografa
secret_key = 'Luco@1504'
app.secret_key = sha256(secret_key.encode()).hexdigest()

# Cria os parâmetros de conexão para o pymysql
host = 'localhost'
user = 'root'
password = 'mypassword'
database = 'bd_gerenciador_de_tarefas'

# Cria uma connection com o BD ('bd_gerenciador_de_tarefas')
mysql = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    cursorclass=pymysql.cursors.DictCursor  
)


logado = False

# Rota inicial para a página de cadastro
@app.route("/")
def home():
    return render_template("registrar.html")


# Rota para a página de cadastro
@app.route('/register', methods =['GET', 'POST']) 
def register(): 

    msg = '' 

    # Tratamento de erros
    try:

        with mysql.cursor() as cursor:
            # Recebe um formulário via POST e verifica os valores 
            if request.method == 'POST' and 'usuario' in request.form and 'senha' in request.form and 'email' in request.form : 
                # Guarda os valores do formulário nas variáveis
                usuario = request.form['usuario'] 
                senha = request.form['senha'] 
                email = request.form['email'] 
                
                # Busca se a conta já existe na tabela 'contas' baseado no email 
                query_select_contas = 'SELECT * FROM contas WHERE email = %s'
                cursor.execute(query_select_contas, (email, )) 
                account = cursor.fetchone() 

                if account: 
                    msg = 'Essa conta já existe!'

                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
                    msg = 'Endereço de email inválido!'

                elif not re.match(r'[A-Za-z0-9]+', usuario): 
                    msg = 'Usuário só deve conter números e letras!'

                elif not usuario or not senha or not email: 
                    msg = 'Por favor, preencha os campos!'

                else: 
                    # Encriptografa a senha    
                    senha_criptografada = sha256(senha.encode()).hexdigest()
                    
                    # Insere os valores de cadastro na tabela contas
                    query_insert_contas = "INSERT INTO contas VALUES (%s, %s, %s)"
                    cursor.execute(query_insert_contas, (usuario, senha_criptografada, email, )) 
                    mysql.commit() 

                    msg = 'Conta criada com sucesso! Insira seus dados no campo de login para entrar.'

                    return render_template('login.html') # Carrega a página de login  

            return render_template('registrar.html') # Carrega a página de cadastro
        
    except Exception as e:
        mysql.rollback()
        return f"Ocorreu um erro: {e}"

    finally:
        cursor.close()


# Rota para a página de login
@app.route("/login", methods = ['POST','GET'])
def login():

    global logado

    # Tratamento de erros
    try:

        with mysql.cursor() as cursor:
            # Recebe um formulário via POST e verifica os valores 
            if request.method == 'POST' and 'email' in request.form and 'senha' in request.form: 
                # Guarda os valores recebidos em variáveis
                email = request.form['email'] 
                senha = request.form['senha'] 
                
                # Criptografia da senha
                senha_criptografada = sha256(senha.encode()).hexdigest()

                # Busca os valores recebidos na tabela 'contas' 
                query_select_contas = 'SELECT * FROM contas WHERE email = %s AND senha = %s'
                cursor.execute(query_select_contas, (email, senha_criptografada, )) 
                conta = cursor.fetchone() 

                # Se 'conta' não for nulo, as informações de autenticação são válidas e o usuário é logado
                if conta: 
                    # Cria um objeto session para armazenar os dados do usuário        
                    session['loggedin'] = True
                    session['id'] = conta['id'] 
                    session['email'] = conta['email'] 
                    session['usuario'] = conta['usuario'] 
                    
                    logado = True
                    return redirect(url_for('homepage')) # Carrega a homepage 
                    
        return render_template('login.html') # Carrega a página de login
    
    except Exception as e:
        return f"Ocorreu um erro {e}"
    
    finally:
        cursor.close()


# Rota para o logout do usuário. Acionada por um botão
@app.route('/logout') 
def logout(): 

    global logado
    
    if logado:
        # Exclui os dados do usuário no objeto session    
        session.pop('loggedin', None) 
        session.pop('id', None) 
        session.pop('username', None) 

        logado = False
        
    return redirect(url_for('login')) # Carrega a página de login



# Rota para a página inicial ('homepage')
@app.route("/homepage", methods =['GET','POST'])
def homepage():

    if logado:

        if request.method == 'GET':
            # Chama a função inicializaTarefas() para exibir as tarefas do usuário na UI
            inicializaTarefas()

        return render_template("home.html") # Carrega a página inicial
    
    return redirect(url_for('login')) # Carrega a página de login 


# Rota para função de inicializar as tarefas na UI
@app.route("/inicializa-tarefas")
def inicializaTarefas():

    # Tratamento de erros
    try:

        with mysql.cursor() as cursor:

            # Busca as tarefas associadas ao usuário na tabela 'tarefas'
            query_select_tarefas = "SELECT * FROM tarefas WHERE usuario_id = %s"
            cursor.execute(query_select_tarefas, (session['id'], ))
            tarefas_usuario = cursor.fetchall()

            # Cria um dicionário para guardar as tarefas retornadas e enviar em formato jsonify
            dict_tarefas_usuario = {}

            for indice, tarefa_tupla in enumerate(tarefas_usuario):

                # Cria um dicionário para mapear os atributos de cada tarefa    
                dict_tarefa = {
                    "categoria": tarefa_tupla["nome_tarefa"],
                    "descricao": tarefa_tupla["descricao_tarefa"],
                    "data": tarefa_tupla["data_tarefa"].strftime("%d/%m/%y"),
                    "ID": tarefa_tupla['id']
                }

                # Adiciona cada tarefa mapeada ao dicionário 'dict_tarefas_usuario'
                dict_tarefas_usuario["tarefa_"+str(indice)] = dict_tarefa

            return jsonify(dict_tarefas_usuario)

    except Exception as e:
        return f"Ocorreu um erro: {e}"
    
    finally:
        cursor.close()


# Rota para adicionar as tarefas do usuário 
@app.route("/adiciona-tarefa", methods=['POST'])
def adicionaTarefa():

    # Tratamento de erros
    try:
        with mysql.cursor() as cursor:
                    
            if request.method == 'POST':

                # Guarda os valores do formulário nas variáveis
                nome_tarefa = request.form.get("nomeTarefa")
                descricao_tarefa = request.form.get("descricaoTarefa")
                data_tarefa = request.form.get("data")

                # Insere a tarefa na tabela 'tarefas' 
                # "Session['id']" é utilizado para associar a tarefa àquele usuário por meio de uma FK definida na tabela
                query_insert_tarefas = "INSERT INTO tarefas(usuario_id, nome_tarefa, descricao_tarefa, data_tarefa, status_tarefa) VALUES (%s, %s, %s, %s, 'pendente')"
                cursor.execute(query_insert_tarefas, (session['id'], nome_tarefa, descricao_tarefa, data_tarefa, )) 
                mysql.commit()


                """
                Cria um dicionário 'tarefa_submetida' para armazenar os atributos da tarefa adicionada.
                Esse dicionário será enviado em formato de jsonify para o frontend para tratá-lo de forma
                que seja exibida as tarefas na UI
                """
                tarefa_submetida = {
                    "categoria": nome_tarefa,
                    "descricao": descricao_tarefa,
                    "data": data_tarefa,
                    "status": "pendente",
                    "ID": cursor.lastrowid
                    }
                
                return jsonify(tarefa_submetida)
    
    except Exception as e:
        mysql.rollback()
        return f"Ocorreu um erro: {e}"
    
    finally:
        cursor.close()



# Rota para edição da tarefas
@app.route("/editar-tarefa", methods=['POST'])
def editarTarefa():
        
        # Tratamento de erros
        try:
            with mysql.cursor() as cursor:

                # Recebe um formulário via POST e verifica os valores 
                if request.method == 'POST':

                    # Guarda os valores do formulário nas variáveis
                    id_tarefa_editada = request.form.get('id_tarefa_editada')
                    nova_categoria_tarefa = request.form.get('nova_tarefa')
                    nova_descricao_tarefa = request.form.get('nova_descricao_tarefa')
                    nova_data_tarefa = request.form.get("nova_data")

                    # Atualiza a tabela 'tarefas' com os novos valores atualizados 
                    query_update_tarefas = 'UPDATE tarefas SET nome_tarefa=%s,descricao_tarefa=%s,data_tarefa=%s WHERE id=%s'
                    cursor.execute(query_update_tarefas, (nova_categoria_tarefa, nova_descricao_tarefa, nova_data_tarefa, id_tarefa_editada, ))
                    mysql.commit()

                    # Cria um dicionário 'nova_tarefa' para mapear os dados e enviar em formato jsonify
                    nova_tarefa = {
                        "novaCategoria": nova_categoria_tarefa,
                        "novaDescricao": nova_descricao_tarefa,
                        "novaData": nova_data_tarefa,
                        "id": id_tarefa_editada
                    }

                    return jsonify(nova_tarefa)
                
        except Exception as e:
            mysql.rollback()
            return f"Ocorre um erro: {e}"

        finally:
            cursor.close()
            

# Rota para exclusão das tarefas            
@app.route("/excluir-tarefa", methods=['POST'])
def excluirTarefa():

    # Tratamento de erros
    try:
        with mysql.cursor() as cursor:
            if request.method == 'POST':
                
                # Guarda o valor da id da tarefa a ser excluída enviada pelo formulário em uma variável
                id_tarefa_excluida = request.form.get("tarefa_excluida")

                # Deleta a tarefa na tabela 'tarefas' baseado no id recebido
                query_delete_tarefa = "DELETE FROM tarefas WHERE id= %s"
                cursor.execute(query_delete_tarefa, (id_tarefa_excluida, ))
                mysql.commit()

                return jsonify({"message": "Tarefa excluída com sucesso"})
    
    except Exception as e:
        mysql.rollback()
        return f"Ocorreu um erro: {e}"
    
    finally:
        cursor.close()


# Rota para carregar a página 'sobre-o-criador'
@app.route("/sobre-o-criador")
def sobreMim():

    if logado:
    
        return render_template("sobre-o-criador.html") # Carrega a página 'sobre-o-criador'
    
    return redirect(url_for('login')) # Carrega a página do login


# Inicia o app
if __name__ == "__main__":
    app.run(debug=True)