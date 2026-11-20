---
name: odoo-performance-database
description: >-
  Senior Developer Guide for High-Performance Odoo Database Architecture & ORM Optimization.
  Covers eliminating N+1 queries, bulk data processing, indexing strategies, _read_group mastery,
  safe raw SQL with odoo.tools.SQL and parameterized psycopg2, multi-company isolation,
  memory-safe recordset batching, and database locks.
  Use when designing high-volume data models, diagnosing slow queries, or writing batch integrations.
---

# High-Performance Odoo Database & ORM Optimization (Odoo 19 & 20)

Architectural handbook for database efficiency, index design, query optimization, and memory management in high-throughput Odoo environments.

---

## 1. Eliminating the N+1 Query Anti-Pattern

### ❌ The Junior Mistake: ORM Operations in Loops
```python
# Disastrous performance: N queries to read + N queries to write!
for order in orders:
    partner = self.env['res.partner'].search([('id', '=', order.partner_id.id)])
    order.write({'customer_email': partner.email})
```

### ✅ The Senior Solution: Batch ORM
```python
# 1 query for all records, 1 batch update
partner_emails = {p.id: p.email for p in orders.partner_id}
for order in orders:
    order.customer_email = partner_emails.get(order.partner_id.id, False)
```

---

## 2. Advanced Indexing Strategies

PostgreSQL indexes are essential for high-volume models (e.g. `account.move.line`, `stock.move`, `pos.order`).

### A. Field Indexing
```python
# Simple B-tree index
reference = fields.Char(string="Reference", index=True)

# Trigram / Partial / Unaccent Indexing (PostgreSQL)
# For models with heavy text search:
def init(self):
    super().init()
    self.env.cr.execute("""
        CREATE INDEX IF NOT EXISTS idx_sale_order_name_trgm 
        ON sale_order USING gin (name gin_trgm_ops);
    """)
```

### B. Composite Multi-Column Indexes
When queries frequently filter by multiple fields together (e.g. `state` + `company_id` + `date`):
```python
class StockMove(models.Model):
    _inherit = 'stock.move'

    _sql_constraints = [
        ('uniq_reference_company', 'unique(reference, company_id)', 'Reference must be unique per company!'),
    ]

    def init(self):
        super().init()
        self.env.cr.execute("""
            CREATE INDEX IF NOT EXISTS idx_stock_move_comp_state_date
            ON stock_move (company_id, state, date);
        """)
```

---

## 3. High-Performance Aggregations with `_read_group`

Never load thousands of records into Python RAM to compute totals or counts. Use `_read_group`:

```python
# Computes totals in a single SQL query:
groups = self.env['account.move.line']._read_group(
    domain=[('move_id.state', '=', 'posted'), ('account_id.account_type', '=', 'income')],
    groupby=['partner_id', 'date:month'],
    aggregates=['balance:sum', 'id:count'],
)
for partner, month, total_balance, line_count in groups:
    # Process aggregated rows with zero memory footprint
    pass
```

---

## 4. Parameterized SQL with `odoo.tools.SQL`

When raw SQL is strictly required for high-speed bulk inserts or complex CTEs:
- **Never** interpolate strings (`%`, `.format()`, f-strings).
- Always use parameterized queries or `odoo.tools.SQL`.

```python
from odoo.tools import SQL

# Safe Identifier and Parameterized Values
query = SQL(
    "SELECT id, %(col)s FROM %(table)s WHERE company_id = %(company_id)s AND state = %(state)s",
    table=SQL.identifier('sale_order'),
    col=SQL.identifier('amount_total'),
    company_id=self.env.company.id,
    state='sale',
)
self.env.cr.execute(query)
results = self.env.cr.fetchall()
```

---

## 5. Memory-Safe Chunking for Massive Datasets

When importing or processing 50,000+ records, prevent Out-Of-Memory (OOM) crashes by chunking and clearing the ORM cache:

```python
CHUNK_SIZE = 2000

def process_large_dataset(self):
    domain = [('state', '=', 'draft'), ('processed', '=', False)]
    total_count = self.search_count(domain)

    # Process in slices using offset
    for offset in range(0, total_count, CHUNK_SIZE):
        records = self.search(domain, offset=0, limit=CHUNK_SIZE)
        if not records:
            break

        # Business logic inside transaction savepoint
        with self.env.cr.savepoint():
            records._process_batch()
            records.write({'processed': True})

        # Evict processed records from Python memory
        self.env.invalidate_all()
```
