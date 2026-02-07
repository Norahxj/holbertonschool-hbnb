HbnB - UML Project (Part1)

🏗️ 1. Introduction

The HBnB project is a simplified AirBnB-like platform designed to demonstrate strong software engineering principles, including layered architecture, object-oriented design, and clear separation of concerns.

This document compiles all architectural and behavioral diagrams produced during the design phase and serves as a technical blueprint for the system. It explains what the system is composed of, how its components interact, and why specific design decisions were made.

Purpose of This Document

This documentation is intended to:

Guide the implementation phase of the HBnB project

Provide a shared technical reference for developers

Clarify architectural boundaries and responsibilities

Document the business logic and API interaction flow

Support future maintenance and scalability

🧱 2. High-Level Architecture

HBnB follows a three-layer architecture, a widely used architectural style that improves modularity, maintainability, and testability.

The layers are:

Presentation Layer

Business Logic Layer

Persistence Layer

Each layer has a clearly defined responsibility, and dependencies flow in one direction only, from top to bottom.

🔹 Presentation Layer

The Presentation Layer is the entry point of the system.

Responsibilities:

Expose RESTful API endpoints

Handle HTTP requests and responses

Perform basic request validation and input sanitization

Translate client requests into business operations

Return appropriate HTTP status codes (200, 201, 400, 404, etc.)

Key Design Rule:
This layer does not contain business logic or database operations.
All core processing is delegated to the Business Logic Layer via the facade.

🔹 Business Logic Layer

The Business Logic Layer represents the core domain of the application.

Responsibilities:

Define domain entities (User, Place, Review, Amenity)

Enforce business rules and validations

Coordinate workflows across entities

Act as the single communication point for the Presentation Layer

Facade Pattern:
All interactions pass through HBnBFacade, which:

Simplifies communication

Prevents tight coupling

Centralizes business workflows

🔹 Persistence Layer

The Persistence Layer is responsible for data storage and retrieval.

Responsibilities:

Persist domain objects

Retrieve and query data

Abstract database implementation details

Key Design Rule:
This layer contains no business logic — only data access operations.

🗂️ 2.1 High-Level Package Diagram

---

![Package Diagram ](https://raw.githubusercontent.com/Norahxj/holbertonschool-hbnb/refs/heads/main/part1/Package%20Diagram%20.png)

---

Diagram Purpose:

Illustrates the three system layers

Shows dependency direction

Highlights the facade as the only gateway to business logic

🧠 Architectural Design Rationale

The layered architecture enforces separation of concerns

The facade pattern prevents the Presentation Layer from:

Accessing entities directly

Depending on internal business logic structure

This design supports:

Easier testing

Cleaner APIs

Future scalability

🧩 3. Business Logic Layer — Class Diagram

This section describes the domain model, which represents the core concepts and rules of the HBnB system.
# 🌐 HBnB Evolution — Business Logic Layer  
## 🧩 Detailed Class Diagram (Task 1)

### 📘 Overview  
This document presents the **Detailed Class Diagram** for the **Business Logic Layer** of the HBnB Evolution application.  
The goal of this task is to model the core domain entities, their attributes, behaviors, and relationships using standard UML notation.

The Business Logic Layer includes the following entities:

- **User**
- **Place**
- **Review**
- **Amenity**

*Each entity includes:
- A unique identifier (`UUID4`)
- Audit fields (`created_at`, `updated_at`)
- Attributes describing its state
- Methods describing its behavior
- Proper UML visibility (`+` public, `-` private)

> **Note:** All attributes and methods are public except `password`, which is private for security reasons.

---

## 🖼️ Class Diagram  
> ![Class Diagram](https://raw.githubusercontent.com/Norahxj/holbertonschool-hbnb/refs/heads/main/part1/Class%20Diagram.png)

### 👤 **User**
Represents a platform user (regular or admin).

#### **Attributes**
| Visibility | Name | Type |
|-----------|------|------|
| + | id | UUID |
| + | first_name | String |
| + | last_name | String |
| + | email | String |
| - | password | String |
| + | is_admin | Boolean |
| + | created_at | DateTime |
| + | updated_at | DateTime |

#### **Methods**
- `+ register()`
- `+ updateProfile()`
- `+ delete()`

#### **Notes**
- A user can own multiple places.
- A user can write multiple reviews.
- Password is private for security.

---

### 🏠 **Place**
Represents a property listed by a user.

#### **Attributes**
| Visibility | Name | Type |
|-----------|------|------|
| + | id | UUID |
| + | title | String |
| + | description | String |
| + | price | Float |
| + | latitude | Float |
| + | longitude | Float |
| + | owner_id | UUID |
| + | created_at | DateTime |
| + | updated_at | DateTime |

#### **Methods**
- `+ create()`
- `+ update()`
- `+ delete()`
- `+ listId()` *(as required by project)*

#### **Notes**
- A place belongs to exactly one user.
- A place can have many reviews.
- A place can have many amenities (many‑to‑many).

---

### ⭐ **Review**
Represents a user’s review on a place.

#### **Attributes**
| Visibility | Name | Type |
|-----------|------|------|
| + | id | UUID |
| + | rating | int |
| + | comment | String |
| + | user_id | UUID |
| + | place_id | UUID |
| + | created_at | DateTime |
| + | updated_at | DateTime |

#### **Methods**
- `+ create()`
- `+ update()`
- `+ delete()`
- `+ listId()` *(or listByPlace())*

#### **Notes**
- A review belongs to one user and one place.

---

### 🛎️ **Amenity**
Represents a feature or service available at a place.

#### **Attributes**
| Visibility | Name | Type |
|-----------|------|------|
| + | id | UUID |
| + | name | String |
| + | description | String |
| + | created_at | DateTime |
| + | updated_at | DateTime |

#### **Methods**
- `+ create()`
- `+ update()`
- `+ delete()`

#### **Notes**
- Amenity has a many‑to‑many relationship with Place.

---

## 🔗 Relationships Summary

| Relationship | Type | Multiplicity | Meaning |
|-------------|------|--------------|---------|
| User — Place | Association | 1 → 0..* | A user can own multiple places |
| User — Review | Association | 1 → 0..* | A user can write multiple reviews |
| Place — Review | Association | 1 → 0..* | A place can have multiple reviews |
| Place — Amenity | Association (M:N) | * ↔ * | A place can have many amenities and vice versa |

---

## 📝 Notes on UML Design  
- Visibility is represented using UML notation:  
  - `+` public  
  - `-` private  
- No lists appear inside methods — multiplicity handles that.
- All entities include UUID and audit timestamps.
- Diagram follows the Business Logic Layer requirements exactly.

---

## 🎯 Conclusion  
This class diagram provides a complete and accurate representation of the HBnB Business Logic Layer.  
It will serve as the foundation for implementing the models and business rules in later project phase.

---

![Class Diagram](https://raw.githubusercontent.com/Norahxj/holbertonschool-hbnb/refs/heads/main/part1/Class%20Diagram.png)

---

5.1 User Registration:

---

![Sequence Diagram (User Registration)](https://raw.githubusercontent.com/Norahxj/holbertonschool-hbnb/refs/heads/main/part1/Sequence%20Diagram%20(User%20Registration).png)

---

This sequence diagram illustrates how a new user account is created in the system. The user interacts with a web registration page, which submits the registration request to the API. The request is validated and forwarded to the Business Logic layer through the HBnBFacade. The system verifies email uniqueness, creates a user entity, securely hashes the password, and persists the user data in the database. Alternative flows handle error scenarios such as duplicate email addresses or invalid input.



5.2 Place Creation:

---

![Sequence Diagram (Place Creation)](https://raw.githubusercontent.com/Norahxj/holbertonschool-hbnb/refs/heads/main/part1/Sequence%20Diagram%20(Place%20Creation).png)

---

This diagram describes the workflow for creating a new place listing. The user submits place details through a dedicated page, which sends the request to the API. The Business Logic layer validates permissions and input data before creating a place entity. The place is then stored in the database through the persistence layer. The diagram also includes failure paths for invalid data or unauthorized actions, ensuring robust validation and error handling.



5.3 Review Submission:

---

![Sequence Diagram (Review Submission)](https://raw.githubusercontent.com/Norahxj/holbertonschool-hbnb/refs/heads/main/part1/Sequence%20Diagram%20(Review%20Submission).png)

---

The review submission sequence diagram shows how users can submit reviews for places. After writing a review, the request is sent to the API and processed by the Business Logic layer. The system validates the review content and ensures the referenced place exists before creating and saving the review. Both successful and failure scenarios are illustrated, highlighting how validation errors are returned to the user.



5.4 Fetching a List of Places:

---

![Sequence Diagram (Fetching a List of Places)](https://raw.githubusercontent.com/Norahxj/holbertonschool-hbnb/refs/heads/main/part1/Sequence%20Diagram%20(User%20Registration).png)

---

This diagram demonstrates how users search for available places. The user submits search filters through a search page, which forwards the request to the API. The Business Logic layer retrieves matching places from the database, formats the results, and returns them to the Presentation layer. The diagram includes an alternative flow for empty results, ensuring the system gracefully handles searches with no matches.



📝 6. Conclusion

This document provides a complete and structured technical overview of the HBnB Evolution system. It combines architectural design, domain modeling, and interaction flows into a single reference that supports implementation, testing, and future evolution.

By enforcing clear boundaries between layers and documenting interactions thoroughly, the HBnB system is designed to be robust, maintainable, and scalable.

✨ Authors

Norah Aljuhani
Holberton School — Saudi Arabia

Manar Althqfi
Holberton School — Saudi Arabia

Mariam Almalki
Holberton School — Saudi Arabia
