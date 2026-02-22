# HBnB — Task 6 Documentation  

---

# 1. Overview

Task 6 required testing all API endpoints of the HBnB project and documenting:

- The final project structure  
- The exact responsibilities of each team member  
- All curl commands used during testing  
- The real behavior of each endpoint  
- Success and failure cases  
- Returned HTTP status codes  
- Swagger usage for API verification  
- Noting which entities did NOT require DELETE  

This document reflects the actual implementation and real test results observed during development.

---

# 2. Team Responsibilities (Actual Work Delivered)

## Mariam
- Designed the entire project structure  
- Created the folder organization:
  - api/v1  
  - models  
  - services  
  - persistence  
- Implemented the Review model  
- Implemented the Review API endpoints  
- Connected the API layer to the Business Logic layer via the Facade  
- Ensured Review creation, retrieval, and deletion work correctly  

## Manar
- Implemented the User model  
- Implemented the User API endpoints  
- Implemented the Repository layer (persistence/repository.py)  
- Executed all Task 6 API tests  
- Documented all test results  
- Identified real runtime errors during testing (KeyError, 404, missing fields)  

## Norah
- Implemented the Place model  
- Implemented the Amenity model  
- Implemented the Place API endpoints  
- Implemented the Amenity API endpoints  
- Ensured correct integration between Place and Amenity entities  

---

# 3. Final Project Structure (Designed by Mariam)

```text
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
```

---

# 4. Swagger Usage (Actual Behavior)

Swagger was used during Task 6 to:

- Display all available endpoints  
- Show required request bodies  
- Show expected responses  
- Display possible HTTP status codes (200, 201, 400, 404)  
- Test POST and GET requests quickly  
- Confirm that routes were properly registered  

Swagger documentation was available at:

```
http://127.0.0.1:5000/api/v1/docs
```

Swagger correctly displayed:

- User endpoints  
- Place endpoints  
- Review endpoints  
- Amenity endpoints  

Swagger was used as a live reference while running curl commands to ensure that:

- The endpoints existed  
- The request body format was correct  
- The responses matched the design  

---

# 5. API Testing (Actual Results With curl)

All tests were executed against:

```
http://127.0.0.1:5000/api/v1/
```

Below are the curl commands and the real behavior observed.

---

# 5.1 USER API (Implemented by Manar)

## 5.1.1 Create User — SUCCESS

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
-H "Content-Type: application/json" \
-d '{
  "first_name": "Manar",
  "last_name": "Alharbi",
  "email": "manar@example.com",
  "password": "123456",
  "is_admin": true,
  "is_owner": false
}'
```

**Result:**  
- 201 Created  
- User stored successfully  

---

## 5.1.2 Get User — SUCCESS

```bash
curl -X GET http://127.0.0.1:5000/api/v1/users/USER_ID
```

**Result:**  
- 200 OK  

---

## 5.1.3 Create User — FAILURE (Missing Fields)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
-H "Content-Type: application/json" \
-d '{"first_name":"Manar"}'
```

**Result:**  
- 400 Bad Request  

---

## 5.1.4 Note on DELETE for User

User entity **did NOT require DELETE** in Task 6.

---

# 5.2 PLACE API (Implemented by Noura)

## 5.2.1 Create Place — SUCCESS

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
-H "Content-Type: application/json" \
-d '{
  "title": "Manar House",
  "description": "Nice place",
  "price": 200
}'
```

**Result:**  
- 201 Created  

---

## 5.2.2 Get Place — SUCCESS

```bash
curl -X GET http://127.0.0.1:5000/api/v1/places/PLACE_ID
```

**Result:**  
- 200 OK  

---

## 5.2.3 Create Place — FAILURE (Missing Fields)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
-H "Content-Type: application/json" \
-d '{"title":"Only Title"}'
```

**Result:**  
- 400 Bad Request  

---

## 5.2.4 Note on DELETE for Place

Place entity **did NOT require DELETE** in Task 6.

---

# 5.3 AMENITY API (Implemented by Noura)

## 5.3.1 Create Amenity — SUCCESS

```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
-H "Content-Type: application/json" \
-d '{"name":"WiFi"}'
```

**Result:**  
- 201 Created  

---

## 5.3.2 Get Amenity — SUCCESS

```bash
curl -X GET http://127.0.0.1:5000/api/v1/amenities/AMENITY_ID
```

**Result:**  
- 200 OK  

---

## 5.3.3 Delete Amenity — SUCCESS  
(Not required but implemented)

```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/amenities/AMENITY_ID
```

**Result:**  
- 204 No Content  

---

## 5.3.4 Get Amenity After Deletion — FAILURE

```bash
curl -X GET http://127.0.0.1:5000/api/v1/amenities/AMENITY_ID
```

**Result:**  
- 404 Not Found  

---

## 5.3.5 Invalid Amenity ID — FAILURE

```bash
curl -X GET http://127.0.0.1:5000/api/v1/amenities/INVALID_ID
```

**Result:**  
- 404 Not Found  

---

# 5.4 REVIEW API (Implemented by Maryam)

## 5.4.1 Create Review — SUCCESS

```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
-H "Content-Type: application/json" \
-d '{
  "user_id": "VALID_USER_ID",
  "place_id": "VALID_PLACE_ID",
  "comment": "Amazing place!",
  "rating": 5
}'
```

**Result:**  
- 201 Created  

---

## 5.4.2 Create Review — FAILURE (Missing Fields)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
-H "Content-Type: application/json" \
-d '{}'
```

**Result:**  
- 400 Bad Request  
- KeyError: 'user_id'  

---

## 5.4.3 Create Review — FAILURE (Invalid user_id)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
-H "Content-Type: application/json" \
-d '{
  "user_id": "999",
  "place_id": "VALID_PLACE_ID",
  "comment": "Test",
  "rating": 4
}'
```

**Result:**  
- 404 Not Found  
- "User not found"  

---

## 5.4.4 Create Review — FAILURE (Invalid place_id)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
-H "Content-Type: application/json" \
-d '{
  "user_id": "VALID_USER_ID",
  "place_id": "999",
  "comment": "Test",
  "rating": 4
}'
```

**Result:**  
- 404 Not Found  
- "Place not found"  

---

## 5.4.5 Get Review — SUCCESS

```bash
curl -X GET http://127.0.0.1:5000/api/v1/reviews/REVIEW_ID
```

**Result:**  
- 200 OK  

---

## 5.4.6 Delete Review — SUCCESS

```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/reviews/REVIEW_ID
```

**Result:**  
- 204 No Content  

---

## 5.4.7 Get Review After Deletion — FAILURE

```bash
curl -X GET http://127.0.0.1:5000/api/v1/reviews/REVIEW_ID
```

**Result:**  
- 404 Not Found  
- "Review not found"  

---

# 6. Error Handling and HTTP Status Codes (Based on Real Results)

- 200 OK → Successful GET  
- 201 Created → Successful POST  
- 204 No Content → Successful DELETE  
- 400 Bad Request → Missing or invalid request body  
- 404 Not Found → Non-existent resource or invalid foreign key  

---

# 7. Architecture Validation (From Task 6 Behavior)

| Scenario                    | Expected | Actual | Matches |
|----------------------------|----------|--------|---------|
| Create resource            | 201      | 201    | Yes     |
| Get existing resource      | 200      | 200    | Yes     |
| Delete resource            | 204      | 204    | Yes     |
| Missing required fields    | 400      | 400    | Yes     |
| Non-existent resource ID   | 404      | 404    | Yes     |
| Invalid foreign key        | 404      | 404    | Yes     |

---

# 8. Final Summary

- All endpoints were tested using curl  
- Swagger was used to verify endpoint definitions and request/response formats  
- Success and failure scenarios behaved as expected  
- Some entities (User, Place) did not require DELETE  
- Review and Amenity DELETE operations were implemented and tested  
- Documentation includes every curl command and outcome observed in Task 6  

This document serves as the official technical record for Task 6.
```
