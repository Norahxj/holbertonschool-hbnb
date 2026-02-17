import uuid
from datetime import datetime

class BaseModel:
    """Base class for all models."""

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def touch(self):
        """Update timestamp."""
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        """Convert object to dictionary."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def update_from_dict(self, data: dict):
        """Update attributes from a dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.touch()
