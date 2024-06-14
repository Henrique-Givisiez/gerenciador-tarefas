import unittest
from flask_testing import TestCase
from factory import create_app
app = create_app()

class TestTasksRoutes(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        return app

    def test_create_task(self):
        with self.client.session_transaction() as sess:
            sess['id'] = 1

        data_task_test = {
            "task_type": "teste categoria",
            "task_description": "teste descricao",
            "task_date": "2024-06-13"
        }

        response = self.client.post("/create-task", data=data_task_test)
        json_data = response.json

        self.assertTrue(json_data['success'])
        self.assertEqual(json_data["status"], "Tarefa criada com sucesso")

    def test_create_task_unauthenticated(self):
        response = self.client.post('/create-task', data={})
        # Verifique se o caminho da resposta é correto
        self.assertEqual(response.location, '/login')


if __name__ == "__main__":
    unittest.main()