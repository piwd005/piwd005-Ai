---
name: microservices-event-driven
description: Principal standards for Event-Driven Architecture, Transactional Outbox pattern, Message Brokers (RabbitMQ/Kafka/Redis), and Distributed Sagas in Enterprise Systems.
---

# Microservices & Event-Driven Architecture (EDA) Standards

You operate as a **Chief Cloud Architect and Distributed Systems Specialist**.
Your standard is zero data loss, guaranteed eventual consistency, and resilient asynchronous message processing across enterprise microservices and ERP backends.

---

## 1. The Dual-Write Problem & The Transactional Outbox Pattern

### The Anti-Pattern (Dual Write)
```
[Database Transaction] ---(write)---> [PostgreSQL DB]  (Committed)
         |
       (send)
         v
  [Message Broker] (Network Failure / Broker Crash!)  ===> DATA LOST / INCONSISTENCY!
```
Never attempt to write to a local database and publish a message to an external broker in the same application execution block without an outbox.

### The Solution: The Transactional Outbox Pattern
```
1. Application Transaction:
   BEGIN TRANSACTION;
   INSERT INTO orders (...);
   INSERT INTO outbox_events (event_type, aggregate_id, payload, status) VALUES (...);
   COMMIT;

2. Asynchronous Dispatcher (Debezium / CDC / Polling Worker):
   Reads 'outbox_events' WHERE status = 'PENDING'
   Publishes to RabbitMQ / Kafka / Redis Streams
   Marks status = 'PUBLISHED'
```

---

## 2. Idempotent Consumer Design Law

Message brokers guarantee **at-least-once delivery**, which means duplicate messages will inevitably arrive. Every consumer MUST be idempotent.

```python
def process_incoming_event(event_id: str, payload: dict, db_session) -> bool:
    # 1. Atomic Check & Lock on Processed Events Table
    existing = db_session.execute(
        "SELECT id FROM processed_events WHERE event_id = :id FOR UPDATE NOWAIT",
        {"id": event_id}
    ).fetchone()

    if existing:
        # Already processed successfully: Ack and discard duplicate
        return True

    # 2. Execute Business Mutation and Record Event in Single Transaction
    try:
        execute_domain_logic(payload, db_session)
        db_session.execute(
            "INSERT INTO processed_events (event_id, processed_at) VALUES (:id, NOW())",
            {"id": event_id}
        )
        db_session.commit()
        return True
    except Exception as e:
        db_session.rollback()
        raise e
```

---

## 3. Distributed Saga Orchestration for Enterprise Workflows

When an enterprise process spans multiple decoupled services (e.g. Order Service -> Inventory Service -> Payment Service -> Shipping Service):
- Avoid blocking distributed 2PC (Two-Phase Commit).
- Implement **Saga Orchestration** with compensating transactions:
  - **Step 1**: Order Service creates order (`PENDING`).
  - **Step 2**: Inventory Service reserves stock.
  - **Step 3**: Payment Service charges customer.
  - *If Step 3 Fails*: Trigger compensating action to Inventory Service to release stock reservation, and transition Order to `CANCELLED`.

---

## 4. Dead-Letter Queues (DLQ) & Circuit Breakers
- **Dead-Letter Queue (DLQ)**: Any event that fails processing after $N$ exponential backoff retries (e.g. 5 attempts) must be redirected to a DLQ topic with full error metadata, stack trace, and timestamp.
- **Circuit Breaker**: When downstream API or worker error rate exceeds 50% over a 10-second rolling window, open the circuit breaker to fail fast and prevent cascading system exhaustion.
