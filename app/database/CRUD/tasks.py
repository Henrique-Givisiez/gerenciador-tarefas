from database.base import BaseHelper

class TaskHelper(BaseHelper):

    # Create a new task function
    def create(self, user_id: int, task_category: str, task_description: str, task_date: str, task_status: str) -> bool:
        # Query to create task
        query_insert_tarefas = "INSERT INTO tarefas(usuario_id, categoria_tarefa, descricao_tarefa, data_tarefa, status_tarefa) VALUES (%s, %s, %s, %s, %s)"
        try:
            # Execute query
            self.cursor.execute(query_insert_tarefas, (user_id, task_category, task_description, task_date, task_status))
            self.conn.commit()
            task_id = self.cursor.lastrowid
            return task_id
        except Exception as error:
            print(f"Ocorreu um erro: {error}")
            return False
        

    # Read all tasks
    def read(self, user_id: int):
        # Query to read tasks
        query_read_tasks = "SELECT * FROM tarefas WHERE usuario_id = %s"
        try:
            # Execute query
            self.cursor.execute(query_read_tasks, (user_id))
            tasks = self.cursor.fetchall()
            return tasks
        except Exception as error:
            print(f"Ocorreu um erro: {error}")
            return None
    

    # Update task
    def update(self, task_id: int, new_category: str, new_description: str, new_date: str, new_status: str) -> bool:
        fields_list = []
        new_values = []

        if new_category:
            fields_list.append("categoria_tarefa = %s")
            new_values.append(new_category)

        if new_description:
            fields_list.append("descricao_tarefa = %s")
            new_values.append(new_description)

        if new_date:
            fields_list.append("data_tarefa = %s")
            new_values.append(new_date)

        if new_status:
            fields_list.append("status_tarefa = %s")
            new_values.append(new_status)

        
        # Join all existing fields to update query
        query_update_tarefas = "UPDATE tarefas SET" + ", ".join(fields_list) + "WHERE id = %s"
        new_values.append(task_id)


        try:
            self.cursor.execute(query_update_tarefas, (new_values))
            self.conn.commit()
            return True
        except Exception as error:
            # Cancel commit
            self.conn.rollback()
            print(f"Ocorreu um erro: {error}")
            return False
        
    
    # Delete task
    def delete(self, task_id: int) -> bool:
        # Query to delete task
        query_delete_tarefa = "DELETE FROM tarefas WHERE id = %s"
        try:
            # Execute query
            self.cursor.execute(query_delete_tarefa, (task_id))
            self.conn.commit()
            return True
        except Exception as error:
            # Cancel commit
            self.conn.rollback()
            print(f"Ocorreu um erro: {error}")
            return False
