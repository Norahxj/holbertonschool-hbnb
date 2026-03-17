from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:

    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # ---------------- USERS ----------------

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        return self.user_repo.update(user_id, data)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    # ---------------- AMENITIES ----------------

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update(amenity_id, amenity_data)

    # ---------------- PLACES ----------------

    def create_place(self, place_data):

        # validate owner
        owner = self.get_user(place_data["owner_id"])
        if not owner:
            raise ValueError("Owner not found")

        # validate amenities
        amenities = []
        for amenity_id in place_data.get("amenities", []):
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity {amenity_id} not found")
            amenities.append(amenity)

        # create place
        place = Place(
            title=place_data["title"],
            description=place_data.get("description"),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner=owner
        )

        # attach amenities
        place.amenities = amenities

        # store
        self.place_repo.add(place)

        return place

    # Retrieve a place by ID
    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    # Retrieve all places
    def get_all_places(self):
        return self.place_repo.get_all()

    # Update a place
    def update_place(self, place_id, place_data):

        place = self.get_place(place_id)
        if not place:
            return None

        for key, value in place_data.items():

            if key == "owner_id":
                owner = self.get_user(value)
                if not owner:
                    raise ValueError("Owner not found")

                place.owner = owner

            elif key == "amenities":
                amenities = []
                for amenity_id in value:
                    amenity = self.get_amenity(amenity_id)
                    if not amenity:
                        raise ValueError(f"Amenity {amenity_id} not found")
                    amenities.append(amenity)

                place.amenities = amenities

            else:
                setattr(place, key, value)

        return place

    # ----------------- REVIEWS -----------------

    def create_review(self, review_data):

        user = self.get_user(review_data["user_id"])
        if not user:
            raise ValueError("User not found")

        place = self.get_place(review_data["place_id"])
        if not place:
            raise ValueError("Place not found")

        if not (1 <= review_data["rating"] <= 5):
            raise ValueError("Rating must be between 1 and 5")

        review = Review(
                text=review_data["text"],
                rating=review_data["rating"],
                user=user,
                place=place
                )

        self.review_repo.add(review)
        place.add_review(review)

        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):

        place = self.get_place(place_id)

        if not place:
            return None

        return place.reviews

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)

        if not review:
            return None

        if "text" in review_data:
            if not review_data["text"]:
                raise ValueError("text cannot be empty")
            review.text = review_data["text"]

            if "rating" in review_data:
                rating = review_data["rating"]
                if rating < 1 or rating > 5:
                    raise ValueError("rating must be between 1 and 5")
                review.rating = rating

                review.touch()

                return review

    def delete_review(self, review_id):

        review = self.review_repo.get(review_id)

        if not review:
            return False

        place = review.place

        if review in place.reviews:
            place.reviews.remove(review)

        self.review_repo.delete(review_id)

        return True
