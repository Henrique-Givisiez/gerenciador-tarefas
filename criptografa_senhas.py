import pymysql
from hashlib import sha256

connection = pymysql.connect( 
        host='localhost', 
        user='root',  
        password = "Luco@1504", 
        db='bd_gerenciador_de_tarefas'
        ) 

def hash_password(senha: str):
    result = sha256(senha.encode()).hexdigest()
    return result

def cadastro():
    usuario = input("digite um usuario\n")
    senha = input("digite uma senha\n")
    email = "teste@email"
    senha_criptografada = hash_password(senha)

    with connection.cursor() as cursor:
        insert_query = "INSERT INTO contas(usuario, senha, email) VALUES (%s,%s,%s)"
        cursor.execute(insert_query, (usuario, senha_criptografada, email))
        connection.commit()
        print(senha_criptografada)
        login()
    
def login():
    usuario = input("digite um usuario\n")
    senha = input("digite uma senha\n")

    with connection.cursor() as cursor:
        select_query =  "SELECT senha FROM contas WHERE usuario = %s"
        senha_criptografada = hash_password(senha)
        print(senha_criptografada)
        cursor.execute(select_query, (usuario))
        senha_bd = cursor.fetchone()[0]
        if senha_bd == senha_criptografada:
            print("loggedin")
        else:
            print("wrong password")

print(login())

