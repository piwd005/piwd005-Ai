---
name: universal-database-architect
description: >-
  Lead Database Architect & DBA expertise for PostgreSQL, MySQL, Redis, and distributed
  data stores. Covers query plan optimization (EXPLAIN ANALYZE), B-Tree / GIN / GiST indexing,
  zero-downtime schema migrations, foreign key indexing, deadlock prevention, table partitioning,
  connection pooling (PgBouncer), and multi-tenant database isolation. Use when designing
  data schemas, tuning slow queries, or resolving database lock contention.
---

# Lead Database Architect & DBA Handbook

Design high-throughput, enterprise-scale database architectures that guarantee ACID transactions, sub-millisecond query execution, and zero downtime.

---

## 1. High-Performance Indexing Strategy

1. **Foreign Key Indexing**:
   - Every `FOREIGN KEY` constraint column MUST have a supporting B-tree index in PostgreSQL/MySQL. Unindexed foreign keys cause full table locks on parent `DELETE` or `UPDATE` cascades.
2. **Composite Indexes (Left-Prefix Rule)**:
   - When indexing multiple columns `(tenant_id, status, created_at)`:
     - Place equality columns first (`tenant_id`, `status`).
     - Place range or sort columns last (`created_at`).
3. **Partial Indexes**:
   - Use partial indexes for skewed boolean or status flags:
     ```sql
     CREATE INDEX idx_orders_unprocessed ON orders (created_at) WHERE status = 'pending';
     ```
4. **GIN / GiST Indexes for Search and Vectors**:
   - Use GIN indexes for JSONB keys (`USING gin (metadata jsonb_path_ops)`).
   - Use HNSW or IVFFlat for vector embeddings via `pgvector`.

---

## 2. Zero-Downtime Schema Migrations

1. **Never Run Blocking DDL**:
   - In PostgreSQL, never add a column with a non-constant dynamic default (`DEFAULT clock_timestamp()`) without safe staged steps.
   - Never create indexes synchronously on large tables: always use `CREATE INDEX CONCURRENTLY`.
2. **Safe Migration Sequence for Column Renames**:
   - Step 1: Add new column (nullable).
   - Step 2: Dual-write in application code to both old and new columns.
   - Step 3: Backfill existing data in small batches (`LIMIT 1000`).
   - Step 4: Switch application reads to new column.
   - Step 5: Deprecate and safely drop old column in a subsequent release.

---

## 3. Query Plan Optimization (EXPLAIN ANALYZE)

- Look for `Seq Scan` on tables with > 10,000 rows.
- Look for high `Buffers: shared hit=... read=... dirtied=...`.
- Eliminate nested loops on large datasets: encourage hash joins or index scans.
