from .base_model import BaseModel
import re

class User(BaseModel):
    """User model."""

    def __init__(self, first_name, last_name, email, password, is_admin=False, is_owner=False):
        super().__init__()

        if not first_name or not first_name.strip():
            raise ValueError("first_name is required")

        if not last_name or not last_name.strip():
            raise ValueError("last_name is required")

        if not email or not email.strip():
            raise ValueError("email is required")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("invalid email format")

        if not password or not password.strip():
            raise ValueError("password is required")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.is_owner = is_owner

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "is_owner": self.is_owner,
        })
        return data
