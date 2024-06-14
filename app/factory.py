from flask import Flask  # Importa os módulos necessários do Flask
from database.database import Database  # Importa a classe Database 
from hashlib import sha256  # Importa a função sha256 do módulo hashlib
from auth.routes import auth_bp  # Importa o blueprint auth_bp do módulo auth.routes
from tasks.routes import tasks_bp  # Importa o blueprint tasks_bp do módulo tasks.routes

database = Database()  # Cria uma instância da classe Database

def create_app():
    app = Flask(__name__, template_folder="../templates")  # Cria uma instância da aplicação Flask

    # Configurações do banco de dados MySQL
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_PORT'] = '5500'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'mypassword'
    app.config['MYSQL_DB'] = 'bd_gerenciador_de_tarefas'
     
    secret_key = 'chave super secreta'  # Chave secreta para a aplicação
    app.secret_key = sha256(secret_key.encode()).hexdigest()  # Gera a chave secreta e a associa à aplicação

    # Registra os blueprints na aplicação
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    
    return app  # Retorna a instância da aplicação
