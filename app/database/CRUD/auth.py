from hashlib import sha256
from database.base import BaseHelper

class AuthHelper(BaseHelper):
    # Create a new user function
    def create(self, username: str, email: str, password: str) -> bool:
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
                print("Essa conta já existe!")
                return False
                
            else:
                # Execute the query
                self.cursor.execute(query_insert_contas, (username, email, hashed_password))
                self.conn.commit()
                return True
                
        except Exception as error:
            # Cancel the commit
            self.conn.rollback()
            print(f"Ocorreu um erro: {error}")
            return False
        
    # Check user login
    def check_login(self, email: str, password: str):
        # Hash password
        hashed_password = sha256(password.encode()).hexdigest()
        # Select query to get 'id' from user with 'email' and 'senha' as parameters
        query_select_conta = "SELECT id FROM contas WHERE email = %s AND senha = %s"
        try:
            # Execute query
            self.cursor.execute(query_select_conta, (email, hashed_password))
            user_id = self.cursor.fetchone()
            if user_id:
                return user_id # User found
            return False # User not found

        except Exception as error:
            print(f"Ocorreu um erro: {error}")    
            return False
        

    # Read user details
    def read(self, user_id: int):
        # Select query to get data from user
        query_select_contas = "SELECT * FROM contas WHERE id=%s"
        try:
            # Execute query
            self.cursor.execute(query_select_contas, (user_id))
            user_details = self.cursor.fetchone()
            return user_details

        except Exception as error:
            print(f"Ocorreu um erro: {error}")
            return None
        

    # Update user 
    def update(self, user_id: int, new_username: str, new_email: str, new_password: str) -> bool:
        
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
            return True

        except Exception as error:
            print(f"Ocorreu um erro: {error}")
            return False

    # Delete user
    def delete(self, user_id: int) -> bool:

        # Check if user have tasks 
        if not self.user_have_tasks(user_id=user_id):
            # Query to delete user in database
            query_delete_conta = "DELETE FROM contas WHERE id = %s"
            try:
                # Execute query
                self.cursor.execute(query_delete_conta, (user_id))
                self.conn.commit()
                return True
            
            except Exception as error:
                # Cancel commit
                self.conn.rollback()
                print(f"Ocorreu um erro: {error}")
                return False
            
        else:
            # Query to delete tasks from user
            query_delete_tarefa = "DELETE FROM tarefas WHERE usuario_id = %s"
            try:
                # Execute query
                self.cursor.execute(query_delete_tarefa, (user_id))
                self.conn.commit()
                return self.delete(user_id)

            except Exception as error:
                # Cancel commit
                self.conn.rollback()
                print(f"Ocorreu um erro: {error}")
                return False

    # Check tasks from user function
    def user_have_tasks(self, user_id: int) -> bool:
        # Query to select tasks from user
        query_select_tarefas = "SELECT * FROM tarefas WHERE usuario_id = %s"
        try:
            # Execute query
            self.cursor.execute(query_select_tarefas, (user_id))
            results = self.cursor.fetchall()
            if results:
                return True # User still have tasks
            return False # No tasks
        except Exception as error:
            print(f"Ocorreu um erro: {error}")
            return True


