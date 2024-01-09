import pymysql

from accounts import AccountsHelper


def get_db_connection():
     # Cria os parâmetros para a conexão da database
    host = 'localhost'
    user = 'root'
    password = 'mypassword'
    database = 'bd_gerenciador_de_tarefas'

    connection = pymysql.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    return connection



class Database:
    def __init__(self):
        self.connection = get_db_connection()
        self.cursor = self.connection.cursor()
        self.accounts = AccountsHelper(self.connection, self.cursor)

    def close(self):
        self.connection.close()
        self.cursor.close()
