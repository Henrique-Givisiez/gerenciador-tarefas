from flask import Flask
from hashlib import sha256
import requests

def create_app():
    # Cria um app com o Flask
    app = Flask(__name__)

    # Cria uma chave secreta e criptografa
    secret_key = 'Luco@1504'
    app.secret_key = sha256(secret_key.encode()).hexdigest()

    # Cria os parâmetros para a configuração do app
    host = 'localhost'
    user = 'root'
    password = 'mypassword'
    database = 'bd_gerenciador_de_tarefas'
    port = "5500"

    app.config['MYSQL_HOST'] = host
    app.config['MYSQL_PORT'] = port
    app.config['MYSQL_USER'] = user
    app.config['MYSQL_PASSWORD'] = password
    app.config['MYSQL_DB'] = database
    
    from routes.auth import auth_bp
    from routes.tasks import tasks_bp

    app.register_blueprint(auth_bp, url_prefix=f"/{auth_bp.name}")
    app.register_blueprint(tasks_bp, url_prefix=f"/{tasks_bp.name}")
    
    return app

