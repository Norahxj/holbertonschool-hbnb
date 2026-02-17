from app.persistence.repository import Repository
from app.models.user import User

repo = Repository()

class Facade:

    def create_user(self, data):
        user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=data["password"],
            is_admin=data.get("is_admin", False),
            is_owner=data.get("is_owner", False)
        )
        return repo.save_user(user)

    def get_all_users(self):
        return repo.all_users()

    def get_user(self, user_id):
        return repo.get_user(user_id)

    def update_user(self, user_id, data):
        user = repo.get_user(user_id)
        if not user:
            return None
        user.update_from_dict(data)
        return user

    def delete_user(self, user_id):
        return repo.delete_user(user_id)
