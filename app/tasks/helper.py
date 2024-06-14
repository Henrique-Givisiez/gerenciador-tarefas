from database.base import BaseHelper  # Importa a classe BaseHelper do módulo database.base
from time import strftime  # Importa a função strftime do módulo time para formatar datas

# CRUD para tarefas
class TaskHelper(BaseHelper):
    # Cria tarefa
    def create(self, user_id: int, task_type: str, task_description: str, task_date: str):
        success = False  # Indica se a criação da tarefa foi bem-sucedida
        msg = ""  # Mensagem de retorno
        task_status = "pending"  # Define o status padrão da tarefa como "pendente"

        # Query para inserir uma nova tarefa no banco de dados
        query_insert_tasks = """INSERT INTO tarefas(
        usuario_id, categoria_tarefa, descricao_tarefa, data_tarefa, status_tarefa)
        VALUES (%s, %s, %s, %s, %s)"""

        try:
            if task_type and task_date:  # Verifica se os campos obrigatórios foram fornecidos
                # Executa a query para inserir a nova tarefa
                self.cursor.execute(query_insert_tasks, (user_id, task_type, task_description, task_date, task_status))
                self.conn.commit()
                success = True
                msg = "Tarefa criada com sucesso"
            else:
                msg = "Campos incompletos!"

            return success, msg

        except Exception as error:
            msg = f"Ocorreu um erro: {error}"  # Mensagem de erro em caso de exceção
            self.conn.rollback()
            return success, msg
        
    # Função para ler as tarefas
    def read(self, task_id: int = None, user_id: int = None):
        success = False  # Indica se a leitura da tarefa foi bem-sucedida
        
        try:
            if task_id:
                # Query para selecionar uma tarefa pelo ID
                query_read_task = "SELECT * FROM tarefas WHERE id = %s"
                self.cursor.execute(query_read_task, (task_id))
                task = self.cursor.fetchone()  # Obtém a tarefa
                task = {
                    "task_id": task[0],
                    "task_type": task[2],
                    "task_description": task[3],
                    "task_date": task[4].strftime("%d/%m/%Y")
                }
                return task
            
            if user_id:
                # Query para selecionar todas as tarefas de um usuário
                query_read_tasks_by_user = "SELECT * FROM tarefas WHERE usuario_id = %s"
                self.cursor.execute(query_read_tasks_by_user, (user_id))
                user_tasks = self.cursor.fetchall()  # Obtém todas as tarefas do usuário
                dict_tasks = {}
                success = True
                for task in user_tasks:
                    task = list(task)
                    task[4] =task[4].strftime("%d/%m/%Y")  # Formata a data da tarefa
                    dict_tasks[task[0]] = task
                return success, dict_tasks

        except Exception as error:
            msg = f"Ocorreu um erro: {error}"  # Mensagem de erro em caso de exceção
            return success, msg  
    
    # Atualiza tarefa
    def update(self, data: dict):
        success = False  # Indica se a atualização da tarefa foi bem-sucedida
        fields_list = []  # Lista de campos a serem atualizados
        new_values = []  # Novos valores dos campos
        task_id = data["task_id"]
        new_task_type = data["new_task_type"]
        new_task_description = data["new_task_description"]
        new_task_date = data["new_task_date"]
        new_task_status = data["new_task_status"]

        if new_task_type != "0" and len(new_task_type) != 0:
            fields_list.append("categoria_tarefa = %s")
            new_values.append(new_task_type)

        if new_task_description != "0" and len(new_task_description) != 0:
            fields_list.append("descricao_tarefa = %s")
            new_values.append(new_task_description)

        if new_task_date != "0" and len(new_task_date) != 0:
            fields_list.append("data_tarefa = %s")
            new_values.append(new_task_date)

        if new_task_status != "0" and len(new_task_status) != 0:
            fields_list.append("status_tarefa = %s")
            new_values.append(new_task_status)

        # Junta todos os campos existentes na query de atualização
        query_update_contas = "UPDATE tarefas SET " + ", ".join(fields_list) + " WHERE id = %s"
        new_values.append(task_id)

        try:
            # Executa a query de atualização
            self.cursor.execute(query_update_contas, tuple(new_values))
            self.conn.commit()
            success = True
            msg = "Tarefa atualizada com sucesso"
            return success, msg

        except Exception as error:
            msg = f"Ocorreu um erro: {error}"  # Mensagem de erro em caso de exceção
            self.conn.rollback()  # Cancela a transação
            return success, msg
        
    # Deleta tarefa
    def delete(self, task_id: int = None, user_id: int = None):
        success = False  # Indica se a exclusão da tarefa foi bem-sucedida

        try:
            if task_id:
                # Query para excluir
                query_delete_task = "DELETE FROM tarefas WHERE id = %s"
                self.cursor.execute(query_delete_task, (task_id))
            
            if user_id:
                # Query para excluir todas as tarefas de um usuário
                query_delete_user_tasks = "DELETE FROM tarefa WHERE usuario_id = %s"
                self.cursor.execute(query_delete_user_tasks, (user_id))
            
            self.conn.commit()  # Confirma a transação
            success = True  # Define que a operação foi bem-sucedida
            return success, msg
        
        except Exception as error:
            self.conn.rollback()  # Cancela a transação em caso de erro
            msg = f"Ocorreu um erro: {error}"  # Mensagem de erro em caso de exceção
            return success, msg  # Retorna a mensagem de erro e o status de sucesso
