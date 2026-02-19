from app.models.base_model import BaseModel
import re

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password=None,
                 is_admin=False, is_owner=False):
        super().__init__(*args, **kwargs)

        if not first_name or not first_name.strip():
            raise ValueError("first_name is required")

        if not last_name or not last_name.strip():
            raise ValueError("last_name is required")

        if not email or not email.strip():
            raise ValueError("email is required")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("invalid email format")

        if password in not None and not password.strip():
            raise ValueError("password cannot be empty")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.is_owner = is_owner
