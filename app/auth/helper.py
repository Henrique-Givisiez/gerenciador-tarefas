from hashlib import sha256
from re import match
from app.database.base import BaseHelper
from app.tasks.helper import TaskHelper
import pymysql

# CRUD accounts
class AccountsHelper(BaseHelper):
    def __init__(self, connection: pymysql.Connection, cursor: pymysql.cursors.Cursor):
        super().__init__(connection, cursor)
        self.task = TaskHelper()

    # Check login
    def check_auth(self, email: str, password: str):
        msg = ""
        success = False
        user_id = None
        # Hash password
        hashed_password = sha256(password.encode()).hexdigest()
        
        query_select_contas = "SELECT * FROM contas WHERE email = %s and senha = %s"

        try:
            self.cursor.execute(query_select_contas, (email, hashed_password))

            user = self.cursor.fetchone()
            if user:
                user_id = user[0]
                username = user[1]
                msg = f"Seja bem vindo, {username}!"
                success = True
            
            else:
                msg = "Credencias inválidas!"

            return user_id, msg, success
        
        except Exception as error:
            msg = f"Ocorreu um erro: {error}"
            return msg, success
    

    # Check if user have tasks
    def user_have_tasks(self, user_id):
        result = self.task.read(user_id=user_id)
        if result:
            return True
        return False
    
        
    # Create a new user function
    def create(self, username: str, email: str, password: str):
        msg = ""
        success = False

        # Hash password
        hashed_password = sha256(password.encode()).hexdigest()

        # Query to insert user in database
        query_insert_contas = "INSERT INTO contas(usuario, email, senha) VALUES (%s, %s, %s)"

        try:
            # Check if account already exists 
            query_select_contas = "SELECT * FROM contas WHERE email = %s"
            self.cursor.execute(query_select_contas, (email))
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
                # Execute the query
                self.cursor.execute(query_insert_contas, (username, email, hashed_password))
                self.conn.commit()
                msg = "Conta criada com sucesso!"
                success = True

            return success, msg
                
        except Exception as error:
            # Cancel the commit
            self.conn.rollback()
            msg = f"Ocorreu um erro: {error}"
            return success, msg
    

    # Read user 
    def read(self, user_id: int):
        query_select_contas = "SELECT * FROM contas WHERE id = %s"
        try:
            self.cursor.execute(query_select_contas, (user_id))
            return self.cursor.fetchone()
        except Exception as error:
            return f"Ocorreu um erro: {error}"
    

    # Update user
    def update(self, user_id: int, new_username: str = None, new_email: str = None, new_password: str = None):
        success = False
        fields_list = []
        new_values = []

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

        # Join all existing fields to update query
        query_update_contas = "UPDATE contas SET" + ", ".join(fields_list) + "WHERE id = %s"
        new_values.append(user_id)

        try:
            # Execute the query
            self.cursor.execute(query_update_contas, tuple(new_values))
            self.conn.commit()
            success = True
            return success

        except Exception as error:
            print(f"Ocorreu um erro: {error}")
            self.conn.rollback()
            return success
        
    
    # Delete user
    def delete(self, user_id: int):
        query_delete_contas = "DELETE FROM contas WHERE id = %s"
        success = False
        msg = ""

        try:
            # Call function "user_have_tasks" to check tasks. If true, delete tasks from user 
            if not self.user_have_tasks(user_id):
                self.cursor.execute(query_delete_contas, (user_id))
                self.conn.commit()
                success = True
                return success
        
            else:
                self.task.delete(user_id=user_id)
                return self.delete(user_id)
            
        except Exception as error:
            msg = f"Ocorreu um erro {error}"
            self.conn.rollback()
            return msg, success