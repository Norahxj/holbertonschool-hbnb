# Part 1: Technical Documentation

## 0. High-Level Package Diagram

### Objective
The objective of this task is to create a high-level package diagram that illustrates the three-layer architecture of the HBnB application and the communication between these layers using the Facade design pattern. This diagram provides a conceptual overview of how the application is structured and how its main components interact.

---

### Description
The HBnB application follows a layered architecture composed of three main layers:

- **Presentation Layer (Services, API):**  
  This layer manages all interactions between users and the application. It exposes APIs and services that handle incoming requests and outgoing responses.

- **Business Logic Layer (Models):**  
  This layer contains the core business logic of the application. It includes the main models representing the system’s entities, such as User, Place, Review, and Amenity.

- **Persistence Layer:**  
  This layer is responsible for data storage and retrieval. It interacts directly with the database through repositories or data access components.

Communication between layers is structured and controlled using the **Facade Pattern**, which provides a unified interface between the Presentation Layer and the Business Logic Layer. This approach simplifies interactions and enforces separation of concerns.

---

### High-Level Package Diagram

The following UML package diagram represents the three-layer architecture of the HBnB application and the communication pathways between them:

classDiagram
class PresentationLayer {
    API
    Services
}

class BusinessLogicLayer {
    User
    Place
    Review
    Amenity
}

class PersistenceLayer {
    Repositories
}

PresentationLayer --> BusinessLogicLayer : Facade Pattern
BusinessLogicLayer --> PersistenceLayer : Database Operations

