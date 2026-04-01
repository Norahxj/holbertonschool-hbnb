from sqlalchemy.orm import validates
from app.extensions import db
from app.models.base_model import BaseModel


class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, text, rating, place_id, user_id):
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    @validates('text')
    def validate_text(self, key, value):
        if not value or not value.strip():
            raise ValueError("Review text is required")
        return value.strip()

    @validates('rating')
    def validate_rating(self, key, value):
        if not (1 <= value <= 5):
            raise ValueError("rating must be between 1 and 5")
        return value

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_id": self.user_id
        })
        return data
