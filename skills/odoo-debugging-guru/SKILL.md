---
name: odoo-debugging-guru
description: >-
  Principal-level diagnostics and issue resolution for Odoo systems.
  Covers tracing PostgreSQL deadlocks, diagnosing slow queries with EXPLAIN ANALYZE,
  profiling worker memory leaks, eliminating cache invalidation loops, and resolving
  OWL component reactivity bugs. Use when diagnosing tough production crashes,
  database lock contention, slow page loads, or complex framework bugs.
---

# Principal Odoo Debugging & Performance Diagnostics Guide

Advanced troubleshooting methodologies for diagnosing and fixing the most complex production failures in Odoo 18, 19, and 20.

---

## 1. PostgreSQL Deadlocks & Row Lock Contention

### Symptoms
- `psycopg2.errors.DeadlockDetected: deadlock detected`
- `could not obtain lock on row in relation "sale_order"`

### Root Causes & Principal Fixes
1. **Inconsistent Lock Ordering**:
   - Transaction A locks Order 1 then Order 2.
   - Transaction B locks Order 2 then Order 1 $\rightarrow$ Deadlock!
   - **Fix**: Always sort record IDs before locking:
     ```python
     # Principal Standard: Sort IDs to guarantee consistent locking order
     sorted_ids = sorted(records.ids)
     self.env.cr.execute("SELECT id FROM sale_order WHERE id IN %s ORDER BY id FOR UPDATE", [tuple(sorted_ids)])
     ```
2. **Holding Locks During External HTTP Calls**:
   - Never run `requests.post()` inside an active transaction that holds locks.
   - **Fix**: Move external API calls to background cron or commit transaction before calling external service.

---

## 2. Diagnosing Slow ORM Queries with `EXPLAIN ANALYZE`

When a list view or report takes more than 500ms to load:

1. **Log SQL Queries**:
   - Run Odoo with `--log-sql` or profile in `psql`:
     ```sql
     EXPLAIN (ANALYZE, BUFFERS)
     SELECT id, name, partner_id, state 
     FROM sale_order 
     WHERE company_id = 1 AND state = 'sale' 
     ORDER BY date_order DESC LIMIT 80;
     ```
2. **Identify Sequential Scans (`Seq Scan`)**:
   - If `Seq Scan` is occurring on a table with >10,000 rows, a B-tree index is missing.
3. **Add Composite B-tree Index**:
   ```python
   def init(self):
       super().init()
       self.env.cr.execute("""
           CREATE INDEX IF NOT EXISTS idx_sale_order_perf
           ON sale_order (company_id, state, date_order DESC);
       """)
   ```

---

## 3. Worker Memory Leaks & OOM Prevention

### Symptoms
- Odoo workers killed by Linux OOM killer (`Killed`, Exit code 137).
- Worker memory climbing steadily after batch imports.

### Principal Fix: Memory-Safe Recordset Batching
```python
BATCH_SIZE = 1000

def process_massive_dataset(self):
    domain = [('state', '=', 'draft'), ('processed', '=', False)]
    total = self.search_count(domain)

    for offset in range(0, total, BATCH_SIZE):
        records = self.search(domain, offset=0, limit=BATCH_SIZE)
        if not records:
            break

        # Isolate batch in savepoint
        with self.env.cr.savepoint():
            records._execute_batch_action()
            records.write({'processed': True})

        # CRITICAL: Evict records from Python memory to prevent OOM
        self.env.invalidate_all()
```

---

## 4. Frontend OWL Reactivity & Infinite Render Loops

### Symptoms
- Browser tab freezes with `Maximum call stack size exceeded`.
- Network tab shows thousands of repeated RPC calls.

### Root Causes & Principal Fixes
1. **Mutating State Inside Getter or Render**:
   - Calling `this.state.x = y` inside a getter causes an infinite re-render loop.
   - **Fix**: Only mutate state in user events (`t-on-click`) or lifecycle hooks (`onWillStart`, `onWillUpdateProps`).
2. **Missing `t-key` in `t-foreach`**:
   - Rendering lists without a unique `t-key` causes OWL DOM reconciliation corruption.
   - **Fix**: Always specify `t-key="item.id"`:
     ```xml
     <tr t-foreach="state.items" t-as="item" t-key="item.id">
         <td><t t-esc="item.name"/></td>
     </tr>
     ```
