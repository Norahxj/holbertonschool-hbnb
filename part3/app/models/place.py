from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()

        if not title or len(title) > 100:
            raise ValueError("title is required and must be <= 100 characters")

        if not isinstance(owner, User):
            raise ValueError("owner must be a User instance")

        self.title = title
        self.description = description
        self._price = None
        self._latitude = None
        self._longitude = None
        self.price = price      # triggers setter validation
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

        self.reviews = []
        self.amenities = []

    # Property for price
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("price must be a positive value")
        self._price = value
        self.touch()  # update timestamp

    # Property for latitude
    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not (-90 <= value <= 90):
            raise ValueError("latitude must be between -90 and 90")
        self._latitude = value
        self.touch()

    # Property for longitude
    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not (-180 <= value <= 180):
            raise ValueError("longitude must be between -180 and 180")
        self._longitude = value
        self.touch()

    def add_review(self, review):
        self.reviews.append(review)
        self.touch()

    def add_amenity(self, amenity):
        if not isinstance(amenity, Amenity):
            raise ValueError("amenity must be an Amenity instance")
        self.amenities.append(amenity)
        self.touch()
