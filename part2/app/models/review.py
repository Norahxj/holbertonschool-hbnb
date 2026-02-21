from place import Place
from user import User

from base_model import BaseModel

class Review(BaseModel):
    def __init__(self, user_id, place_id, comment, rating):
        """Initialize a new Review instance."""
        super().__init__()
        self.user_id = user_id
        self.place_id = place_id
        # self.name = name
        self.comment = comment
        self.ratings = rating
        self.review_id = self.id

    def save(self):
        """Save the review only if the user is not the host/place owner of the place."""
        if self.user_id == self.place_id.host_id:
            raise ValueError("Host or place owner cannot review their own place.")
        super().save()

    def to_dict(self):
        """Return a dictionary representation of the Review instance."""
        base_dict = super().to_dict()
        base_dict.update({
            'user_id': self.user_id,
            'place_id': self.place_id,
            'comment': self.comment,
            'ratings': self.ratings,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'id': self.review_id
        })
        return base_dict
