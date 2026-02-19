import uuid
from datetime import datetime

class BaseModel:
    """Base class for all models."""

    def __init__(self, *args, **kwargs):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        # Apply kwargs to the object (only if attribute exists)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def touch(self):
        """Update timestamp."""
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """Convert object to dictionary."""
        result = self.__dict__.copy()
        result["created_at"] = self.created_at.isoformat()
        result["updated_at"] = self.updated_at.isoformat()
        return result

    def update_from_dict(self, data: dict):
        """Update attributes from a dictionary."""
        for key, value in data.items():
            setattr(self, key, value)
        self.touch()

