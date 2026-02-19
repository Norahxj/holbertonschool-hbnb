from app.persistence.repository import Repository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.repo = Repository()

    def create_user(self, data):
        user = User(**data)
        return self.repo.save_user(user)

    def get_user(self, user_id):
        return self.repo.get_user(user_id)

    def get_all_users(self):
        return self.repo.all_users()

    def update_user(self, user_id, data):
        user = self.repo.get_user(user_id)
        if not user:
            return None
        user.update_from_dict(data)
        return user
