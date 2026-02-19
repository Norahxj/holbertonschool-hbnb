from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def init(self, name, description=""):
        super().init()

        if not name or not name.strip():
            raise ValueError("name is required")

        self.name = name
        self.description = description
