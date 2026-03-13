import unittest
import requests

class TestUserAPI(unittest.TestCase):
    url = 'http://localhost:5000/api/v1/'
    headers = {'Content-Type': 'application/json'}
    user = None
    place = None
    amenities = []
    reviews = []
    
    def test_01_create_user(self):
        user_data = {'first_name': 'John', 'last_name': 'Doe', 'email': 'john.doe@example.com'}
        response = requests.post(self.url + 'users/', json=user_data, headers=self.headers)
        
        self.assertEqual(response.status_code, 201)
        
        response_data = response.json()
        TestUserAPI.user = response_data
        self.assertIn('id', response_data)
        self.assertEqual(response_data['first_name'], 'John')
        self.assertEqual(response_data['last_name'], 'Doe')
        self.assertEqual(response_data['email'], 'john.doe@example.com')
        
    def test_02_update_user(self):
        user_data = {'first_name': 'Jane'}
        response = requests.put(self.url + f"users/{TestUserAPI.user['id']}", json=user_data, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        
        response_data = response.json()
        self.assertEqual(response_data['message'], "User updated successfully")

    def test_03_get_user(self):
        response = requests.get(self.url + f"users/{TestUserAPI.user['id']}", headers=self.headers)

        self.assertEqual(response.status_code, 200)
        
        response_data = response.json()
        self.assertEqual(response_data['first_name'], 'Jane')
        self.assertEqual(response_data['last_name'], 'Doe')
        self.assertEqual(response_data['email'], 'john.doe@example.com')

    def test_04_get_nonuser(self):
        response = requests.get(self.url + f"users/test", headers=self.headers)

        self.assertEqual(response.status_code, 404)
        response_data = response.json()
        self.assertEqual(response_data['error'], "User not found")
    
    def test_05_create_amenities(self):
        amenity_data = {'name': 'Wi-Fi'}
        response = requests.post(self.url + 'amenities/', json=amenity_data, headers=self.headers)
        response_data = response.json()
        self.assertIn('id', response_data)
        TestUserAPI.amenities.append({'id': response_data['id'], 'name': response_data['name']})
        self.assertEqual(response_data['name'], 'Wi-Fi')

        amenity_data = {'name': 'Pool'}
        response = requests.post(self.url + 'amenities/', json=amenity_data, headers=self.headers)
        response_data = response.json()
        self.assertIn('id', response_data)
        TestUserAPI.amenities.append({'id': response_data['id'], 'name': response_data['name']})
        self.assertEqual(response_data['name'], 'Pool')

    def test_06_update_amenity(self):
        amenity_data = {'name': 'Wi Fi'}
        response = requests.put(self.url + f'amenities/{TestUserAPI.amenities[0]['id']}', json=amenity_data, headers=self.headers)
        response_data = response.json()
        self.assertEqual(response_data['message'], 'Amenity updated successfully')

    def test_07_get_amenity(self):
        response = requests.get(self.url + f"amenities/{TestUserAPI.amenities[0]['id']}", headers=self.headers)

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['name'], "Wi Fi")

    def test_08_get_nonamenity(self):
        response = requests.get(self.url + f"amenities/test", headers=self.headers)

        self.assertEqual(response.status_code, 404)
        response_data = response.json()
        self.assertEqual(response_data['error'], "Amenity not found")

    def test_09_create_place_without_amenities(self):
        place_data = {
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": TestUserAPI.user['id'],
        }
        response = requests.post(self.url + 'places/', json=place_data, headers=self.headers)
        response_data = response.json()
        TestUserAPI.place = response_data
        self.assertEqual(response.status_code, 201)

        self.assertIn('id', response_data)
        self.assertEqual(response_data["title"], "Cozy Apartment")
        self.assertEqual(response_data["description"], "A nice place to stay")
        self.assertEqual(response_data['price'], 100.0)
        self.assertEqual(response_data['latitude'], 37.7749)
        self.assertEqual(response_data['longitude'], -122.4194)
        self.assertEqual(response_data['owner_id'], TestUserAPI.user['id'])
    
    def test_10_add_amenities(self):
        response = requests.post(self.url + f'places/{TestUserAPI.place['id']}/amenities', json=TestUserAPI.amenities, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        

    def test_11_create_place_with_amenities(self):
        place_data = {
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": TestUserAPI.user['id'],
            "amenities": self.amenities
        }
        response = requests.post(self.url + 'places/', json=place_data, headers=self.headers)
        response_data = response.json()
        self.assertEqual(response.status_code, 201)

        self.assertIn('id', response_data)
        TestUserAPI.place_id = response_data['id']
        self.assertEqual(response_data["title"], "Cozy Apartment")
        self.assertEqual(response_data["description"], "A nice place to stay")
        self.assertEqual(response_data['price'], 100.0)
        self.assertEqual(response_data['latitude'], 37.7749)
        self.assertEqual(response_data['longitude'], -122.4194)
        self.assertEqual(response_data['owner_id'], self.user['id'])

    def test_12_get_place(self):
        response = requests.get(self.url + f'places/{TestUserAPI.place['id']}', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["title"], "Cozy Apartment")
        self.assertEqual(response_data["description"], "A nice place to stay")
        self.assertEqual(response_data['price'], 100.0)
        self.assertEqual(response_data['latitude'], 37.7749)
        self.assertEqual(response_data['longitude'], -122.4194)
        self.assertEqual(response_data['owner']['id'], self.user['id'])
        self.assertEqual(response_data['amenities'][0], self.amenities[0])

    def test_13_create_review(self):
        review_data = {'text': 'Très bonne expérience', 'rating': 5, 'user_id': TestUserAPI.user['id'], 'place_id': TestUserAPI.place['id']}
        response = requests.post(self.url + 'reviews/', json=review_data, headers=self.headers)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        TestUserAPI.reviews.append(response_data)
        self.assertEqual(response_data['text'], review_data['text'])
        self.assertEqual(response_data['rating'], review_data['rating'])
        self.assertEqual(response_data['user_id'], review_data['user_id'])
        self.assertEqual(response_data['place_id'], review_data['place_id'])

    def test_14_create_review2(self):
        review_data = {'text': 'Pas fou', 'rating': 2, 'user_id': TestUserAPI.user['id'], 'place_id': TestUserAPI.place['id']}
        response = requests.post(self.url + 'reviews/', json=review_data, headers=self.headers)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        TestUserAPI.reviews.append(response_data)
        self.assertEqual(response_data['text'], review_data['text'])
        self.assertEqual(response_data['rating'], review_data['rating'])
        self.assertEqual(response_data['user_id'], review_data['user_id'])
        self.assertEqual(response_data['place_id'], review_data['place_id'])

    def test_15_get_review(self):
        response = requests.get(self.url + f'reviews/{TestUserAPI.reviews[0]['id']}')
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, TestUserAPI.reviews[0])

    def test_16_get_reviews(self):
        response = requests.get(self.url + f'reviews/')
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, TestUserAPI.reviews)

    def test_17_update_review(self):
        review_data = {'rating': 5}
        response = requests.put(self.url + f'reviews/{TestUserAPI.reviews[0]['id']}', json=review_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_18_get_places_reviews(self):
        response = requests.get(self.url + f'places/{TestUserAPI.place['id']}/reviews/')
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, TestUserAPI.reviews)

    def test_19_delete_review(self):
        response = requests.delete(self.url + f'reviews/{TestUserAPI.reviews[0]['id']}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Review deleted successfully')
        response = requests.get(self.url + f'reviews/')
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, [TestUserAPI.reviews[1]])


if __name__ == "__main__":
    unittest.main()
