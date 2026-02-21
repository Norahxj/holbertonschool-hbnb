# HBnB — Task 6 Documentation  

---

# 1. Overview

Task 6 required testing all API endpoints of the HBnB project and documenting:

- The final project structure  
- The exact responsibilities of each team member  
- The real behavior of each endpoint during testing  
- Success and failure cases  
- Returned HTTP status codes  
- Swagger usage for API verification  

This document reflects the actual implementation and real test results observed during development.

---

# 2. Team Responsibilities (Actual Work Delivered)

## Maryam
- Designed the complete project structure  
- Created the folder organization:
  - api/v1  
  - models  
  - services  
  - persistence  
- Implemented the Review model  
- Implemented the Review API endpoints  
- Ensured proper integration between layers  
- Connected the API layer to the Business Logic layer via the Facade  

## Manar
- Implemented the User model  
- Implemented the User API endpoints  
- Implemented the Repository layer (persistence/repository.py)  
- Executed all Task 6 API tests  
- Documented all test results  
- Identified real runtime errors during testing (e.g., KeyError and 404 cases)  

## Noura
- Implemented the Place model  
- Implemented the Amenity model  
- Implemented the Place API endpoints  
- Implemented the Amenity API endpoints  
- Ensured correct integration between Place and Amenity entities  

---

# 3. Final Project Structure (Designed by Maryam)

hbnb/
├── app/
│   ├── init.py
│   ├── api/
│   │   ├── init.py
│   │   ├── v1/
│   │   │   ├── init.py
│   │   │   ├── users.py
│   │   │   ├── places.py
│   │   │   ├── reviews.py
│   │   │   ├── amenities.py
│   ├── models/
│   │   ├── init.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── init.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── init.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md

The architecture follows a clear layered design:

- Presentation Layer → api/
- Business Logic Layer → models/ and services/
- Persistence Layer → persistence/

Each layer has a single responsibility and communicates only with the layer directly below it.

---

# 4. Swagger Usage (Actual Behavior)

During Task 6, Swagger was used to:

- Display all available endpoints  
- Show required request bodies  
- Show expected responses  
- Display possible HTTP status codes (200, 201, 400, 404)  
- Test POST and GET requests quickly  
- Confirm that routes were properly registered  

Swagger documentation was available at:

/api/v1/docs

It correctly displayed:

- User endpoints  
- Place endpoints  
- Review endpoints  
- Amenity endpoints  

---

# 5. API Testing (Actual Results)

## 5.1 User API (Implemented by Manar)

### Create User (Success)

Result:
- Returned 201 Created  
- User was successfully stored  
- UUID was generated automatically  

---

## 5.2 Place API (Implemented by Noura)

### Create Place (Success)

Result:
- Returned 201 Created  
- Place was successfully stored  
- Owner field remained null (not linked to a user)

---

## 5.3 Review API (Implemented by Maryam)

### Create Review (Success)

Result:
- Returned 201 Created  
- Review was successfully created  
- Foreign keys were validated  

### Get Review (Success)

Result:
- Returned 200 OK  
- Data retrieved correctly  

### Delete Review (Success)

Result:
- Returned 204 No Content  
- Review was successfully deleted  

### Get Review After Deletion (Failure)

Result:
- Returned 404 Not Found  
- Message: "Review not found"

---

# 6. Error Cases Encountered During Testing

## 6.1 Missing Required Fields

When creating a Review without required fields:

Result:
- Returned 400 Bad Request  
- Error handled properly instead of exposing internal exceptions  

## 6.2 Invalid Foreign Keys

When using a non-existent user_id:

Result:
- Returned 404 Not Found  
- Message: "User not found"

When using a non-existent place_id:

Result:
- Returned 404 Not Found  
- Message: "Place not found"

## 6.3 Invalid Resource ID

When using a placeholder ID (not a valid UUID):

Result:
- Returned 404 Not Found  

---

# 7. Architecture Validation

All results matched the intended system design:

- Resource creation → 201  
- Successful retrieval → 200  
- Deletion → 204  
- Missing data → 400  
- Non-existent resources → 404  

The separation between Presentation, Business Logic, and Persistence layers functioned correctly during all tests.

---

# 8. Final Summary

Task 6 was successfully completed.

- All endpoints were tested.  
- Success and failure scenarios behaved as expected.  
- Swagger confirmed proper endpoint registration.  
- The layered architecture operated correctly.  

This document serves as the official technical record for Task 6.
