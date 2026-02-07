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

🖼️ 3.1 Class Diagram

---

![Class Diagram](https://raw.githubusercontent.com/Norahxj/holbertonschool-hbnb/refs/heads/main/part1/Class%20Diagram.png)

---

Diagram Purpose:

Defines core entities

Shows attributes and methods

Illustrates relationships and multiplicities

Clarifies ownership and dependencies

🧬 3.2 Entity Explanations
👤 User

Represents a registered platform user.

Responsibilities:

Register and manage an account

Own places

Submit reviews

Design Notes:

Password is private for security

Business rules belong in this layer

Persistence is handled externally via repositories

🏠 Place

Represents a property listed by a user.

Responsibilities:

Store property details

Maintain ownership relationship

Aggregate reviews and amenities

Design Notes:

A place must belong to exactly one user

Acts as a central entity in the domain

⭐ Review

Represents feedback provided by a user for a place.

Responsibilities:

Store rating and comment

Enforce relationship with user and place

Design Notes:

Reviews cannot exist without a user and a place

🛎️ Amenity

Represents a feature or service offered by a place.

Responsibilities:

Describe reusable amenities

Support many-to-many relationships

🔗 4. Relationships Summary
Relationship	Type	Multiplicity	Description
User → Place	Association	1 → 0..*	A user can own multiple places
User → Review	Association	1 → 0..*	A user can submit multiple reviews
Place → Review	Association	1 → 0..*	A place can have multiple reviews
Place ↔ Amenity	Many-to-Many	* ↔ *	Places can share amenities
🔄 5. Sequence Diagrams — API Interaction Flow

Sequence diagrams illustrate runtime behavior and clearly show how requests flow across layers.



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
