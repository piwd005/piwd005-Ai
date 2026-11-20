---
name: odoo-file-auditor
description: "Principal-grade Deep File Inspector for Odoo Addons. Audits Python files via AST for unparameterized SQL, insecure sudo(), compute loops, and missing super(); validates CSV security access rights (ir.model.access.csv); checks XML views for unescaped entities, deprecated tags, and bad XPaths; validates Excel/CSV data files."
---

# Odoo File-Level Deep Inspector (Principal Standard)

This skill provides static, syntactic, and semantic inspection of individual source and data files in Odoo modules to eliminate vulnerabilities and regressions before compilation.

---

## 1. Python Source File Auditing (`*.py`)

### A. SQL Injection Prevention
- **Rule**: Never use string concatenation (`+`), `%` formatting, `.format()`, or f-strings inside `self.env.cr.execute(...)`.
- **Approved Patterns**:
  ```python
  # Pattern 1: Parameterized tuple
  self.env.cr.execute("SELECT id FROM res_partner WHERE name = %s", (name,))

  # Pattern 2: odoo.tools.SQL (Odoo 17, 18, 19, 20)
  from odoo.tools import SQL
  query = SQL("SELECT id FROM res_partner WHERE name = %s", name)
  self.env.cr.execute(query)
  ```

### B. Insecure `sudo()` Usage & Escalation Prevention
- **Rule**: Calling `.sudo()` bypasses all multi-company and record-level security rules.
- **Enforcement**:
  1. A code comment explaining why elevated privileges are required MUST precede every `.sudo()`.
  2. Never chain `.sudo()` directly into write operations with user-controlled input without explicit field whitelisting.
  3. When accessing system records in user context, use `.with_user(...)` or `.with_context(...)` rather than blank `.sudo()`.

### C. Compute Loop & Cache Invalidation Hazards
- **Rule**: A computed method decorated with `@api.depends('field_a')` must NEVER modify `self.field_a` inside the method body. This triggers an infinite recursive recompute loop and server crash.
- **Rule**: All fields accessed inside `@api.depends` must be explicitly listed in the decorator.

### D. Standard ORM Overrides
- When overriding `create(vals_list)`:
  - Must accept `vals_list` (batch create).
  - Must call `super().create(vals_list)`.
- When overriding `write(vals)`:
  - Must return boolean from `super().write(vals)`.
- When overriding `unlink()`:
  - Must perform pre-checks before calling `super().unlink()`.

### E. Mutable Default Arguments
- Never use mutable defaults in function signatures: `def action_process(self, records=[])`. Use `records=None` and initialize inside the function.

---

## 2. Security Access File Auditing (`ir.model.access.csv`)

### A. Header Integrity
The first line MUST be exactly:
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
```

### B. Logical Permission Auditing
- A row with `perm_write=1`, `perm_create=1`, or `perm_unlink=1` MUST have `perm_read=1`. A user cannot write or delete a record they cannot read.
- `model_id:id` must reference `model_<model_name_with_underscores>` (e.g. `model_crm_lead` for `crm.lead`).

### C. Trailing Newline & Duplicate IDs
- File must end with a trailing newline.
- The `id` column must be unique across all rows and follow OCA naming convention: `access_<model_name>_<group_name>`.

---

## 3. XML View & Data File Auditing (`*.xml`)

### A. Modern Syntax Integrity (Odoo 19 & 20)
- Views must use `<list>` (never `<tree>`).
- Direct expressions only: `invisible="state != 'draft'"`. Never `attrs=` or `states=`.
- Chatter must use `<chatter/>` directly inside `<form>` (after `</sheet>`).
- Selections like `priority` must use string literals `'0'`, `'1'`, `'2'`, `'3'`.

### B. Unescaped XML Entities
- Every `&` must be written as `&amp;`.
- Every `<` in python domain expressions must be written as `&lt;` or wrapped in `<![CDATA[ ... ]]>`.

### C. Master Data Safety
- Records creating sequences, default settings, or initial master data MUST include `noupdate="1"` on `<odoo noupdate="1">` or `<data noupdate="1">` to avoid overwriting user edits on module upgrade.

---

## 4. Using the File Auditor Tool

Audit any single file directly:
```bash
odoo-dev file-audit /path/to/models/my_model.py
odoo-dev file-audit /path/to/security/ir.model.access.csv
odoo-dev file-audit /path/to/views/my_views.xml
```
