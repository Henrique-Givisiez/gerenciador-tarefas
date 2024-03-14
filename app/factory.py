from flask import Flask, request, g, session
from database.database import Database
from hashlib import sha256
from auth.routes import auth_bp
from tasks.routes import tasks_bp
database = Database()


def create_app():
    app = Flask(__name__, template_folder="../templates")

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_PORT'] = '5500'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'mypassword'
    app.config['MYSQL_DB'] = 'bd_gerenciador_de_tarefas'
    secret_key = 'Luco@1504'
    app.secret_key = sha256(secret_key.encode()).hexdigest()
    
    @app.before_request
    def load_user():
        user_id = request.headers.get("User-id")
        if user_id:
            user = database.auth.read(user_id)
            g.user = user
        else:
            g.user = None


    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    
    return app
