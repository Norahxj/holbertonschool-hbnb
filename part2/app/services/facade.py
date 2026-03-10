from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place


class HBnBFacade:

    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()

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
