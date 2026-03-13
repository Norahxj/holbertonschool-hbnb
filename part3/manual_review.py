import os
import uuid
import unittest
import requests

print("---------------- 👀 Checking task 0 ---------------- \n")
# Define the expected directory structure
required_dirs = [
    "app",
    "app/api",
    "app/api/v1",
    "app/models",
    "app/services",
    "app/persistence"
]

# Check if all required directories and init files exist
missing_dirs = [d for d in required_dirs if not os.path.isdir(d)]
missing_init_files = [d for d in required_dirs if not os.path.isfile(os.path.join(d, "__init__.py"))]

if missing_dirs:
    print("❌ Missing directories:")
    for d in missing_dirs:
        print(f" - {d}")
else:
    print("✅ All required directories exist.")

if missing_init_files:
    print("❌ Missing __init__.py files in:")
    for d in missing_init_files:
        print(f" - {d}")
else:
	print("✅ All required __init__.py files exist.")
     
with open('app/__init__.py', 'r') as f:
	content = f.read()
	if "from flask import Flask" in content and "from flask_restx import Api" and "app = Flask(__name__)" in content:
		print("✅ app/__init__.py looks good.")
	else:
		print("❌ app/__init__.py is missing expected imports.")

inMemoryRepository_methods = [
      'add',
      'get',
      'get_all',
      'get_by_attribute',
      'update',
      'delete' ]

from app.persistence.repository import InMemoryRepository
from abc import ABC
missings_methods = [m for m in inMemoryRepository_methods if not hasattr(InMemoryRepository, m)]
if missings_methods:
	print("❌ InMemoryRepository is missing methods:")
	for m in missings_methods:
		print(f" - {m}")
else:
	print("✅ InMemoryRepository has all expected methods.")

if issubclass(InMemoryRepository, ABC):
	print("✅ InMemoryRepository is a subclass of ABC.")
else:
	print("❌ InMemoryRepository is not a subclass of object.")

from app.services.facade import HBnBFacade
facade = HBnBFacade()
missing_attributes = [a for a in ['user_repo', 'amenity_repo', 'place_repo', 'review_repo'] if not hasattr(facade, a)]
if missing_attributes:
	print("❌ HBnBFacade is missing attributes:")
	for a in missing_attributes:
		print(f" - {a}")
else:
	wrong_attributes = [a for a in ['user_repo', 'amenity_repo', 'place_repo', 'review_repo'] if not isinstance(getattr(facade, a), InMemoryRepository)]
	if wrong_attributes:
		print("❌ HBnBFacade has wrong attributes:")
		for a in wrong_attributes:
			print(f" - {a}")
	else:
		print("✅ HBnBFacade has all expected attributes.")

with open("run.py", "r") as f:
	content = f.read()
	if "from app import create_app" in content and "app = create_app()" and "app.run(debug=True)" in content:
		print("✅ run.py looks good.")
	else:
		print("❌ run.py is missing expected imports.")

from config import Config, DevelopmentConfig
if DevelopmentConfig.DEBUG == True and Config.DEBUG == False and Config.SECRET_KEY:
	print("✅ config.py looks good")
else:
	print("❌ config.py is missing expected values.")

with open("requirements.txt", "r") as f:
	content = f.read()
	if "flask" in content and "flask-restx" in content:
		print("✅ requierements.txt looks good.")
	else:
		print("❌ requierements.txt is missing expected values.")

print("🫵 Check yourself if python3 run.py starts without any errors and access port 5000")
print("🫵 Check yourself if README exists and contains a brief overview of the project\n")

print("---------------- 👀 Checking task 1 ----------------\n")

from app.models.basemodel import BaseModel
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from datetime import datetime

# Check 0 - check if BaseModel has all expected attributes
print("👀 Checking check 0:\n")
basemodel = BaseModel()
attributes = {'id': str, 'created_at': datetime, 'updated_at': datetime}
missing_attributes = [a for a, t in attributes.items() if not hasattr(basemodel, a) or not isinstance(getattr(basemodel, a), t)]
if missing_attributes:
	print("❌ BaseModel is missing attributes:")
	for a in missing_attributes:
		print(f" - {a}")
else:
	print("✅ BaseModel has all expected attributes.")

missing_classes = [c for c in [BaseModel, User, Amenity, Place, Review] if not issubclass(c, BaseModel)]
if missing_classes:
	print("❌ Missing classes:")
	for c in missing_classes:
		print(f" - {c.__name__}")
else:
	print("✅ All classes inherits from BaseModel.")
print()

# Check 1 - check if User has all expected attributes
print("👀 Checking check 1:\n")
try:
	user = User('John', 'Doe', 'john.doe@example.com')
	print("✅ User is being created without errors.")
except:
	print("❌ User is not being created without errors.")

attributes = {'first_name': str, 'last_name': str, 'email': str, 'is_admin': bool}
missing_attributes = [a for a, t in attributes.items() if not hasattr(user, a) or not isinstance(getattr(user, a), t)]
if missing_attributes:
	print("❌ User is missing attributes:")
	for a in missing_attributes:
		print(f" - {a}")
else:
	print("✅ User has all expected attributes.")

try:
	user = User('', 'Doe', 'john.doexample.com')
	print("❌ User is not checking first_name if empty.")
except:
	print("✅ User is checking first_name if empty.")

try:
	user = User('abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz', 'Doe', 'john.doexample.com')
	print("❌ User is not checking first_name length.")
except:
	print("✅ User is checking first_name length.")

try:
	user = User('John', 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz', 'john.doexample.com')
	print("❌ User is not checking last_name length.")
except:
	print("✅ User is checking last_name length.")

try:
	user = User('John', '', 'john.doexample.com')
	print("❌ User is not checking last_name if empty.")
except:
	print("✅ User is checking last_name if empty.")

try:
	user = User('John', 1, 'john.doexample.com')
	print("❌ User is not checking last_name type.")
except TypeError:
	print("✅ User is checking last_name type.")

try:
	user = User('John', 'Doe', 'john.doexample.com')
	print("❌ User is not checking email format.")
except:	
	print("✅ User is checking email format.")

try:
	user = User('John', 'Doe', 'john.doe@example.com')
	print("❌ User is not checking email if it already exists.")
except:	
	print("✅ User is checking email if it already exists.")

try:
	user = User('John', 'Doe', 1)
	print("❌ User is not checking email type.")
except:	
	print("✅ User is checking email type.")
print()

# Check 2 - check if Place has all expected attributes
print("👀 Checking check 2:\n")

try:
	place = Place('My Place', 10.10, 86.02, 153.12, user, 'A nice place')
	print("✅ Place is being created without errors.")
except:
	print("❌ Place is not being created without errors.")

attributes = {'title': str, 'price': float, 'latitude': float, 'longitude': float, 'owner': User, 'description': str, 'reviews': list, 'amenities': list}
missing_attributes = [a for a, t in attributes.items() if not hasattr(place, a) or not isinstance(getattr(place, a), t)]
if missing_attributes:
	print("❌ Place is missing attributes:")
	for a in missing_attributes:
		print(f" - {a}")
else:
	print("✅ Place has all expected attributes.")

try:
	place = Place('012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890', 10, 86.02, 153.12, user, 'A nice place')
	print("❌ Place is not checking title length.")
except:
	print("✅ Place is checking title length.")

try:
	place = Place('', 10, 86.02, 153.12, user, 'A nice place')
	print("❌ Place is not checking title if empty.")
except:
	print("✅ Place is checking title if empty.")

try:
	place = Place(1, 10, 86.02, 153.12, user, 'A nice place')
	print("❌ Place is not checking title type.")
except:
	print("✅ Place is checking title type.")

try:
	place = Place('My Place', '10', 86.02, 153.12, user, 'A nice place')
	print("❌ Place is not checking price type or if negative.")
except:
	print("✅ Place is checking price type.")

try:
	place = Place('My Place', -1, 86.02, 153.12, user, 'A nice place')
	print("❌ Place is not checking price if negative.")
except:
	print("✅ Place is checking price type and if negative.")

try:
	place = Place('My Place', 10, '86.02', 153.12, user, 'A nice place')
	print("❌ Place is not checking latitude type.")
except:	
	print("✅ Place is checking latitude type.")

try:
	place = Place('My Place', 10, 91, 153.12, user, 'A nice place')
	print("❌ Place is not checking latitude if outside the range.")
except:	
	print("✅ Place is checking latitude if outside the range.")

try:
	place = Place('My Place', 10, 86.02, '153.12', user, 'A nice place')
	print("❌ Place is not checking longitude type.")
except:
	print("✅ Place is checking longitude type.")

try:
	place = Place('My Place', 10, 86.02, 181, user, 'A nice place')
	print("❌ Place is not checking longitude outside the range.")
except:
	print("✅ Place is checking longitude if outside the range.")

try:
	place = Place('My Place', 10, 86.02, 153.12, '', 'A nice place')
	place = Place('My Place', 10, 86.02, 153.12, 'test', 'A nice place')
	print("❌ Place is not checking owner if empty.")
except:
	print("✅ Place is checking owner if empty.")

try:
	place = Place('My Place', 10, 86.02, 153.12, 'test', 'A nice place')
	print("❌ Place is not checking owner type.")
except:
	print("✅ Place is checking owner type.")

print()

# Check 3 - check if Review has all expected attributes

print("👀 Checking check 3:\n")
try:
	review = Review('Great place', 5, place, user)
	print("✅ Review is being created without errors.")
except:
	print("❌ Review is not being created without errors.")

attributes = {'text': str, 'rating': int, 'place': Place, 'user': User}
missing_attributes = [a for a, t in attributes.items() if not hasattr(review, a) and not isinstance(getattr(review, a), t)]
if missing_attributes:
	print("❌ Review is missing attributes:")
	for a in missing_attributes:
		print(f" - {a}")
else:
	print("✅ Review has all expected attributes.")

try:
	review = Review('', 5, place, user)
	print("❌ Review is not validating text if empty.")
except:
	print("✅ Review is validating text if empty.")

try:
	review = Review(1, 5, place, user)
	print("❌ Review is not validating text type.")
except:
	print("✅ Review is validating text type.")

try:
	review = Review('Great place', '5', place, user)
	print("❌ Review is not validating rating type.")
except:
	print("✅ Review is validating rating type.")

try:
	review = Review('Great place', 6, place, user)
	review = Review('Great place', 0, place, user)
	print("❌ Review is not validating rating if outside the range.")
except:
	print("✅ Review is validating rating if outside the range.")

try:
	review = Review('Great place', 5, '', user)
	print("❌ Review is not validating place if empty.")
except:
	print("✅ Review is validating place if empty.")

try:
	review = Review('Great place', 5, 'place', user)
	print("❌ Review is not validating place type.")
except:
	print("✅ Review is validating place type.")

try:
	review = Review('Great place', 5, place, '')
	print("❌ Review is not validating user if empty.")
except:
	print("✅ Review is validating user type and if empty.")

try:
	review = Review('Great place', 5, place, 'user')
	print("❌ Review is not validating user type.")
except:
	print("✅ Review is validating user type and if empty.")
print()

# Check 4 - check if Amenity has all expected attributes

print("👀 Checking check 4:\n")
try:
	amenity = Amenity('Wifi')
	print("✅ Amenity is being created without errors.")
except:
	print("❌ Amenity is not being created without errors.")

attributes = {'name': str}
missing_attributes = [a for a, t in attributes.items() if not hasattr(amenity, a)]
if missing_attributes:
	print("❌ Amenity is missing attributes:")
	for a in missing_attributes:
		print(f" - {a}")
else:
	print("✅ Amenity has all expected attributes.")

try:
	amenity = Amenity('')
	amenity = Amenity(1)
	print("❌ Amenity is not validating name type or if empty.")
except:
	print("✅ Amenity is validating name type and if empty.")

if not 'add_review' in dir(Place):
	print("❌ User is missing add_review method.")
else:
	place.add_review(review)
	if review not in place.reviews:
		print("❌ add_review is not adding the review to the place.")
	else:
		print("✅ add_review is adding the review to the place.")
	
if not 'add_amenity' in dir(Place):
	print("❌ User is missing add_amenity method.")
else:
	place.add_amenity(amenity)
	if amenity not in place.amenities:
		print("❌ add_amenity is not adding the amenity to the place.")
	else:
		print("✅ add_amenity is adding the amenity to the place.")
print()

# Check 5 - check if classes have all exepected common methods and attributes

print("👀 Checking check 5:\n")
common_methods = ['save', 'update']
common_attributes = ['id', 'created_at', 'updated_at']
missing_methods = []
missing_attributes = []
objects = [user, place, review, amenity]
for obj in objects:
	for m in common_methods:
		if not hasattr(obj, m):
			missing_methods.append((obj.__class__.__name__,
				m))
	for a in common_attributes:
		if not hasattr(obj, a):
			missing_attributes.append((obj.__class__.__name__,
				a))
if missing_methods:
	print("❌ Missing methods:")
	for m in missing_methods:
		print(f" - {m[0]} is missing {m[1]} method.")
else:
	print("✅ All classes have all expected methods.")

if missing_attributes:
	print("❌ Missing attributes:")
	for a in missing_attributes:
		print(f" - {a[0]} is missing {a[1]} attribute.")
else:
	print("✅ All classes have all expected attributes.")

udpate_time = user.updated_at
user.update({'first_name': 'Jane'})
if user.updated_at == udpate_time:
	print("❌ update is not updating the updated_at attribute.")
else:
	print("✅ update is updating the updated_at attribute.")
print()

# Check 6 - check if all classes have a id using a valid UUID

print("👀 Checking check 6:\n")
for object in objects:
	try:
		uuid_obj = uuid.UUID(object.id, version=4)
		if str(uuid_obj) == object.id:
			print(f"✅ {object.__class__.__name__} id is a valid UUID.")
		else:
			print(f"❌ {object.__class__.__name__} id is not a valid UUID.")
	except:
		print(f"❌ {object.__class__.__name__} id is not a valid UUID.")
print()

# Check 7 - check if simple tests have been implemented
print("👀 Checking check 7:\n")
print("🫵 Check yourself if simple tests have been implemented\n")

print("---------------- 👀 Checking task 2 ----------------\n")

print("For the following tests, the API must be running on port 5000\n")

class TestAPI(unittest.TestCase):
	url = 'http://localhost:5000/api/v1/'
	headers = {'Content-Type': 'application/json'}
	user = None
	place = None
	amenities = []
	reviews = []
	user2 = None
    
	
	def test_01_create_user(self):
		user_data = {'first_name': 'John', 'last_name': 'Doe', 'email': 'john.doe@example.com'}
		response = requests.post(self.url + 'users/', json=user_data, headers=self.headers)

		try:
			self.assertEqual(response.status_code, 201)
			response_data = response.json()
			TestAPI.user = response_data
			self.assertIn('id', response_data)
			self.assertEqual(response_data['first_name'], 'John')
			self.assertEqual(response_data['last_name'], 'Doe')
			self.assertEqual(response_data['email'], 'john.doe@example.com')
			user_data = {'first_name': 'Mike', 'last_name': 'Tyson', 'email': 'mike.tyson@example.com'}
			response = requests.post(self.url + 'users/', json=user_data, headers=self.headers)
			TestAPI.user2 = response.json()
			print("✅ test_01_create_user passed")
		except:
			print("❌ test_01_create_user failed")
	
	def test_02_create_user_with_email_exists(self):
		user_data = {'first_name': 'John', 'last_name': 'Doe', 'email': 'john.doe@example.com'}
		response = requests.post(self.url + 'users/', json=user_data, headers=self.headers)

		try:
			self.assertEqual(response.status_code, 400)
			print("✅ test_02_create_user_with_email_exists passed")
		except:
			print("❌ test_02_create_user_with_email_exists failed")
		
	def test_03_create_user_with_wrong_data(self):
		user_data = {'first_name': 'John', 'last_name': 'Doe', 'email': 'john.doeexample.com'}
		response = requests.post(self.url + 'users/', json=user_data, headers=self.headers)

		try:
			self.assertEqual(response.status_code, 400)
			print("✅ test_03_create_user_with_wrong_data passed")
		except:
			print("❌ test_03_create_user_with_wrong_data failed")
		
	def test_04_get_user(self):
		response = requests.get(self.url + f"users/{TestAPI.user['id']}", headers=self.headers)

		try:
			self.assertEqual(response.status_code, 200)
			response_data = response.json()
			self.assertEqual(response_data['first_name'], 'John')
			self.assertEqual(response_data['last_name'], 'Doe')
			self.assertEqual(response_data['email'], 'john.doe@example.com')
			print("✅ test_04_get_user passed")
		except:
			print("❌ test_04_get_user failed")
		
	def test_05_get_nonuser(self):
		response = requests.get(self.url + f"users/test", headers=self.headers)

		self.assertEqual(response.status_code, 404)
		response_data = response.json()
		try:
			self.assertEqual(response_data['error'], "User not found")
			print("✅ test_05_get_nonuser passed")
		except:
			print("❌ test_05_get_nonuser failed")
	
	def test_06_get_users(self):
		response = requests.get(self.url + "users", headers=self.headers)

		try:
			self.assertEqual(response.status_code, 200)
			response_data = response.json()
			self.assertIn(TestAPI.user, response_data)
			self.assertEqual(len(response_data), 2)
			print("✅ test_06_get_users passed")
		except:
			print("❌ test_06_get_users failed")
	
	def test_07_update_user(self):
		user_data = {'first_name': 'Jane', 'email': 'jane.doe@example.com'}
		response = requests.put(self.url + f"users/{TestAPI.user['id']}", json=user_data, headers=self.headers)

		try:
			self.assertEqual(response.status_code, 200)
			response_data = response.json()
			self.assertEqual(response_data['first_name'], 'Jane')
			self.assertEqual(response_data['last_name'], 'Doe')
			self.assertEqual(response_data['email'], 'jane.doe@example.com')
			print("✅ test_07_update_user passed")
		except:
			print("❌ test_07_update_user failed")
	
	def test_08_update_user_with_invalid_data(self):
		user_data = {'email': 'jane.doeexample.com'}
		response = requests.put(self.url + f"users/{TestAPI.user['id']}", json=user_data, headers=self.headers)

		try:
			self.assertEqual(response.status_code, 400)
			print("✅ test_08_update_user_with_invalid_data passed")
		except:
			print("❌ test_08_update_user_with_invalid_data failed")
		
	def test_09_update_nonuser(self):
		user_data = {'first_name': 'John'}
		response = requests.put(self.url + f"users/test", json=user_data, headers=self.headers)

		try:
			self.assertEqual(response.status_code, 404)
			print("✅ test_09_update_nonuser passed")
		except:
			print("❌ test_09_update_nonuser failed")
		print("👀 Check yourself the Swagger documentation for users.")
		print("\n---------------- 👀 Checking task 3 ----------------\n")

	def test_10_create_amenities(self):
		try:
			amenity_data = {'name': 'Wi-Fi'}
			response = requests.post(self.url + 'amenities/', json=amenity_data, headers=self.headers)
			self.assertEqual(response.status_code, 201)
			response_data = response.json()
			self.assertIn('id', response_data)
			TestAPI.amenities.append({'id': response_data['id'], 'name': response_data['name']})
			self.assertEqual(response_data['name'], 'Wi-Fi')
			
			amenity_data = {'name': 'Pool'}
			response = requests.post(self.url + 'amenities/', json=amenity_data, headers=self.headers)
			self.assertEqual(response.status_code, 201)
			response_data = response.json()
			self.assertIn('id', response_data)
			TestAPI.amenities.append({'id': response_data['id'], 'name': response_data['name']})
			
			self.assertEqual(response_data['name'], 'Pool')
			print("✅ test_10_create_amenities passed")
		except:
			print("❌ test_10_create_amenities failed")
		
	def test_11_create_amenity_with_invalid_data(self):
		amenity_data = {'name': ''}
		response = requests.post(self.url + 'amenities/', json=amenity_data, headers=self.headers)

		try:
			self.assertEqual(response.status_code, 400)
			print("✅ test_11_create_amenity_with_invalid_data passed")
		except:
			print("❌ test_11_create_amenity_with_invalid_data failed")
		
	def test_12_get_amenity(self):
		response = requests.get(self.url + f"amenities/{TestAPI.amenities[0]['id']}", headers=self.headers)

		try:
			self.assertEqual(response.status_code, 200)
			response_data = response.json()
			self.assertEqual(response_data['name'], 'Wi-Fi')
			print("✅ test_12_get_amenity passed")
		except:
			print("❌ test_12_get_amenity failed")
	
	def test_13_get_nonamenity(self):
		response = requests.get(self.url + f"amenities/test", headers=self.headers)

		try:
			self.assertEqual(response.status_code, 404)
			print("✅ test_13_get_nonamenity passed")
		except:
			print("❌ test_13_get_nonamenity failed")
	
	def test_14_get_amenities(self):
		response = requests.get(self.url + "amenities", headers=self.headers)

		try:
			self.assertEqual(response.status_code, 200)
			response_data = response.json()
			self.assertIn(TestAPI.amenities[0], response_data)
			self.assertIn(TestAPI.amenities[1], response_data)
			print("✅ test_14_get_amenities passed")
		except:
			print("❌ test_14_get_amenities failed")
	
	def test_15_update_amenity(self):
		amenity_data = {'name': 'WiFi'}
		response = requests.put(self.url + f"amenities/{TestAPI.amenities[0]['id']}", json=amenity_data, headers=self.headers)

		try:
			self.assertEqual(response.status_code, 200)
			response_data = response.json()
			self.assertEqual(response_data['message'], 'Amenity updated successfully')
			print("✅ test_15_update_amenity passed")
		except:
			print("❌ test_15_update_amenity failed")
	
	def test_16_update_amenity_with_invalid_data(self):
		amenity_data = {'name': ''}
		response = requests.put(self.url + f"amenities/{TestAPI.amenities[0]['id']}", json=amenity_data, headers=self.headers)

		try:
			self.assertEqual(response.status_code, 400)
			print("✅ test_16_update_amenity_with_invalid_data passed")
		except:
			print("❌ test_16_update_amenity_with_invalid_data failed")
		
	def test_17_update_nonamenity(self):
		amenity_data = {'name': 'WiFi'}
		response = requests.put(self.url + f"amenities/test", json=amenity_data, headers=self.headers)

		try:
			self.assertEqual(response.status_code, 404)
			print("✅ test_17_update_nonamenity passed")
		except:
			print("❌ test_17_update_nonamenity failed")
	
	def test_18_check_facade_method(self):
		from app.services.facade import HBnBFacade
		facade = HBnBFacade()
		methods = ['create_amenity', 'get_amenity', 'get_all_amenities', 'update_amenity']
		missing_methods = [m for m in methods if not hasattr(facade, m)]
		if missing_methods:
			print("❌ HBnBFacade is missing methods:")
			for m in missing_methods:
				print(f" - {m}")
		else:
			print("✅ HBnBFacade has all expected methods.")
		print("👀 Check yourself if the facade is used in amenities controllers.")
		print("👀 Check yourself the Swagger documentation for amenities.")
		print("\n---------------- 👀 Checking task 4 ----------------\n")

	def test_19_create_place(self):
		# Delete amenities if the student didn't implement it in the POST method (task not clear about it)
		place_data = {'title': 'My Place', 'price': 10.10, 'latitude': 86.02, 'longitude': 153.12, 'owner_id': TestAPI.user['id'], 'description': 'A nice place', 'amenities': self.amenities}
		response = requests.post(self.url + 'places/', json=place_data, headers=self.headers)

		try:
			self.assertEqual(response.status_code, 201)
			response_data = response.json()
			TestAPI.place = response_data
			self.assertIn('id', response_data)
			self.assertEqual(response_data['title'], 'My Place')
			self.assertEqual(response_data['price'], 10.10)
			self.assertEqual(response_data['latitude'], 86.02)
			self.assertEqual(response_data['longitude'], 153.12)
			self.assertEqual(response_data['description'], 'A nice place')
			place_data = {'title': 'Villa', 'price': 150.10, 'latitude': 56.02, 'longitude': 123.12, 'owner_id': TestAPI.user['id'], 'description': 'A nice place'}
			response = requests.post(self.url + 'places/', json=place_data, headers=self.headers)
			print("✅ test_19_create_place passed")
		except:
			print("❌ test_19_create_place failed")
	
	def test_20_create_place_with_invalid_data(self):
		try:
			place_data = {'title': 'My Place', 'price': -10.10, 'latitude': 86.02, 'longitude': 153.12, 'owner_id': TestAPI.user['id'], 'description': 'A nice place'}
			response = requests.post(self.url + 'places/', json=place_data, headers=self.headers)
			self.assertEqual(response.status_code, 400)
			place_data = {'title': 'My Place', 'price': 10.10, 'latitude': 100.02, 'longitude': 153.12, 'owner_id': TestAPI.user['id'], 'description': 'A nice place'}
			response = requests.post(self.url + 'places/', json=place_data, headers=self.headers)
			self.assertEqual(response.status_code, 400)
			place_data = {'title': 'My Place', 'price': 10.10, 'latitude': 86.02, 'longitude': -193.12, 'owner_id': TestAPI.user['id'], 'description': 'A nice place'}
			response = requests.post(self.url + 'places/', json=place_data, headers=self.headers)
			self.assertEqual(response.status_code, 400)
			print("✅ test_20_create_place_with_invalid_data passed")
		except:
			print("❌ test_20_create_place_with_invalid_data failed")
		
	def test_21_create_place_with_invalid_ids(self):
		place_data = {'title': 'My Place', 'price': 10.10, 'latitude': 86.02, 'longitude': 153.12, 'owner_id': 'test', 'description': 'A nice place'}
		response = requests.post(self.url + 'places/', json=place_data, headers=self.headers)

		try:
			self.assertIn(response.status_code, [400, 404])
			# Delete the following 3 lines if the student didn't implement amenities in the POST method (task not clear about it)
			place_data = {'title': 'My Place', 'price': 10.10, 'latitude': 86.02, 'longitude': 153.12, 'owner_id': TestAPI.user['id'], 'description': 'A nice place', 'amenities': [{'id': 'test', 'name': 'WiFi'}]}
			response = requests.post(self.url + 'places/', json=place_data, headers=self.headers)
			self.assertIn(response.status_code, [400, 404])
			print("✅ test_21_create_place_with_invalid_ids passed")
		except:
			print("❌ test_21_create_place_with_invalid_ids failed")
	
	def test_22_get_place(self):
		response = requests.get(self.url + f"places/{TestAPI.place['id']}", headers=self.headers)

		try:
			self.assertEqual(response.status_code, 200)
			response_data = response.json()
			self.assertEqual(response_data['title'], 'My Place')
			self.assertEqual(response_data['price'], 10.10)
			self.assertEqual(response_data['latitude'], 86.02)
			self.assertEqual(response_data['longitude'], 153.12)
			self.assertEqual(response_data['description'], 'A nice place')
			self.assertTrue('owner' in response_data or 'owner_id' in response_data or 'ownerid' in response_data)
			self.assertTrue('amenities' in response_data)
			print("✅ test_22_get_place passed")
		except:
			print("❌ test_22_get_place failed")

	def test_23_get_nonplace(self):
		response = requests.get(self.url + f"places/test", headers=self.headers)

		try:
			self.assertEqual(response.status_code, 404)
			print("✅ test_23_get_nonplace passed")
		except:
			print("❌ test_23_get_nonplace failed")

	def test_24_get_places(self):
		response = requests.get(self.url + "places", headers=self.headers)

		try:
			self.assertEqual(response.status_code, 200)
			response_data = response.json()
			self.assertIn(TestAPI.place, response_data)
			self.assertEqual(len(response_data), 2)
			print("✅ test_24_get_places passed")
		except:
			print("❌ test_24_get_places failed")
	
	def test_25_update_place(self):
		place_data = {'title': 'My Place', 'price': 20.20, 'latitude': 86.02, 'longitude': 153.12, 'description': 'A nice place'}
		response = requests.put(self.url + f"places/{TestAPI.place['id']}", json=place_data, headers=self.headers)

		try:
			self.assertEqual(response.status_code, 200)
			response_data = response.json()
			self.assertEqual(response_data['message'], 'Place updated successfully')
			response = requests.get(self.url + f"places/{TestAPI.place['id']}", headers=self.headers)
			response_data = response.json()
			self.assertEqual(response_data['price'], 20.20)
			print("✅ test_25_update_place passed")
		except:
			print("❌ test_25_update_place failed")

	def test_26_update_place_with_invalid_data(self):
		try:
			place_data = {'price': -20.20}
			response = requests.put(self.url + f"places/{TestAPI.place['id']}", json=place_data, headers=self.headers)
			self.assertEqual(response.status_code, 400)
			place_data = {'latitude': 100.02}
			response = requests.put(self.url + f"places/{TestAPI.place['id']}", json=place_data, headers=self.headers)
			self.assertEqual(response.status_code, 400)
			place_data = {'longitude': -193.12}
			response = requests.put(self.url + f"places/{TestAPI.place['id']}", json=place_data, headers=self.headers)
			self.assertEqual(response.status_code, 400)
			print("✅ test_26_update_place_with_invalid_data passed")
		except:
			print("❌ test_26_update_place_with_invalid_data failed")

	def test_27_update_nonplace(self):
		place_data = {'title': 'My Place'}
		response = requests.put(self.url + f"places/test", json=place_data, headers=self.headers)

		try:
			self.assertEqual(response.status_code, 404)
			print("✅ test_27_update_nonplace passed")
		except:
			print("❌ test_27_update_nonplace failed")

	def test_28_check_facade_method(self):
		from app.services.facade import HBnBFacade
		facade = HBnBFacade()
		methods = ['create_place', 'get_place', 'get_all_places', 'update_place']
		missing_methods = [m for m in methods if not hasattr(facade, m)]
		if missing_methods:
			print("❌ HBnBFacade is missing methods:")
			for m in missing_methods:
				print(f" - {m}")
		else:
			print("✅ HBnBFacade has all expected methods.")
		print("👀 Check yourself if the facade is used in places controllers.")
		print("\n---------------- 👀 Checking task 5 ----------------\n")

	def test_29_create_review(self):
		review_data = {'text': 'Great place', 'rating': 5, 'place_id': TestAPI.place['id'], 'user_id': TestAPI.user2['id']}
		response = requests.post(self.url + 'reviews/', json=review_data, headers=self.headers)

		try:
			self.assertEqual(response.status_code, 201)
			response_data = response.json()
			TestAPI.reviews.append(response_data)
			self.assertIn('id', response_data)
			self.assertEqual(response_data['text'], 'Great place')
			self.assertEqual(response_data['rating'], 5)
			self.assertIn('user_id', response_data)
			self.assertIn('place_id', response_data)
			print("✅ test_29_create_review passed")
		except:
			print("❌ test_29_create_review failed")
	
	def test_30_create_review_with_invalid_data(self):
		review_data = {'text': 'Great place', 'rating': 6, 'place_id': TestAPI.place['id'], 'user_id': TestAPI.user2['id']}
		response = requests.post(self.url + 'reviews/', json=review_data, headers=self.headers)

		try:
			self.assertEqual(response.status_code, 400)
			review_data = {'text': '', 'rating': 2, 'place_id': TestAPI.place['id'], 'user_id': TestAPI.user2['id']}
			response = requests.post(self.url + 'reviews/', json=review_data, headers=self.headers)
			self.assertEqual(response.status_code, 400)
			print("✅ test_30_create_review_with_invalid_data passed")
		except:
			print("❌ test_30_create_review_with_invalid_data failed")

	def test_31_create_review_with_invalid_ids(self):
		review_data = {'text': 'Great place', 'rating': 5, 'place_id': 'test', 'user_id': TestAPI.user2['id']}
		response = requests.post(self.url + 'reviews/', json=review_data, headers=self.headers)

		try:
			self.assertIn(response.status_code, [400, 404])
			review_data = {'text': 'Great place', 'rating': 5, 'place_id': TestAPI.place['id'], 'user_id': 'test'}
			response = requests.post(self.url + 'reviews/', json=review_data, headers=self.headers)
			self.assertIn(response.status_code, [400, 404])
			print("✅ test_31_create_review_with_invalid_ids passed")
		except:
			print("❌ test_31_create_review_with_invalid_ids failed")

	def test_32_get_review(self):
		response = requests.get(self.url + f"reviews/{TestAPI.reviews[0]['id']}", headers=self.headers)

		try:
			self.assertEqual(response.status_code, 200)
			response_data = response.json()
			self.assertEqual(response_data['text'], 'Great place')
			self.assertEqual(response_data['rating'], 5)
			self.assertIn('user_id', response_data)
			self.assertIn('place_id', response_data)
			print("✅ test_32_get_review passed")
		except:
			print("❌ test_32_get_review failed")
		
	def test_33_get_nonreview(self):
		response = requests.get(self.url + f"reviews/test", headers=self.headers)

		try:
			self.assertEqual(response.status_code, 404)
			print("✅ test_33_get_nonreview passed")
		except:
			print("❌ test_33_get_nonreview failed")
	
	def test_34_get_reviews_for_places(self):
		response = requests.get(self.url + f"places/{TestAPI.place['id']}/reviews", headers=self.headers)

		try:
			self.assertEqual(response.status_code, 200)
			response_data = response.json()
			self.assertIn(TestAPI.reviews[0], response_data)
			print("✅ test_34_get_reviews_for_places passed")
		except:
			print("❌ test_34_get_reviews_for_places failed")
	
	def test_35_update_review(self):
		review_data = {'text': 'Great place', 'rating': 4}
		response = requests.put(self.url + f"reviews/{TestAPI.reviews[0]['id']}", json=review_data, headers=self.headers)

		try:
			self.assertEqual(response.status_code, 200)
			response_data = response.json()
			self.assertEqual(response_data['message'], 'Review updated successfully')
			response = requests.get(self.url + f"reviews/{TestAPI.reviews[0]['id']}", headers=self.headers)
			response_data = response.json()
			self.assertEqual(response_data['rating'], 4)
			print("✅ test_35_update_review passed")
		except:
			print("❌ test_35_update_review failed")
	
	def test_36_update_review_with_wrong_data(self):
		review_data = {'rating': 6}
		response = requests.put(self.url + f"reviews/{TestAPI.reviews[0]['id']}", json=review_data, headers=self.headers)

		try:
			self.assertEqual(response.status_code, 400)
			review_data = {'text': ''}
			response = requests.put(self.url + f"reviews/{TestAPI.reviews[0]['id']}", json=review_data, headers=self.headers)
			print("✅ test_36_update_review_with_wrong_data passed")
		except:
			print("❌ test_36_update_review_with_wrong_data failed")
		
	def test_37_delete_review(self):
		response = requests.delete(self.url + f"reviews/{TestAPI.reviews[0]['id']}", headers=self.headers)

		try:
			self.assertEqual(response.status_code, 200)
			response_data = response.json()
			self.assertEqual(response_data['message'], 'Review deleted successfully')
			response = requests.get(self.url + f"reviews/{TestAPI.reviews[0]['id']}", headers=self.headers)
			self.assertEqual(response.status_code, 404)
			print("✅ test_37_delete_review passed")
		except:
			print("❌ test_37_delete_review failed")
	
	def test_38_check_facade_methods_review(self):
		from app.services.facade import HBnBFacade
		facade = HBnBFacade()
		methods = ['create_review', 'get_review', 'get_all_reviews', 'get_reviews_by_place', 'update_review', 'delete_review']
		missing_methods = [m for m in methods if not hasattr(facade, m)]
		if missing_methods:
			print("❌ HBnBFacade is missing methods:")
			for m in missing_methods:
				print(f" - {m}")
		else:
			print("✅ HBnBFacade has all expected methods.")
		print("👀 Check yourself if the facade is used in reviews controllers.")
		print("\n---------------- 👀 Checking task 6 ----------------\n")

unittest.main()

print("For this task, you need to check if there are few tests for the API endpoints.\n")

