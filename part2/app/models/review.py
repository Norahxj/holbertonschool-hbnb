from app.models.place import Place
from app.models.user import User
from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, user_id, place_id, comment, rating):
        super().__init__()
        self.user_id = user_id
        self.place_id = place_id
        self.comment = comment
        self.rating = rating

    def save(self):
        super().save()

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            'user_id': self.user_id,
            'place_id': self.place_id,
            'comment': self.comment,
            'rating': self.rating,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        })
        return base_dict
