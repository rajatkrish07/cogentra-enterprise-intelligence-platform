# Cogentra

## Enterprise Workspace Prototype

Cogentra is a backend-focused product development project built to learn and apply structured backend engineering practices around a real product domain.

The project evolved from a simple in-memory FastAPI prototype into a database-backed layered application using:

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* SQLite
* Uvicorn
* Git

The project also applies architectural patterns such as Dependency Injection, Service Layer, Repository Pattern, and centralized exception handling.

Cogentra is intentionally kept focused. Its purpose is to demonstrate the progression from a simple prototype to a structured, persistent backend with a usable product interface.

---

# Project Purpose

Cogentra was built primarily as a backend and product-development learning project.

The project covers:

* REST API development
* FastAPI application structure
* Pydantic request/response models
* SQLAlchemy ORM
* SQLite persistence
* Dependency Injection
* Service Layer architecture
* Repository Pattern
* Domain-level exception handling
* Centralized HTTP exception handling
* Database constraints
* Database migrations with Alembic
* Separation of responsibilities
* Frontend integration

The project intentionally avoids unnecessary infrastructure and feature expansion.

---

# Architecture

The current backend follows a layered architecture:

```text
Client
  |
  v
Router
  |
  | HTTP / request handling
  v
Service
  |
  | Business logic
  v
Repository
  |
  | Database access
  v
SQLAlchemy ORM
  |
  v
SQLite
```

Application-level exceptions are handled through a centralized exception boundary.

### Responsibilities

**Router**

* Handles HTTP concerns
* Receives requests
* Resolves dependencies
* Calls the appropriate service
* Returns response schemas

**Service**

* Contains business/application logic
* Applies business rules
* Coordinates repository operations

**Repository**

* Performs database operations
* Works with SQLAlchemy sessions
* Handles database persistence and retrieval

**SQLAlchemy ORM**

* Maps application entities to database tables

**SQLite**

* Provides persistent storage

**Exception Handlers**

* Translate application exceptions into structured HTTP responses

---

# Core Domain

Cogentra currently revolves around four main entities:

```text
User
 |
 +-- Chat
      |
      +-- Message
           |
           +-- AI Response
```

### User

Represents a Cogentra user.

### Chat

Represents an individual conversation/workspace belonging to a user.

A user can have multiple chats.

The same user cannot have duplicate chat titles.

### Message

Represents a message belonging to a chat.

Message text is intentionally not unique.

### AI Response

Represents a response associated with a message.

Multiple AI responses can belong to the same message, allowing response regeneration and response history.

Cogentra does not currently integrate with an external LLM provider. `AIResponse` is part of the product domain and persistence model.

---

# Technology Stack

| Technology | Role                                          |
| ---------- | --------------------------------------------- |
| Python     | Backend language                              |
| FastAPI    | REST API framework                            |
| Pydantic   | Request/response validation and serialization |
| SQLAlchemy | ORM and database access                       |
| SQLite     | Database                                      |
| Uvicorn    | ASGI application server                       |
| Alembic    | Database migrations                           |
| Git        | Version control                               |

---

# Database

Cogentra uses SQLite for persistent storage.

The main tables are:

```text
user_orm
    |
    +-- chats_orm
            |
            +-- messages_orm
                    |
                    +-- ai_response_orm
```

Important database constraints include:

* Unique username
* Unique email
* Unique `(user_id, title)` combination for chats
* Foreign keys between domain entities

Database schema evolution is handled through Alembic.

---

# Dependency Injection

FastAPI dependencies are responsible for constructing and injecting request-scoped resources.

The dependency flow is:

```text
Database Session
      |
      +--------------------+
      |          |         |
      v          v         v
 UserRepo    ChatRepo   MessageRepo ...
      |          |         |
      v          v         v
 UserService ChatService MessageService ...
      |
      v
    Router
```

The database session is created by the database dependency and passed into repositories.

Repositories do not create their own sessions.

---

# Exception Handling

Cogentra separates application-level errors from HTTP concerns.

Examples of domain exceptions include:

* `UserNotFoundError`
* `ChatNotFoundError`
* `MessageNotFoundError`
* `AIResponseNotFoundError`
* `DuplicateEmailError`
* `DuplicateChatError`
* `NoEmailChangeError`
* `ChatRenameError`

The overall flow is:

```text
Service / Repository
        |
        v
Application Exception
        |
        v
Central Exception Handler
        |
        v
Structured HTTP Response
```

Database write failures are rolled back before being re-raised.

---

# AI Response Model

Although Cogentra does not currently connect to a real LLM, the application models AI responses as persistent entities.

A message may contain multiple responses:

```text
Message
 |
 +-- AIResponse #1
 |
 +-- AIResponse #2
 |
 +-- AIResponse #3
```

Regeneration creates a new persisted response instead of overwriting the previous response.

Response history is retrieved by `message_id` and ordered from newest to oldest.

---

# API Domain

The backend provides APIs around:

### Users

* User creation
* User retrieval
* User-related operations supported by the current backend

### Chats

* Create chat
* Retrieve chat
* Find chat by title
* Rename chat
* Delete chat

### Messages

* Create message
* Retrieve message
* Edit message
* Delete message

### AI Responses

* Generate response
* Regenerate response
* Retrieve response history

The exact request and response contracts are defined by the FastAPI routers and Pydantic schemas in the source code.

---

# Project Structure

```text
Cogentra/
|
+-- routers/
|   +-- users_router
|   +-- chats_router
|   +-- messages_router
|   +-- ai_response_router
|   +-- health
|
+-- services/
|   +-- user_service
|   +-- chat_service
|   +-- message_service
|   +-- ai_response_service
|
+-- repositories/
|   +-- user_repository
|   +-- chat_repository
|   +-- message_repository
|   +-- ai_response_repository
|
+-- database/
|   +-- database configuration
|
+-- models/
|   +-- SQLAlchemy ORM models
|
+-- schemas/
|   +-- request schemas
|   +-- response schemas
|
+-- dependencies/
|   +-- database/session dependencies
|   +-- repository dependencies
|   +-- service dependencies
|   +-- entity dependencies
|
+-- exceptions/
|   +-- domain exceptions
|
+-- alembic/
|
+-- main.py
```

Unused admin and debug functionality has been removed.

---

# Backend Status

The backend foundation is complete for the current project scope.

| Component                           | Status   |
| ----------------------------------- | -------- |
| FastAPI application                 | Complete |
| SQLite persistence                  | Complete |
| SQLAlchemy ORM                      | Complete |
| Repository pattern                  | Complete |
| User service/repository flow        | Complete |
| Chat service/repository flow        | Complete |
| Message service/repository flow     | Complete |
| AI response service/repository flow | Complete |
| Dependency Injection                | Complete |
| Domain exceptions                   | Complete |
| Centralized HTTP exception handling | Complete |
| Database transaction handling       | Complete |
| AI response history                 | Complete |
| Alembic migrations                  | Complete |
| Legacy in-memory architecture       | Removed  |
| Admin router                        | Removed  |
| Debug router                        | Removed  |

The backend is intentionally frozen at this stage.

---

# Frontend

The next and final product-development stage for Cogentra is a minimal frontend integrated with the existing FastAPI backend.

The frontend should represent the actual product domain:

```text
User
  |
  v
Chats
  |
  v
Messages
  |
  v
AI Responses
```

The intended interface is:

* Minimalistic
* Clean
* Professional
* Responsive
* Blue as the primary accent
* Light/neutral visual system
* Subtle transitions
* Simple workspace layout
* Not a ChatGPT clone

The frontend should support the backend capabilities that already exist, including:

* User/profile information
* Chat listing
* Create/select chat
* Rename/delete chat where supported
* Message creation
* Message editing/deletion where supported
* AI response generation
* AI response regeneration
* Response history

No fake AI capabilities or unsupported backend functionality should be introduced.

The frontend may be developed using AI-assisted tooling, with the existing backend remaining the source of truth for API behavior.

---

# Product Development Flow

Cogentra evolved through the following progression:

```text
Simple FastAPI Prototype
          |
          v
In-Memory Application
          |
          v
SQLAlchemy + SQLite
          |
          v
Repository Layer
          |
          v
Service Layer
          |
          v
Dependency Injection
          |
          v
Centralized Exception Handling
          |
          v
Tested Backend
          |
          v
Minimal Frontend
          |
          v
Cogentra Complete
```

---

# What Cogentra Taught

The project was intentionally used to understand how a small product evolves into a structured backend.

Key engineering lessons include:

* Separation of HTTP, business logic, and persistence
* Dependency Injection
* Request-scoped database sessions
* Repository responsibilities
* Service responsibilities
* ORM/database relationships
* Database constraints
* Transactions and rollbacks
* Domain exceptions
* Centralized error handling
* API contracts
* Persistence
* Migrations
* Frontend/backend integration

---

# Scope

Cogentra is intentionally not being expanded into a large enterprise platform.

Out of scope for the current project:

* Complex authentication systems
* Advanced RBAC
* Microservices
* Kubernetes
* Distributed infrastructure
* Real LLM integration
* RAG
* Agents
* Vector databases
* AI orchestration frameworks
* Unnecessary backend abstractions

These are intentionally outside Cogentra's scope.

The AI Engineering focus has moved to **CapitalMind AI**.

---

# Current Status

**Status: Backend Complete — Frontend Integration**

The backend has reached the intended learning milestone.

The remaining work is to connect a small, polished frontend to the existing API and complete the product prototype.

After the frontend integration is complete, Cogentra will be considered finished for its intended purpose.

---

# Related Project

**CapitalMind AI** is the flagship AI Engineering project that follows Cogentra.

While Cogentra focuses primarily on backend and product engineering, CapitalMind AI focuses on:

```text
LLMs
  ↓
Real-Time AI Chat
  ↓
RAG
  ↓
Embeddings
  ↓
Vector Databases
  ↓
Retrieval
  ↓
Tool Calling
  ↓
Basic Agents
  ↓
AI Evaluation
```

The two projects are intentionally kept separate so that each serves a different learning objective.
