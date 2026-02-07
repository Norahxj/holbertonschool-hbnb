# 📘 HBnB Evolution — System Documentation  
## 🏗️ Overview  

This document presents the full architectural and behavioral design of the HBnB Evolution platform.  
It compiles all UML diagrams created during the design phase and explains how the system’s components interact across the Presentation, Business Logic, and Persistence layers.  
The goal of this documentation is to guide development, ensure consistent understanding among team members, and support long‑term maintainability and scalability.

---

# 1. Introduction

The HBnB project is a simplified AirBnB-like platform designed to demonstrate strong software engineering principles, including layered architecture, object-oriented design, and clear separation of concerns.

This document compiles all architectural and behavioral diagrams produced during the design phase and serves as a technical blueprint for the system. It explains what the system is composed of, how its components interact, and why specific design decisions were made.

## Purpose of This Document

This documentation is intended to:

- Guide the implementation phase of the HBnB project  
- Provide a shared technical reference for developers  
- Clarify architectural boundaries and responsibilities  
- Document the business logic and API interaction flow  
- Support future maintenance and scalability  

---

# 2. High-Level Architecture

HBnB follows a three-layer architecture, a widely used architectural style that improves modularity, maintainability, and testability.

The layers are:

- **Presentation Layer**  
- **Business Logic Layer**  
- **Persistence Layer**

Each layer has a clearly defined responsibility, and dependencies flow in one direction only, from top to bottom.

---

## Presentation Layer

The Presentation Layer is the entry point of the system.

### Responsibilities:

- Expose RESTful API endpoints  
- Handle HTTP requests and responses  
- Perform basic request validation and input sanitization  
- Translate client requests into business operations  
- Return appropriate HTTP status codes (200, 201, 400, 404, etc.)

### Key Design Rule:
This layer does **not** contain business logic or database operations.  
All core processing is delegated to the Business Logic Layer via the facade.

---

## Business Logic Layer

The Business Logic Layer represents the core domain of the application.

### Responsibilities:

- Define domain entities (User, Place, Review, Amenity)  
- Enforce business rules and validations  
- Coordinate workflows across entities  
- Act as the single communication point for the Presentation Layer  

### Facade Pattern:
All interactions pass through **HBnBFacade**, which:

- Simplifies communication  
- Prevents tight coupling  
- Centralizes business workflows  

---

## Persistence Layer

The Persistence Layer is responsible for data storage and retrieval.

### Responsibilities:

- Persist domain objects  
- Retrieve and query data  
- Abstract database implementation details  

### Key Design Rule:
This layer contains **no business logic** — only data access operations.

---

# 2.1 High-Level Package Diagram

---

![Package Diagram ](https://raw.githubusercontent.com/Norahxj/holbertonschool-hbnb/refs/heads/main/part1/Package%20Diagram%20.png)

---

### Diagram Purpose:

- Illustrates the three system layers  
- Shows dependency direction  
- Highlights the facade as the only gateway to business logic  

---

## Architectural Design Rationale

The layered architecture enforces separation of concerns.

The facade pattern prevents the Presentation Layer from:

- Accessing entities directly  
- Depending on internal business logic structure  

This design supports:

- Easier testing  
- Cleaner APIs  
- Future scalability  

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

# 🔄 Sequence Diagrams for API Calls  
## 🧩 Overview  

This section provides sequence diagrams that explain how the HBnB system handles major API calls and how data flows between layers during each operation.  
These diagrams help visualize the internal workflow of the application and clarify how different components collaborate to process user requests.

---

# 5.1 User Registration

---

![Sequence Diagram (User Registration)](https://raw.githubusercontent.com/Norahxj/holbertonschool-hbnb/refs/heads/main/part1/Sequence%20Diagram%20(User%20Registration).png)

---

The **User Registration** sequence diagram provides a detailed view of how a new user account is created within the HBnB system.  
The process begins at the **Presentation Layer**, where the user fills out the registration form on the web page. Before any data is sent to the server, the page performs **client-side validation** to ensure that the input format is correct and required fields are not empty.

Once validated, the request is forwarded to the **API**, which acts as the entry point to the backend. The API then delegates the request to the **HBnBFacade**, the central coordinator of the Business Logic Layer.

Inside the **UserModel**, the system performs several critical operations:

- Parsing and sanitizing the input  
- Checking required fields  
- Querying the **UserRepository** to verify if the email already exists  
- Handling the two possible outcomes:
  - **Email already in use:** The system returns an error through the API, and the user sees a clear error message.
  - **Email is unique:** A new User object is created, the password is securely hashed, and the user is saved in the database.

The **Persistence Layer** handles the actual database operations, including the SELECT and INSERT queries.  
Once the user is successfully stored, the success response travels back up through the layers until the user sees a confirmation message.

This diagram highlights the system’s emphasis on **security**, **data validation**, and **error handling**, ensuring a smooth and safe registration experience.

---

# 5.2 Place Creation

---

![Sequence Diagram (Place Creation)](https://raw.githubusercontent.com/Norahxj/holbertonschool-hbnb/refs/heads/main/part1/Sequence%20Diagram%20(Place%20Creation).png)

---

The **Place Creation** sequence diagram illustrates the workflow for adding a new place listing to the HBnB platform.  
The process begins when the user enters place details—such as name, description, price, and location—into the dedicated creation page.

The request is sent to the **API**, which forwards it to the **HBnBFacade** for validation and processing.  
This diagram emphasizes two major validation steps:

1. **Permission Validation**  
   The system checks whether the user is authorized to create a place. Unauthorized attempts immediately trigger an error response.

2. **Field Validation**  
   The system ensures that all required fields are present and correctly formatted.

If any validation fails, the API returns a **400 Failure response**, and the user is shown an error message.  
If the data is valid, the **PlaceModel** creates a new Place object and sends it to the **PlaceRepository**, which performs the INSERT operation into the database.

Once the database confirms the insertion, the success response travels back through the layers, and the user receives a **201 Place Created** confirmation.

This diagram demonstrates how the system enforces **data integrity**, **authorization rules**, and **robust error handling**.

---

# 5.3 Review Submission

---

![Sequence Diagram (Review Submission)](https://raw.githubusercontent.com/Norahxj/holbertonschool-hbnb/refs/heads/main/part1/Sequence%20Diagram%20(Review%20Submission).png)

---

The **Review Submission** sequence diagram explains how users submit reviews for places they have visited.  
The process begins when the user writes a review on the Review Page, which sends the review data to the API.

The **HBnBFacade** handles the business logic, starting with:

- **Rating Validation:** Ensuring the rating is within acceptable limits.  
  Invalid ratings immediately trigger an error response.

- **Place Existence Check:**  
  The system verifies that the place being reviewed actually exists by querying the database.

If the place exists and the review is valid, the **ReviewModel** creates a Review object and sends it to the **ReviewRepository**, which inserts it into the database.

Once the review is saved, the user receives a **201 Review Submitted** confirmation.

This diagram highlights the system’s commitment to:

- Preventing invalid or malicious reviews  
- Ensuring reviews are tied to real places  
- Maintaining data consistency across layers  

---

# 5.4 Fetching a List of Places

---

![Sequence Diagram (Fetching a List of Places)](https://raw.githubusercontent.com/Norahxj/holbertonschool-hbnb/refs/heads/main/part1/Sequence%20Diagram%20(User%20Registration).png)

---

The **Fetching a List of Places** sequence diagram describes how users search for available places using filters such as location, price range, or amenities.

The search request is submitted through the search page and forwarded to the API.  
The **HBnBFacade** coordinates the retrieval process by querying the **PlaceRepository**, which interacts with the database to fetch matching results.

Two outcomes are shown:

1. **Matching Places Found:**  
   The results are formatted and returned to the user.

2. **No Matches:**  
   The system returns an empty list, and the user interface displays a friendly “No results found” message.

This diagram demonstrates how the system supports efficient searching while maintaining a clean separation between layers.

---

# 6. Conclusion

The diagrams collectively provide a comprehensive view of how the HBnB Evolution system handles user registration, place creation, review submission, and place searching.  
Each diagram reinforces the system’s architectural principles:

- Clear separation between Presentation, Business Logic, and Persistence layers  
- Strong validation and error handling  
- Secure data processing  
- Consistent communication flow across components  

This documentation serves as a solid reference for developers, testers, and future contributors.

---

# ✨ 7. Acknowledgments

This documentation was collaboratively created as part of the HBnB Evolution project.  
Every diagram, architectural decision, and written explanation reflects the combined effort and teamwork invested throughout the design phase.

## 👩‍💻 Contributors  
We proudly acknowledge the team members who contributed to the creation of this documentation:

- **Maryam Al-Malki**  
- **Manar Al-Thaqafi**  
- **Noura Al-Juhani**

Their dedication to clarity, structure, and technical accuracy played a key role in producing a comprehensive and professional system blueprint.
