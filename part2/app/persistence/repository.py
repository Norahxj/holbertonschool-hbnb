class Repository:
    def __init__(self):
        self.users = {}

    # USER CRUD
    def save_user(self, user):
        self.users[user.id] = user
        return user

    def get_user(self, user_id):
        return self.users.get(user_id)

    def delete_user(self, user_id):
        return self.users.pop(user_id, None)

    def all_users(self):
        return list(self.users.values())
