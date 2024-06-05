from hashlib import sha256  # Importa a função sha256 do módulo hashlib
from re import match  # Importa a função match do módulo re para fazer comparações de padrões
from database.base import BaseHelper  # Importa a classe BaseHelper do módulo database.base
from tasks.helper import TaskHelper  # Importa a classe TaskHelper do módulo tasks.helper
import pymysql  # Importa o módulo pymysql para interagir com o banco de dados MySQL

class AccountsHelper(BaseHelper):
    def __init__(self, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
        super().__init__(connection, cursor)
        self.task = TaskHelper(self.conn, self.cursor)  # Cria uma instância de TaskHelper para manipular tarefas relacionadas ao usuário

    # Checa o login
    def check_auth(self, email: str, password: str):
        msg = ""  # Mensagem de retorno
        success = False  # Indica se o login foi bem-sucedido
        user_id = None  # ID do usuário logado
        # Hash da senha
        hashed_password = sha256(password.encode()).hexdigest()

        query_select_contas = "SELECT * FROM contas WHERE email = %s and senha = %s"  # Query para selecionar a conta com o email e senha fornecidos

        try:
            if not match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = "Endereço de email inválido"
            elif not email or not password:
                msg = "Campos incompletos!"
            else: 
                self.cursor.execute(query_select_contas, (email, hashed_password))  # Executa a query com os parâmetros
                user = self.cursor.fetchone()  # Obtém o resultado da query
                if user:
                    user_id = user[0]  # Obtém o ID do usuário
                    username = user[1]  # Obtém o nome de usuário
                    msg = f"Bem-vindo, {username}!"  # Mensagem de boas-vindas
                    success = True  # Indica que o login foi bem-sucedido
                else:
                    msg = "Credenciais inválidas!"  # Mensagem de erro se as credenciais estiverem incorretas

            return user_id, msg, success  # Retorna o ID do usuário, a mensagem e o status de sucesso
        
        except Exception as error:  
            msg = f"Ocorreu um erro: {error}"  # Mensagem de erro em caso de exceção
            return user_id, msg, success  # Retorna a mensagem de erro e o status de sucesso

    # Checa se o usuário possui tarefas
    def user_have_tasks(self, user_id):
        result = self.task.read(user_id=user_id)  
        if result:
            return True
        return False
    
    # Cria um novo usuário
    def create(self, username: str, email: str, password: str):
        msg = ""  # Mensagem de retorno
        success = False  # Indica se a criação da conta foi bem-sucedida

        # Hash da senha
        hashed_password = sha256(password.encode()).hexdigest()

        # Query para inserir um novo usuário no banco de dados
        query_insert_contas = "INSERT INTO contas(usuario, email, senha) VALUES (%s, %s, %s)"

        try:
            # Verifica se a conta já existe
            query_select_contas = "SELECT * FROM contas WHERE email = %s"
            self.cursor.execute(query_select_contas, (email,))
            conta_existente = self.cursor.fetchone()
            
            if conta_existente:
                msg = "Essa conta já existe!"
            
            elif not match(r'[^@]+@[^@]+\.[^@]+', email): 
                msg = 'Endereço de email inválido!'

            elif not match(r'[A-Za-z0-9]+', username): 
                msg = 'Usuário só deve conter números e letras!'

            elif not username or not email or not password:
                msg = "Campos incompletos!"

            else:
                # Executa a query para inserir o novo usuário
                self.cursor.execute(query_insert_contas, (username, email, hashed_password))
                self.conn.commit()
                msg = "Conta criada com sucesso!"
                success = True

            return success, msg
                
        except Exception as error:
            # Cancela a transação e retorna a mensagem de erro
            self.conn.rollback()
            msg = f"Ocorreu um erro: {error}"
            return success, msg

    # Função para ler usuário
    def read(self, user_id: int):
        query_select_contas = "SELECT * FROM contas WHERE id = %s"  # Query para selecionar o usuário pelo ID
        try:
            self.cursor.execute(query_select_contas, (user_id,))  # Executa a query com o ID do usuário
            return self.cursor.fetchone()  # Retorna o usuário encontrado
        except Exception as error:
            return f"Ocorreu um erro: {error}"  # Retorna a mensagem de erro em caso de exceção

    # Atualiza dados do usuário
    def update(self, user_id: int, new_username: str = None, new_email: str = None, new_password: str = None):
        success = False  # Indica se a atualização foi bem-sucedida
        fields_list = []  # Lista de campos a serem atualizados
        new_values = []  # Novos valores dos campos

        if new_username:
            fields_list.append("usuario = %s")
            new_values.append(new_username)

        if new_email:
            fields_list.append("email = %s")
            new_values.append(new_email)

        if new_password:
            hashed_password = sha256(new_password.encode()).hexdigest()
            fields_list.append("senha = %s")
            new_values.append(hashed_password)

        # Junta todos os campos existentes na query de atualização
        query_update_contas = "UPDATE contas SET" + ", ".join(fields_list) + " WHERE id = %s"
        new_values.append(user_id)

        try:
            # Executa a query de atualização
            self.cursor.execute(query_update_contas, tuple(new_values))
            self.conn.commit()
            success = True
            return success  # Retorna o status de sucesso

        except Exception as error:
            print(f"Ocorreu um erro: {error}")  # Exibe a mensagem de erro
            self.conn.rollback()  # Cancela a transação
            return success  # Retorna o status de sucesso

    # Deleta usuário
    def delete(self, user_id: int):
        query_delete_contas = "DELETE FROM contas WHERE id = %s"  # Query para deletar o usuário pelo ID
        success = False  # Indica se a exclusão foi bem-sucedida
        msg = ""  # Mensagem de retorno

        try:
            # Verifica se o usuário possui tarefas
            if not self.user_have_tasks(user_id):
                # Deleta o usuário
                self.cursor.execute(query_delete_contas, (user_id,))
                self.conn.commit()
                success = True
                return success
        
            else:
                # Se o usuário tiver tarefas, exclui as tarefas antes de excluir o usuário
                self.task.delete(user_id=user_id)
                return self.delete(user_id)  # Recursivamente chama a função delete para excluir o usuário novamente

        except Exception as error:
            msg = f"Ocorreu um erro {error}"  # Mensagem de erro em caso de exceção
            self.conn.rollback()  # Cancela a transação
            return msg, success  # Retorna a mensagem de erro e o status de sucesso
