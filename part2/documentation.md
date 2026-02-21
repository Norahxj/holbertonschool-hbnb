# HBnB — System Documentation  
## Task 6: API Testing and System Architecture  
Prepared by: Manar

---

# 1. Introduction

The HBnB project is a simplified AirBnB-like platform designed to demonstrate strong software engineering principles, including layered architecture, object-oriented design, and clear separation of concerns.

This document provides a complete technical blueprint for Task 6. It includes:

- High-level architecture  
- Layer responsibilities  
- Domain model overview  
- API testing for Users, Places, Reviews, and Amenities  
- Success and failure test cases  
- Team responsibilities  
- Final project structure  

This documentation is intended to guide implementation, support maintenance, and serve as a shared technical reference.

---

# 2. Team Responsibilities

The HBnB project was developed collaboratively. Each team member was responsible for a specific domain.

| Team Member | Responsibility |
|-------------|----------------|
| Maryam | Full responsibility for the Review entity (model and API), and for designing the overall project structure. |
| Manar | Responsible for the User entity, the Repository layer (persistence/repository.py), and executing all API testing and documentation. |
| Noura | Responsible for the Place and Amenity entities and their API endpoints. |

---

# 3. High-Level Architecture

HBnB follows a three-layer architecture that improves modularity, maintainability, and testability.

The layers are:

- Presentation Layer  
- Business Logic Layer  
- Persistence Layer  

Dependencies flow from top to bottom only.

---

## 3.1 Presentation Layer

The Presentation Layer is the entry point of the system.

### Responsibilities

- Expose RESTful API endpoints  
- Handle HTTP requests and responses  
- Perform basic request validation  
- Translate client requests into business operations  
- Return appropriate HTTP status codes  

### Design Rule

This layer contains no business logic.  
All core processing is delegated to the Business Logic Layer via the facade.

---

## 3.2 Business Logic Layer

The Business Logic Layer represents the core domain of the application.

### Responsibilities

- Define domain entities (User, Place, Review, Amenity)  
- Enforce business rules and validations  
- Coordinate workflows across entities  
- Act as the single communication point for the Presentation Layer  

### Validation Enforcement

All critical validation rules are enforced inside the Business Logic Layer to guarantee data integrity regardless of the request source.

Examples:

- Review rating must be between 1 and 5  
- Required fields must be validated before object creation  
- Related entities must exist before associations are created  

### Facade Pattern

All interactions pass through the facade in services/facade.py, which:

- Simplifies communication  
- Prevents tight coupling  
- Centralizes business workflows  

---

## 3.3 Persistence Layer

The Persistence Layer is responsible for data storage and retrieval.

### Responsibilities

- Persist domain objects  
- Retrieve and query data  
- Abstract database implementation details  

### Design Rule

This layer contains no business logic.  
It only performs data access operations through the repository.

---

# 4. Final Project Structure

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

---

# 5. Domain Model Overview

The domain model includes four main entities:

- User  
- Place  
- Review  
- Amenity  

Each entity includes:

- UUID identifier  
- Audit fields (created_at, updated_at)  
- Attributes describing its state  
- Methods describing its behavior
The Review entity enforces rating validation within the Business Logic Layer to ensure values remain within the accepted range (1–5).

---

# 6. API Testing

All tests were executed using curl against:

http://127.0.0.1:5000/api/v1/

---

## 6.1 Review API Validation

### 6.1.1 Rating Out of Range

curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
-H "Content-Type: application/json" \
-d '{"user_id":"valid_uuid","place_id":"valid_uuid","comment":"Bad","rating":10}'

#### Response

{
    "message": "Rating must be between 1 and 5"
}

Rating validation is enforced at the Business Logic Layer level.

---

## 6.2 Missing Required Fields

curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
-H "Content-Type: application/json" \
-d '{}'

#### Response

{
    "message": "Missing required fields"
}

Raw exceptions are not exposed to the client.  
Errors are handled and returned in a structured JSON format.

---

## 6.3 Amenity API Testing

### 6.3.1 Create Amenity

curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
-H "Content-Type: application/json" \
-d '{"name":"WiFi"}'

#### Response

{
    "id": "995359bd-1e8f-411d-af56-7441f35b1f5e",
    "name": "WiFi",
    "description": ""
}

---

### 6.3.2 Get Amenity

curl -X GET http://127.0.0.1:5000/api/v1/amenities/995359bd-1e8f-411d-af56-7441f35b1f5e

#### Response

{
    "id": "995359bd-1e8f-411d-af56-7441f35b1f5e",
    "name": "WiFi",
    "description": ""
}

DELETE operation is not implemented for amenities in Part 2 as per project requirements.

---

# 7. API Documentation (Swagger)

The HBnB project includes built-in API documentation using Swagger UI.

Swagger operates entirely within the Presentation Layer and does not contain business logic.

It allows developers to:

- Explore all endpoints  
- View request/response schemas  
- Test API calls directly from the browser  
- Validate request formats  

Swagger is available at:

http://127.0.0.1:5000/api/v1/docs

---

# 8. Conclusion

All API endpoints for Users, Places, Reviews, and Amenities were tested successfully.  

Business rules such as rating validation and required field checks are enforced within the Business Logic Layer to ensure data integrity.  

The layered architecture, facade pattern, and repository design operate as intended and maintain a clean separation of concerns.

This document serves as the complete technical reference for Task 6.
