from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

# Create objects
user = User("John", "Doe", "john@example.com")
place = Place("Nice Flat", "Very cozy", 120, 40.7, -73.9, user)
amenity = Amenity("Wi-Fi")
review = Review("Amazing stay!", 5, place, user)

# Link objects
place.add_amenity(amenity)

# Test relationships
print(place.title)
print(len(place.reviews))
print(place.amenities[0].name)
