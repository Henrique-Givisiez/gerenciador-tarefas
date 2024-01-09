import pymysql

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

