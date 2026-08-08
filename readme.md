<div align="center">

# Cogentra

**An AI chat platform backend, structured in independently evolving layers.**

FastAPI · Pydantic v2 · SQLAlchemy — status: active development

[Overview](#overview) · [System Modules](#system-modules) · [Where Things Stand Today](#where-things-stand-today) · [What's Ahead](#whats-ahead)

</div>

---

## Overview

Cogentra is a backend for an AI chat application, built under one constraint: understand a layer fully before adding the next. The system is organized as a small number of independent modules — domain modeling, API surface, business logic, error handling, and persistence — each introduced at a different stage of the project's development and each replaceable without rewriting the others.

The long-term aim is a platform capable of real conversational AI, retrieval-augmented generation, and agentic workflows. The modules below reflect what's actually built toward that so far, not the destination itself.

> **Status note:** This is a solo, in-progress project. [Where Things Stand Today](#where-things-stand-today) is written to be explicit about which modules are functionally complete and which are scaffolding.

---

## System Modules

### 01 · Domain & Validation Layer

The foundation of the system, and the part that predates the web framework entirely. Core entities — user, chat, message, AI response — are defined as Pydantic v2 models rather than plain data classes, which means validation is a property of the object itself and not something re-implemented at every entry point. Field-level validators enforce invariants (non-empty identifiers, bounded message length, well-formed email addresses), a computed field derives values that shouldn't be stored redundantly, and strict schema configuration rejects any field the model doesn't explicitly define. This layer is deliberately framework-agnostic — it has no knowledge of HTTP.

### 02 · API Layer

Built on FastAPI, with the routing surface segmented by domain concern rather than centralized into one router — users, chats, messages, and administrative views are each owned by their own module. Requests and responses are described by dedicated schema classes, kept distinct from the domain models above so the external contract can evolve independently of internal representation. Shared request-time context — the resolved current user, the resolved chat, the resolved message — is supplied through the framework's dependency-injection graph rather than re-derived in each handler, and that same dependency graph is what drives the auto-generated OpenAPI documentation.

### 03 · Service Layer

Business rules — what makes a chat a duplicate, what a valid rename looks like, how a message gets edited — live in dedicated service classes, one per domain area, sitting between the API layer and the domain models. Routers call services; services have no awareness of HTTP status codes or request objects. This boundary is what lets the routing layer stay thin and lets business logic be reasoned about independently of the transport mechanism carrying it.

### 04 · Error Handling & Observability

Failure is modeled as a first-class concern rather than an afterthought. A hierarchy of typed, domain-specific exceptions distinguishes a missing user from a missing chat from a missing message, and each is caught by a global exception-handling layer registered against FastAPI's exception hooks. Every handled exception — and any unhandled one, as a fallback — is normalized into the same JSON error envelope: a stable error code, a human-readable message, and a request identifier. That identifier is generated per-request by a middleware layer that also measures request latency, both surfaced back to the client through response headers, so failures remain traceable after the fact.

### 05 · Persistence Layer — *in progress*

The system currently runs on process-local state held directly on the domain models — nothing survives a restart. A persistence module is being built in parallel rather than bolted on: a database engine, a session factory, and a declarative ORM base are in place, with one ORM-mapped entity implemented and exercised in isolation. The intended migration is incremental — moving each service's state onto this layer one at a time — rather than a single cutover that would require rewriting the modules above it simultaneously.

---

## Where Things Stand Today

- Authentication isn't implemented yet — the API currently resolves every request against a single fixed identity supplied through dependency injection, not a real per-request authenticated user.
- Chat and message state is held entirely in memory on the domain models and does not persist across process restarts.
- The persistence module (engine, session factory, declarative base) exists but isn't yet consumed by any service or router.
- AI response generation currently returns static placeholder output rather than a real model call.
- Domain validation is enforced at object construction time but isn't consistently re-applied when an existing object is later mutated.
- No automated test suite exists yet.

---

## What's Ahead

- Migrate each service's in-memory state onto the persistence layer, incrementally rather than all at once
- Replace the fixed dependency-injected identity with real authentication and per-user authorization
- Externalize configuration — currently hardcoded — into environment-driven settings
- Replace placeholder AI response generation with an actual model integration
- Introduce an automated test suite, containerization, and CI
- Layer retrieval-augmented generation and agentic workflows on top of the modules above

---

## Contributing

This is currently a solo project documenting the path toward a production-style AI backend. Feedback, questions, and suggestions on direction are welcome via GitHub.

## License

No license file is currently included, so all rights are reserved by default. If the project starts accepting outside contributions or reuse, adding an OSI-approved license is a reasonable next step.

## Author

**Rajat Krishnan** — [@rajatkrish07](https://github.com/rajatkrish07)
