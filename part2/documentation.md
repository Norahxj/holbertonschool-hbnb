1. Overview

The final project structure

The exact responsibilities of each team member

The real behavior of each endpoint during testing

All curl commands used

Success and failure cases

Returned HTTP status codes

Swagger usage for API verification

This document reflects the actual implementation and the real test results observed during development.

2. Team Responsibilities (Actual Work Delivered)
Maryam
Designed the entire project structure

Created the folder organization:

api/v1

models

services

persistence

Implemented the Review model

Implemented the Review API endpoints

Connected the API layer to the Business Logic layer via the Facade

Ensured that Review creation, deletion, and retrieval work correctly

Manar
Implemented the User model

Implemented the User API endpoints

Implemented the Repository layer (persistence/repository.py)

Executed all Task 6 API tests

Documented all test results

Identified real runtime errors during testing (KeyError, 404, missing fields)

Noura
Implemented the Place model

Implemented the Amenity model

Implemented the Place API endpoints

Implemented the Amenity API endpoints

Ensured correct integration between Place and Amenity entities

3. Final Project Structure (Designed by Maryam)
كتابة تعليمات برمجية
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── users.py
│   │   │   ├── places.py
│   │   │   ├── reviews.py
│   │   │   ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
4. Swagger Usage (Actual Behavior)
Swagger was used during Task 6 to:

Display all available endpoints

Show required request bodies

Show expected responses

Display possible HTTP status codes (200, 201, 400, 404)

Test POST and GET requests quickly

Confirm that routes were properly registered

Swagger documentation was available at:

كتابة تعليمات برمجية
/api/v1/docs
Swagger correctly displayed:

User endpoints

Place endpoints

Review endpoints

Amenity endpoints

5. API Testing (Actual Results With curl)
5.1 User API (Implemented by Manar)
Create User — SUCCESS
كتابة تعليمات برمجية
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
-H "Content-Type: application/json" \
-d '{"first_name":"Manar","last_name":"Alharbi","email":"manar@example.com","password":"123456","is_admin":true,"is_owner":false}'
Result:

Returned 201 Created

User stored successfully

UUID generated automatically

5.2 Place API (Implemented by Noura)
Create Place — SUCCESS
كتابة تعليمات برمجية
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
-H "Content-Type: application/json" \
-d '{"title":"Manar House","description":"Nice place","price":200}'
Result:

Returned 201 Created

Place stored successfully

owner remained null

5.3 Review API (Implemented by Maryam)
Create Review — SUCCESS
كتابة تعليمات برمجية
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
-H "Content-Type: application/json" \
-d '{"user_id":"VALID_USER_ID","place_id":"VALID_PLACE_ID","comment":"Amazing place!","rating":5}'
Result:

Returned 201 Created

Review created successfully

Get Review — SUCCESS
كتابة تعليمات برمجية
curl -X GET http://127.0.0.1:5000/api/v1/reviews/REVIEW_ID
Result:

Returned 200 OK

Review data retrieved

Delete Review — SUCCESS
كتابة تعليمات برمجية
curl -X DELETE http://127.0.0.1:5000/api/v1/reviews/REVIEW_ID
Result:

Returned 204 No Content

Review deleted

Get Review After Deletion — FAILURE
كتابة تعليمات برمجية
curl -X GET http://127.0.0.1:5000/api/v1/reviews/REVIEW_ID
Result:

Returned 404 Not Found

Message: "Review not found"

6. Error Cases Encountered During Testing
6.1 Missing Required Fields → 400 Bad Request
When creating a Review without required fields:

كتابة تعليمات برمجية
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
-H "Content-Type: application/json" \
-d '{}'
Actual Result:

Returned 400 Bad Request

Error: KeyError: 'user_id'

6.2 Invalid Foreign Keys → 404 Not Found
Invalid user_id
كتابة تعليمات برمجية
{
  "message": "User not found"
}
Invalid place_id
كتابة تعليمات برمجية
{
  "message": "Place not found"
}
6.3 Invalid Resource ID → 404 Not Found
Using placeholder ID:

كتابة تعليمات برمجية
/amenities/AMENITY_ID
Result:

Returned 404 Not Found

7. Architecture Validation (Based on Real Results)
Scenario	Expected	Actual	Matches Design
Create resource	201	201	Yes
Get existing resource	200	200	Yes
Delete resource	204	204	Yes
Missing fields	400	400	Yes
Non-existent resource	404	404	Yes
Invalid foreign key	404	404	Yes
All results matched the intended system design.

8. Final Summary
Task 6 was successfully completed.

All endpoints were tested using curl.

Success and failure scenarios behaved exactly as expected.

Swagger confirmed proper endpoint registration.

The layered architecture worked correctly.

Each team member delivered their assigned components.
