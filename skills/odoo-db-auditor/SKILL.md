---
name: odoo-db-auditor
description: "Principal-grade Odoo & PostgreSQL Database Health, Schema Drift, Foreign Key Indexing, and Data Integrity Auditor. Inspects unindexed relational fields, orphaned XML IDs, double-entry financial ledger balancing, stock valuation layer consistency, multi-company leaks, and PostgreSQL lock contention."
---

# Odoo Database Health & Integrity Auditor (Principal Standard)

This skill provides comprehensive diagnostics and automated verification for Odoo databases across PostgreSQL system catalogs and Odoo ORM models.

---

## 1. Core Audit Vectors

### A. Missing Foreign Key Indexes (Performance & Deadlock Prevention)
In PostgreSQL, foreign keys without indexes cause full table scans on referenced tables during updates and deletes, leading to severe lock contention and deadlocks (`SELECT FOR UPDATE`).
- **Rule**: Every `Many2one` relational field on high-volume models (e.g. `sale.order.line`, `account.move.line`, `stock.move`, `custom.*`) MUST have a corresponding B-Tree index (`index=True` in field definition or explicit PostgreSQL index).
- **Audit Query**:
  ```sql
  SELECT
      c.conrelid::regclass AS table_name,
      a.attname AS column_name,
      c.conname AS foreign_key_name
  FROM pg_constraint c
  JOIN pg_attribute a ON a.attnum = ANY(c.conkey) AND a.attrelid = c.conrelid
  WHERE c.contype = 'f'
    AND NOT EXISTS (
        SELECT 1 FROM pg_index i
        WHERE i.indrelid = c.conrelid
          AND a.attnum = i.indkey[0]
    )
    AND c.conrelid::regclass::text NOT LIKE 'pg_%'
  ORDER BY table_name, column_name;
  ```

### B. Schema Drift Detection (Python vs PostgreSQL Catalog)
Verifies if fields declared in Python models actually exist in the physical PostgreSQL database table:
- Detects columns missing due to failed migrations or aborted module upgrades.
- Detects column type mismatches (e.g. `varchar` vs `integer`, `boolean` vs `varchar`).

### C. Orphaned XML External IDs (`ir.model.data`)
Orphaned records in `ir.model.data` cause module upgrade crashes (`KeyError`, `MissingError`) and broken menu references:
- Audit: Check `ir.model.data` entries where `res_id` points to an ID that no longer exists in the target model's database table.

### D. Financial & Double-Entry Ledger Integrity
In any ERP, financial integrity is non-negotiable:
- **Balanced Debits and Credits**: In `account.move.line`, every posted journal entry must have `sum(debit) == sum(credit)`.
- **Orphaned Move Lines**: Check lines where `move_id` does not exist in `account.move`.
- **Company Mismatch**: Move lines must strictly match the `company_id` of their parent move.

### E. Inventory Valuation Layer (`stock.valuation.layer`) Integrity
For AVCO and FIFO costing:
- Check for zero or negative unit costs on incoming stock moves.
- Check `stock.valuation.layer` records where `value` or `quantity` is out of sync with corresponding `stock.move`.
- Ensure stock input/output clearing accounts balance with physical quant counts.

### F. Multi-Company & Multi-Branch Segregation Leaks
Audit records for `check_company=True` violations:
- Child records linked to a parent record of a different `company_id` (e.g., `sale.order.line` company != `sale.order` company).
- Partner commercial company mismatches.

### G. PostgreSQL Active Locks & Blocked Transactions
Diagnoses live deadlocks and lock contention:
- Check `pg_locks` and `pg_stat_activity` for `ExclusiveLock`, `RowShareLock`, and transactions in `idle in transaction` state.

---

## 2. Using the Database Auditor Tool

Execute live database health audits via the `odoo_audit_database` tool or CLI:
```bash
odoo-dev db-audit --db mydb --user admin --password admin
```
This automatically runs all 7 inspection vectors and returns a prioritized health scoreboard.
