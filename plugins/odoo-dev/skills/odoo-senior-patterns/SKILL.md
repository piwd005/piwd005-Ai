---
name: odoo-senior-patterns
description: >-
  The Senior Odoo Engineer Handbook and Field-Tested Standards for Odoo 19 & 20.
  Covers the 10 unbreakable laws of senior Odoo development: Zero-Tolerance for Guessed XPaths,
  Defensive Relational Navigation, The "Every Button Must Work" Interactive Law, Safe System
  Parameters, Complete Interactive Business Lifecycle, Selection Field Type Integrity,
  Computed Field Search Methods, Professional QWeb Report Architecture, and Single-Turn
  Excellence. Use on any Odoo task to ensure production-grade perfection.
---

# Senior Odoo Engineering Patterns & Field-Tested Standards

Field-tested rules that distinguish a senior Odoo engineer from an amateur. Apply these rules across all Odoo 19 and Odoo 20 modules.

---

## 1. The "Every Button Must Work" Law (Interactive Traceability)

Never deliver UI elements (buttons, 3-dots actions, statusbars, wizard openers, tabs) that are empty shells or placeholder stubs.
- For **EVERY** button in XML:
  1. If `type="object"`, confirm the method exists on the model:
     ```python
     def action_confirm(self):
         self.ensure_one()
         self.write({'state': 'confirmed'})
         return True
     ```
  2. If `type="action"`, confirm the window action, report, or server action XML ID exists and is accessible.
  3. If a 3-dots dropdown has options (e.g. *Print PDF*, *Send Email*, *Archive*, *Lock*), **every single one must have a working handler**.
  4. Statusbar buttons must transition state with validation checks:
     ```python
     def action_cancel(self):
         for record in self:
             if record.state == 'done':
                 raise UserError(_("Completed records cannot be cancelled."))
             record.state = 'cancelled'
     ```

---

## 2. Zero-Tolerance for Guessed XPaths

A failed XPath causes a fatal `ParseError` on module upgrade, breaking the entire database.
- **Never guess parent view structures or classes.**
- Physically inspect the parent view in the inherited module's XML before writing the XPath.
- Always anchor on **unique `name` attributes**:
  - `//field[@name='partner_id']`
  - `//page[@name='internal_notes']`
  - `//button[@name='action_confirm']`
- Never anchor on transient classes: `[hasclass('oe_title')]` or `[hasclass('btn-secondary')]`.

---

## 3. Defensive Relational Field Navigation

Never assume related records exist. Business documents frequently have empty partner, salesperson, or company assignments.
```python
# ❌ DANGEROUS:
email = record.partner_id.email
tax_id = record.company_id.vat

# ✅ SENIOR STANDARD:
email = record.partner_id.email if record.partner_id else False
tax_id = record.company_id.vat if record.company_id else False
# Or helper function:
def _safe_get(rec, field):
    return getattr(rec, field, False) if rec else False
```

---

## 4. Selection Field Type Integrity (Priority & Domains)

- Odoo `priority` fields are strings/varchar (`'0'`, `'1'`, `'2'`, `'3'`), NOT integers.
- Domain search filters **must** compare against string literals:
  - `[('priority', '=', '3')]` (Correct)
  - `[('priority', '=', 3)]` (Broken — evaluates to False or fails query)
- In `create()` and `write()`, normalize incoming priority:
  ```python
  if 'priority' in vals and vals['priority'] is not None:
      vals['priority'] = str(vals['priority'])
  ```

---

## 5. Computed Field Search Methods (`_search_*`)

When defining `search='_search_<fieldname>'`:
- **Never** restrict to `operator == 'in'` and return `NotImplementedError` for `=` or `!=`.
- The web client search bar evaluates filters with `('field', '=', True)`.
- Always implement support for `('=', '!=', 'in', 'not in')` and return valid domains for both positive and negative evaluations:
```python
def _search_is_late(self, operator, value):
    today = fields.Date.context_today(self)
    positive = (operator == '=' and value) or (operator == '!=' and not value)
    if positive:
        return [('expected_date', '<', today), ('state', 'not in', ('done', 'cancel'))]
    else:
        return ['|', ('expected_date', '>=', today), ('state', 'in', ('done', 'cancel'))]
```

---

## 6. Safe System Parameters (`ir.config_parameter`)

- **Never** insert raw `<record model="ir.config_parameter">` into data XML files. This causes fatal `UniqueViolation` database crashes on module upgrade.
- Implement settings via `res.config.settings` with `config_parameter='...'`:
  ```python
  api_key = fields.Char(string="API Key", config_parameter="my_module.api_key")
  ```
- Always query with a safe fallback default:
  ```python
  key = self.env['ir.config_parameter'].sudo().get_param('my_module.api_key', default='')
  ```

---

## 7. Professional QWeb Report Architecture

When creating or modifying PDF reports using `web.external_layout`:
1. **Always populate `<t t-set="address">`**: Places customer contact and tax information into Odoo's designated top-right header box.
2. **Never place raw columns directly at the top of `<div class="page">`** without `<t t-set="address">` — `wkhtmltopdf` will overlap headers and body content.
3. Structure body into Bootstrap cards, clear status badges, and an aligned signature block.

---

## 8. Eliminate Duplicate Fields & Conflicting Logic

Before adding new fields to an existing or inherited model:
- Inspect existing fields across base and standard addons.
- Never introduce duplicate or synonymous fields:
  - `is_favorite` vs `is_user_favorite`
  - `website_published` vs `is_published`
  - `trash_date` vs `deletion_date`
- Unify under standard Odoo naming conventions.

---

## 9. Single-Turn Comprehensive Execution

When implementing a feature or parity requirement:
1. Conduct an inventory diff across all 6 dimensions:
   - **Models**: declarations and inheritance
   - **Fields**: types, relations, computes
   - **Views**: form, list, search, kanban, pivot, graph
   - **Menus & Actions**: hierarchy, window actions, default contexts
   - **Security**: `ir.model.access.csv`, multi-company rules
   - **Assets**: JS, SCSS, OWL templates
2. Implement **all** missing parts in that same single turn.
3. Verify every layer before concluding:
   - Syntax and AST check
   - Pylint-odoo run
   - XML well-formedness and XPath checks
   - Upgrade test (`odoo-bin -u <module> --stop-after-init`)
