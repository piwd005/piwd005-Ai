---
name: odoo-solution-architect
description: >-
  Senior Odoo Solution Architect expertise for enterprise ERP system design,
  modular decoupling, multi-company/multi-currency architecture, high-throughput scaling,
  asynchronous queue processing, external API integrations (REST, Webhooks, EDI),
  and long-term upgradeability. Use when designing complex multi-module systems,
  architecting high-scale databases, or planning enterprise integrations.
---

# Senior Odoo Solution Architect Handbook

Architect enterprise-grade Odoo systems that scale cleanly, isolate multi-company data, process high-volume transactions asynchronously, and maintain 100% upgrade stability.

---

## 1. Modular Decoupling Architecture

Never bundle all business logic, third-party integrations, and UI customization into a single monolithic addon. Use a layered architecture:

```text
Layer 4: UI & Reports        my_addon_theme / my_addon_reports
Layer 3: Business Workflows  my_addon_operations (extends core models)
Layer 2: External Connectors my_addon_connector (API client, webhook listeners)
Layer 1: Core Data Models    my_addon_core (abstract models, sequence, base master data)
```

- **Clean Dependencies**: Downward dependencies only. Core should never depend on UI or reporting.
- **Hook Extension Points**: Expose public extension points (`_prepare_*_vals()`, `_get_applicable_rules()`) that downstream modules can override using `super()`.

---

## 2. Multi-Company & Multi-Branch Architecture

In enterprise Odoo, multi-company isolation must be designed into every data model from Day 1:

1. **Company Field Declaration**:
   ```python
   company_id = fields.Many2one(
       'res.company',
       string='Company',
       required=True,
       default=lambda self: self.env.company,
       index=True,
   )
   ```
2. **Relational Field Guarding (`check_company=True`)**:
   Always declare `check_company=True` on relational fields so Odoo's ORM prevents cross-company data pollution:
   ```python
   partner_id = fields.Many2one('res.partner', string='Partner', check_company=True)
   warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', check_company=True)
   ```
3. **Record Rules**:
   Include standard multi-company record rules in `security/security.xml`:
   ```xml
   <record id="rule_my_model_multi_company" model="ir.rule">
       <field name="name">My Model Multi-Company</field>
       <field name="model_id" ref="model_my_model"/>
       <field name="domain_force">['|', ('company_id', '=', False), ('company_id', 'in', company_ids)]</field>
   </record>
   ```

---

## 3. High-Throughput & Asynchronous Integration Patterns

When integrating with external e-commerce, ERPs, or payment gateways handling thousands of requests:
- **Never perform synchronous HTTP calls inside database transactions**. If the remote endpoint hangs, PostgreSQL table locks persist, blocking all active users.
- **Use Dedicated Queue / Job Scheduling**:
  1. Save incoming webhook payload into a staging table (`my.webhook.event`) in a lightweight transaction.
  2. A scheduled cron or queue worker picks up pending events, processes them in isolated batches with savepoints, and marks status (`done`, `error`).
- **Database Locks**:
  - Never use raw `SELECT FOR UPDATE` on core tables (`sale_order`, `stock_picking`) without strict timeout and ordering to avoid deadlocks.

---

## 4. REST APIs and Webhook Design

When building APIs in Odoo:
- Use `@http.route` with `type='json'` or `type='http'`, `auth='api_key'` or `auth='user'`.
- Validate all incoming payloads against schemas before invoking ORM operations.
- Return standard HTTP status codes (`200 OK`, `201 Created`, `400 Bad Request`, `401 Unauthorized`, `404 Not Found`).
- Whitelist writable fields — never pass raw `request.httprequest.json` or `post` directly to `create()` or `write()`.
