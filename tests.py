import pymysql

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
    database=database
)


with mysql.cursor() as cursor:
    query_select_contas = "SELECT * from contas"
    cursor.execute(query_select_contas)
    resposta = cursor.fetchall()
    for ind, conta in enumerate(resposta):
        print(ind)
        print(conta[1])