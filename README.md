# 🏠 HBnB Evolution Project

This project is part of the Holberton School curriculum.  
It demonstrates the progressive evolution of a layered backend architecture — from UML system design to full business logic implementation.

The project is structured into multiple parts, each building on the previous one.

---

# 📘 Part 1: System Design & UML Documentation

In Part 1, we focused on designing the complete system architecture before writing any implementation code.

This phase included:

- High-Level Package Diagram
- Detailed Class Diagram
- Sequence Diagrams
- Definition of system entities and relationships
- Layered architecture planning

### 🎯 Objective

To clearly define:

- Entities (User, Place, Review, Amenity)
- Relationships between entities
- Layer responsibilities
- Data flow between components

This ensured that implementation in the next phase strictly followed a structured architectural plan.

---

# 🚀 Part 2: Business Logic Implementation

In Part 2, we transitioned from system design to actual implementation.

This phase focused on building the core domain logic of the HBnB system while respecting the layered architecture defined in Part 1.

---

## ✅ What Was Implemented

### Core Models
- BaseModel (UUID generation + timestamps)
- User model
- Place model
- Review model
- Amenity model

### Architecture Components
- Facade pattern to centralize business operations
- Repository pattern for data persistence
- Layer separation (API / Business / Persistence)

### Validation Logic
- Foreign key validation (user_id, place_id)
- Required field validation
- Error handling with proper HTTP status codes

---

## 🏗 Applied Architecture

The system strictly follows a layered architecture:

- API Layer → Handles HTTP requests and responses
- Business Logic Layer → Contains domain rules and models
- Persistence Layer → Manages data storage via Repository pattern

Each layer has a single responsibility and communicates only with the layer directly below it.

This structure ensures:

- Maintainability
- Scalability
- Clear separation of concerns
- Clean system evolution

---

## 🧪 Testing & Validation

During Part 2:

- All entities were tested via API endpoints
- CRUD operations were validated
- Error scenarios were tested:
  - 400 → Missing or invalid data
  - 404 → Non-existent resources
  - 201 → Successful creation
  - 200 → Successful retrieval
  - 204 → Successful deletion
- Swagger was used to verify endpoint registration and behavior

All test results matched the intended system design.

---

# 👩‍💻 Team Contributions

- Mariam — High-Level Package Diagram & Project Structure  
- Manar — Detailed Class Diagram & User Implementation  
- Norah — Sequence Diagrams & Entity Integration  

---

# 🔮 Next Parts

The next phases of the project will expand into:

- Database integration  
- Full persistence layer implementation  
- Advanced API features  
- Authentication and authorization  

---

# 📌 Conclusion

HBnB Evolution demonstrates a structured backend development approach:

Design → Architecture → Implementation → Validation  

Each phase builds upon the previous one to ensure a clean, scalable, and maintainable system.
