class Repository:
    def init(self):
        self.users = {}
        self.places = {}
        self.amenities = {}

    # ---------------- USERS ----------------
    def save_user(self, user):
        self.users[user.id] = user
        return user

    def get_user(self, user_id):
        return self.users.get(user_id)

    def delete_user(self, user_id):
        return self.users.pop(user_id, None)

    def all_users(self):
        return list(self.users.values())

    # ---------------- PLACES ----------------
    def save_place(self, place):
        self.places[place.id] = place
        return place

    def get_place(self, place_id):
        return self.places.get(place_id)

    def delete_place(self, place_id):
        return self.places.pop(place_id, None)

    def all_places(self):
        return list(self.places.values())

    # ---------------- AMENITIES ----------------
    def save_amenity(self, amenity):
        self.amenities[amenity.id] = amenity
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenities.get(amenity_id)

    def delete_amenity(self, amenity_id):
        return self.amenities.pop(amenity_id, None)

    def all_amenities(self):
        return list(self.amenities.values())


# instance used by the whole app
storage = Repository()
