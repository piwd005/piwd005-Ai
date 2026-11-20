---
name: odoo-enterprise-parity
description: >-
  Exhaustive 6-dimension parity auditing and implementation methodology for Odoo modules.
  Compares Community vs Enterprise, or Custom vs Standard across Models, Fields, Views,
  Menus/Actions, Security, and Assets. Eliminates duplicate fields, verifies interactive button
  handlers, and delivers 100% complete feature parity in a single turn without placeholders.
  Use when porting, upgrading, or auditing modules for enterprise equivalence.
---

# Odoo Enterprise Parity & 6-Dimension Audit Masterclass

Achieve 100% operational and architectural parity between custom/community modules and Odoo Enterprise baselines.

---

## 1. The 6-Dimension Parity Audit Matrix

Before declaring any module "parity-complete", conduct an exhaustive diff across all 6 dimensions:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        THE 6-DIMENSION PARITY DIFF                     │
├─────────────────────┬──────────────────────────────────────────────────┤
│ 1. MODELS           │ Compare all `_name`, `_inherit`, and `_inherits`.│
│ 2. FIELDS           │ Compare field lists, types, relations & computes.│
│                     │ Eliminate duplicate/synonymous fields.           │
│ 3. VIEWS            │ Form, List (<list>), Search, Kanban, Pivot, Graph│
│ 4. MENUS & ACTIONS  │ Action definitions, context defaults, hierarchies│
│ 5. SECURITY & RULES │ ir.model.access.csv, groups, multi-company rules │
│ 6. FRONTEND ASSETS  │ OWL 2.0 components, JS controllers, SCSS styling │
└─────────────────────┴──────────────────────────────────────────────────┘
```

---

## 2. Eliminating Duplicate & Synonymous Fields

Amateurs add duplicate fields that clash with standard Odoo fields. Principal engineers unify:

| ❌ Clashing Duplicate Field | ✅ Standard Odoo Field | Rationale |
| :--- | :--- | :--- |
| `is_favorite` | `is_user_favorite` | Uses Odoo's native user-specific favorite widget |
| `website_published` | `is_published` | Standard Odoo publication mixin (`website.published.mixin`) |
| `trash_date` | `deletion_date` | Consistent with Odoo trash lifecycle |
| `active_archive` | `active` | Core Odoo archivable boolean |
| `status` | `state` | Core Odoo workflow selection state |

---

## 3. The "Every Button Must Work" Interactive Gate

Never deliver UI elements that are empty shells. For EVERY interactive element:
1. **Header Action Buttons**:
   - `action_confirm()` $\rightarrow$ Transitions state to `confirmed`, validates constraints.
   - `action_done()` $\rightarrow$ Transitions state to `done`.
   - `action_cancel()` $\rightarrow$ Validates that completed records cannot be cancelled.
2. **3-Dots Action Dropdown Menu**:
   - Export, Print PDF, Share, Lock, Archive, Duplicate $\rightarrow$ Every item must have a working backend or OWL action.
3. **Smart Buttons (Stat Boxes)**:
   - Compute badge count efficiently with `search_count()`.
   - Clicking smart button opens a window action filtering records by relational ID.

---

## 4. Single-Turn Parity Verification Checklist

- [ ] **Python Compilation Check**: All models, wizards, and helpers compile with zero syntax errors.
- [ ] **XML Syntax Parse Check**: All view, action, menu, and data files parse cleanly with `lxml`.
- [ ] **Zero Duplicate Fields**: No duplicate field warnings in the Odoo registry.
- [ ] **Explicit Action View Mapping**: Window actions explicitly bind `<field name="view_id" ref="..."/>`.
- [ ] **Asset Bundle Integrity**: All JS/SCSS imports declared in `__manifest__.py` exist and load without bundle errors.
- [ ] **Interactive Traceability**: Every button, modal, and report has an operational handler.
