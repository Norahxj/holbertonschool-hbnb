import unittest
from app import create_app


class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_email(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_users(self):
        self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        })
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)

    def test_get_user_invalid_id(self):
        response = self.client.get('/api/v1/users/does-not-exist')
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
