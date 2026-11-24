---
name: universal-architect
description: >-
  Principal Systems Architect expertise for polyglot enterprise software engineering,
  C4 architectural modeling (Context, Container, Component, Code), microservices and
  modular monolith design, 12-factor cloud-native applications, distributed event-driven
  systems (Kafka, RabbitMQ), API gateways, and domain-driven design (DDD). Use when
  designing new systems, breaking monoliths, or creating architectural pre-flight blueprints.
---

# Principal Systems Architect Handbook

Architect zero-defect, high-throughput, cloud-native distributed systems and modular architectures across any programming language and technology stack.

---

## 1. The C4 Architectural Modeling Standard

Always formalize architecture using the C4 model before code is written:
1. **Context**: Who uses the system (users, third-party services) and boundaries.
2. **Container**: High-level technical choices (Frontend SPA, API Gateway, Microservice, DB, Cache, Worker).
3. **Component**: Internal structure of each container (Controllers, Services, Repositories, Domain models).
4. **Code**: Class diagrams, interfaces, and database schemas.

Use `super-dev blueprint <name> --type [fullstack|microservice|api]` to generate standard Mermaid diagrams.

---

## 2. The Twelve-Factor Cloud Architecture

Every production system must adhere to 12-Factor principles:
1. **Codebase**: One codebase tracked in revision control, many deploys.
2. **Dependencies**: Explicitly declare and isolate dependencies (e.g. `requirements.txt`, `package.json`, `go.mod`, `Cargo.toml`).
3. **Config**: Store configuration strictly in environment variables; zero hardcoded secrets.
4. **Backing Services**: Treat databases, caches, and queues as attached resources via connection URIs.
5. **Build, Release, Run**: Strictly separate build and run stages.
6. **Processes**: Execute apps as stateless processes; persist data only in backing stores.
7. **Port Binding**: Export services via port binding (FastAPI on 8000, Next.js on 3000, Gin on 8080).
8. **Concurrency**: Scale out via the process model (horizontal workers, replicas).
9. **Disposability**: Fast startup and graceful shutdown handling `SIGTERM`.
10. **Dev/Prod Parity**: Keep development, staging, and production as similar as possible using Docker.
11. **Logs**: Treat logs as event streams (structured JSON to stdout/stderr).
12. **Admin Processes**: Run administrative and migration tasks as one-off processes.

---

## 3. High-Concurrency & Concurrency Control

- **Optimistic Locking**: Use `version` or `updated_at` timestamps for low-contention entities.
- **Pessimistic Locking**: Use `SELECT FOR UPDATE` with sorted record IDs to prevent deadlocks in high-contention financial or inventory ledgers.
- **Idempotency**: Require `X-Idempotency-Key` on all state-mutating requests (`POST`, `PATCH`). Store keys in Redis with TTL.
