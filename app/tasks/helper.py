from database.base import BaseHelper
from time import strftime

# CRUD for tasks
class TaskHelper(BaseHelper):

    # Create Task
    def create(self, user_id: int, task_type: str, task_description: str, task_date: str):
        success = False
        msg = ""
        task_status = "pending"        

        query_insert_tasks = """INSERT INTO tarefas(
        usuario_id, categoria_tarefa, descricao_tarefa, data_tarefa, status_tarefa)
        VALUES (%s, %s, %s, %s, %s)"""

        try:
            if task_type and task_date: # Required fields
                self.cursor.execute(query_insert_tasks, (user_id, task_type, task_description, task_date, task_status))
                self.conn.commit()
                success = True
                task_id = self.cursor.lastrowid
                task_created_successfully_dict ={
                    "id": task_id,
                    "type": task_type,
                    "description": task_description,
                    "date": task_date,
                    "status": task_status
                }
                return success, task_created_successfully_dict
            
            else:
                msg = "Campos incompletos!"
                return success, msg
                        
        
        except Exception as error:
            msg = f"Ocorreu um erro: {error}"
            return success, msg
        

    # Read task
    def read(self, task_id: int = None, user_id: int = None):
        success = False
        
        try:
            if task_id:
                query_read_task = "SELECT * FROM tarefas WHERE id = %s"
                self.cursor.execute(query_read_task, (task_id))
                task = self.cursor.fetchone()
                return task
            
            if user_id:
                query_read_tasks_by_user = "SELECT * FROM tarefas WHERE usuario_id = %s"
                self.cursor.execute(query_read_tasks_by_user, (user_id))
                user_tasks = self.cursor.fetchall()
                dict_tasks = {}
                success = True
                for task in user_tasks:
                    task = list(task)
                    task[4] = strftime("%d/%m/%Y") 
                    print(task)
                    dict_tasks[task[0]] = task

                return success, dict_tasks

        except Exception as error:
            msg = f"Ocorreu um erro: {error}"
            return success, msg  
        
    
    # Update task
    def update(self, task_id: int, new_task_type: str = None, new_task_descriprion: str = None, new_task_date: str = None, new_task_status: str = None):
        success = False
        fields_list = []
        new_values = []

        if new_task_type:
            fields_list.append("categoria_tarefa= %s")
            new_values.append(new_task_type)

        if new_task_descriprion:
            fields_list.append("descricao_tarefa = %s")
            new_values.append(new_task_descriprion)

        if new_task_date:
            fields_list.append("data_tarefa = %s")
            new_values.append(new_task_date)

        if new_task_status:
            fields_list.append("status_tarefa = %s")
            new_values.append(new_task_status)

        # Join all existing fields to update query
        query_update_contas = "UPDATE tarefas SET" + ", ".join(fields_list) + "WHERE id = %s"
        new_values.append(task_id)

        try:
            # Execute the query
            self.cursor.execute(query_update_contas, tuple(new_values))
            self.conn.commit()
            success = True
            return success

        except Exception as error:
            msg = f"Ocorreu um erro: {error}"
            self.conn.rollback()
            return success, msg
        

    # Delete task
    def delete(self, task_id: int = None, user_id: int = None):
        success = False

        try:
            if task_id:
                query_delete_task = "DELETE FROM tarefas WHERE id = %s"
                self.cursor.execute(query_delete_task, (task_id))
            
            if user_id:
                query_delete_user_tasks = "DELETE FROM tarefa WHERE usuario_id = %s"
                self.cursor.execute(query_delete_user_tasks, (user_id))
            
            self.conn.commit()
            success = True
            return success
        
        except Exception as error:
            self.conn.rollback()
            msg = f"Ocorreu um erro: {error}"
            return msg, success