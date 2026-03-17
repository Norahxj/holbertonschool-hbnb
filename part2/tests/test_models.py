import unittest
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class TestModelsValidation(unittest.TestCase):

    def test_user_valid(self):
        user = User("John", "Doe", "john@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john@example.com")

    def test_user_invalid_email(self):
        with self.assertRaises(ValueError):
            User("John", "Doe", "invalid-email")

    def test_user_empty_first_name(self):
        with self.assertRaises(ValueError):
            User("", "Doe", "john@example.com")

    def test_amenity_valid(self):
        amenity = Amenity("Wi-Fi")
        self.assertEqual(amenity.name, "Wi-Fi")

    def test_amenity_empty_name(self):
        with self.assertRaises(ValueError):
            Amenity("")

    def test_place_valid(self):
        owner = User("Jane", "Doe", "jane@example.com")
        place = Place("Flat", "Nice", 100, 10.0, 20.0, owner)
        self.assertEqual(place.title, "Flat")
        self.assertEqual(place.price, 100)

    def test_place_negative_price(self):
        owner = User("Jane", "Doe", "jane2@example.com")
        with self.assertRaises(ValueError):
            Place("Flat", "Nice", -1, 10.0, 20.0, owner)

    def test_place_invalid_latitude(self):
        owner = User("Jane", "Doe", "jane3@example.com")
        with self.assertRaises(ValueError):
            Place("Flat", "Nice", 100, 100.0, 20.0, owner)

    def test_place_invalid_longitude(self):
        owner = User("Jane", "Doe", "jane4@example.com")
        with self.assertRaises(ValueError):
            Place("Flat", "Nice", 100, 10.0, 200.0, owner)

    def test_review_valid(self):
        user = User("Ali", "Saleh", "ali@example.com")
        place = Place("Flat", "Nice", 100, 10.0, 20.0, user)
        review = Review("Great stay", 5, place, user)
        self.assertEqual(review.text, "Great stay")
        self.assertEqual(review.rating, 5)

    def test_review_empty_text(self):
        user = User("Ali", "Saleh", "ali2@example.com")
        place = Place("Flat", "Nice", 100, 10.0, 20.0, user)
        with self.assertRaises(ValueError):
            Review("", 5, place, user)

    def test_review_invalid_rating_low(self):
        user = User("Ali", "Saleh", "ali3@example.com")
        place = Place("Flat", "Nice", 100, 10.0, 20.0, user)
        with self.assertRaises(ValueError):
            Review("Bad", 0, place, user)

    def test_review_invalid_rating_high(self):
        user = User("Ali", "Saleh", "ali4@example.com")
        place = Place("Flat", "Nice", 100, 10.0, 20.0, user)
        with self.assertRaises(ValueError):
            Review("Bad", 6, place, user)


if __name__ == "__main__":
    unittest.main()
