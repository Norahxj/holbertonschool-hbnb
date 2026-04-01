from sqlalchemy.orm import validates
from app.extensions import db
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    @validates('name')
    def validate_name(self, key, value):
        if not value or len(value.strip()) > 50:
            raise ValueError("Amenity name is required and must be <= 50 characters")
        return value.strip()

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "name": self.name
        })
        return data
