import pymysql  # Importa o módulo pymysql para interagir com o banco de dados MySQL

class BaseHelper:
    def __init__(self, connection: pymysql.connections.Connection, cursor: pymysql.cursors.Cursor):
        self.conn = connection  # Atribui a conexão do banco de dados à variável de instância 'conn'
        self.cursor = cursor  # Atribui o cursor do banco de dados à variável de instância 'cursor'
