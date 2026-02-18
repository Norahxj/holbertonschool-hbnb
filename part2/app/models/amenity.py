from app.models.base import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()

        if not name or len(name) > 50:
            raise ValueError("Amenity name is required and must be <= 50 characters")

        self.name = name
