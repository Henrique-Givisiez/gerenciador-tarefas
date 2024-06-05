import pymysql  # Importa o módulo pymysql para interagir com o banco de dados MySQL
from auth.helper import AccountsHelper  # Importa a classe AccountsHelper do módulo auth.helper
from tasks.helper import TaskHelper  # Importa a classe TaskHelper do módulo tasks.helper

def get_db_connection():
    # Cria os parâmetros para a conexão da database
    host = 'localhost'
    user = 'root'
    password = 'mypassword'
    database = 'bd_gerenciador_de_tarefas'

    # Estabelece a conexão com o banco de dados
    connection = pymysql.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    return connection

class Database:
    def __init__(self):
        # Inicializa a conexão com o banco de dados e o cursor
        self.connection = get_db_connection()
        self.cursor = self.connection.cursor()

        # Instancia os ajudantes de banco de dados
        self.accounts = AccountsHelper(self.connection, self.cursor)
        self.tasks = TaskHelper(self.connection, self.cursor)

    def close(self):
        # Fecha a conexão com o banco de dados e o cursor
        self.connection.close()
        self.cursor.close()
