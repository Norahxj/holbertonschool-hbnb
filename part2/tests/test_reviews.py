import unittest
import uuid
from app import create_app


class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        unique_email = f"reviewer_{uuid.uuid4()}@example.com"
        user_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Reviewer",
            "last_name": "User",
            "email": "reviewer@example.com"
        })

        self.assertEqual(user_resp.status_code, 201, msg=user_resp.get_json())
        self.user_id = user_resp.get_json()["id"]

        place_resp = self.client.post('/api/v1/places/', json={
            "title": "Flat",
            "description": "Nice place",
            "price": 100,
            "latitude": 10.0,
            "longitude": 20.0,
            "owner_id": self.user_id,
            "amenities": []
        })

        self.assertEqual(place_resp.status_code, 201, msg=place_resp.get_json())
        self.place_id = place_resp.get_json()["id"]

    def test_create_review(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great stay",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 201)

    def test_create_review_invalid_rating(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great stay",
            "rating": 6,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_empty_text(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_get_reviews(self):
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
