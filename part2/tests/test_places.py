import unittest
import uuid
from app import create_app


class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        unique_email = f"owner_{uuid.uuid4()}@example.com"
        user_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": unique_email
        })

        self.assertEqual(user_resp.status_code, 201, msg=user_resp.get_json())
        self.user_id = user_resp.get_json()["id"]

    def test_create_place(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Flat",
            "description": "Nice place",
            "price": 100,
            "latitude": 10.0,
            "longitude": 20.0,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 201)

    def test_create_place_invalid_price(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Flat",
            "description": "Nice place",
            "price": -1,
            "latitude": 10.0,
            "longitude": 20.0,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_latitude(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Flat",
            "description": "Nice place",
            "price": 100,
            "latitude": 100.0,
            "longitude": 20.0,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)

    def test_get_places(self):
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
