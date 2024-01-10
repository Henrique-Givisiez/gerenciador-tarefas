from hashlib import sha256
from re import match
from base import BaseHelper


class AccountsHelper(BaseHelper):

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

            loggedin = self.cursor.fetchone()
            
            if loggedin:
                user_id = loggedin[0]
                msg = "Seja bem vindo!"
                success = True
            
            else:
                msg = "Credencias inválidas!"

            return user_id, msg, success
        
        except Exception as error:
            msg = f"Ocorreu um erro: {error}"
            return msg, success
    

        
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
    