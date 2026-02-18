from app.models.base import BaseModel
from app.models.user import User
from app.models.amenity import Amenity


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()

        if not title or len(title) > 100:
            raise ValueError("title is required and must be <= 100 characters")

        if price < 0:
            raise ValueError("price must be a positive value")

        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("latitude must be between -90 and 90")

        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("longitude must be between -180 and 180")

        if not isinstance(owner, User):
            raise ValueError("owner must be a User instance")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        self.reviews.append(review)
        self.save()

    def add_amenity(self, amenity):
        if not isinstance(amenity, Amenity):
            raise ValueError("amenity must be an Amenity instance")
        self.amenities.append(amenity)
        self.save()
