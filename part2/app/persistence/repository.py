class InMemoryRepository:
    """Simple in-memory storage"""

    def __init__(self):
        self.storage = {}

    def add(self, obj):
        self.storage[obj.id] = obj

    def get(self, obj_id):
        return self.storage.get(obj_id)

    def get_all(self):
        return list(self.storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if not obj:
            return None

        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        return obj

    def get_by_attribute(self, attr, value):
        for obj in self.storage.values():
            if getattr(obj, attr) == value:
                return obj
        return None
