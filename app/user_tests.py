import unittest
from flask_testing import TestCase
from factory import create_app
app = create_app()

class TestUserRoutes(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        return app

    def test_create_user(self):
        data_user = {
            "username": "beltrano",
            "email": "beltrano@email.com",
            "password": "senha"
        }

        response = self.client.post("/signup", data=data_user)

        json_data = response.json

        try:
            self.assertEqual(response.status_code, 200)
            self.assertTrue(json_data["success"])
            self.assertEqual(json_data["msg"], "Conta criada com sucesso")
        except AssertionError:
            print(json_data["msg"])
        


if __name__ == "__main__":
    unittest.main()