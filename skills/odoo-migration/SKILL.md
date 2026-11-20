---
name: odoo-migration
description: >-
  Migrate Odoo addons across major versions (Odoo 16, 17, 18, 19, and 20).
  Identifies deprecated syntax, converts legacy XML attributes (tree to list,
  attrs to invisible/readonly), rewrites deprecated Python methods (name_get to
  _compute_display_name), updates OWL components, and resolves schema and API
  breaking changes. Use when upgrading, porting, or auditing code across Odoo
  versions.
---

# Odoo Version Migration & Compatibility Guide

This skill guides migration of Odoo modules between versions (v16.0 -> v17.0 -> v18.0 -> v19.0 -> v20.0).

## Version Compatibility Matrix & Major Breaking Changes

### 1. View Syntax Changes

| Feature / Element | Odoo 16.0 | Odoo 17.0 | Odoo 18.0 / 19.0 / 20.0 | Migration Action |
| --- | --- | --- | --- | --- |
| **List Views** | `<tree>` | `<tree>` (deprecated) | `<list>` (mandatory) | Change `<tree>` to `<list>`, and closing `</tree>` to `</list>` |
| **Attributes (`attrs`)** | `attrs="{'invisible': [('state', '!=', 'draft')]}"` | Deprecated, direct Python expr supported | Removed | Replace `attrs="{'invisible': [('x', '=', y)]}"` with `invisible="x == y"` |
| **`states` attribute** | `states="draft,sent"` | Removed | Removed | Use `invisible="state not in ('draft', 'sent')"` or `readonly="state in ('done', 'cancel')"` |
| **Chatter tag** | `<div class="oe_chatter">...</div>` | `<chatter/>` supported | `<chatter/>` standard | Use clean `<chatter/>` inside `<form>` |
| **Action view mode** | `<field name="view_mode">tree,form</field>` | `tree,form` | `list,form` | Replace `tree` with `list` in `view_mode` |

#### Automated Python Regex for XML Migration
```python
# Convert <tree> to <list>
xml_content = re.sub(r'<tree(\b[^>]*)>', r'<list\1>', xml_content)
xml_content = xml_content.replace('</tree>', '</list>')

# Convert view_mode
xml_content = re.sub(r'(<field\s+name=["\']view_mode["\'][^>]*>.*?)tree(.*?</field>)', r'\1list\2', xml_content)
```

---

### 2. Python ORM & Method Changes

#### A. `name_get()` → `_compute_display_name()`
In Odoo 17+, `name_get()` is completely removed. Use `_compute_display_name()`:

**Legacy (Odoo 16 and older):**
```python
def name_get(self):
    result = []
    for record in self:
        name = f"[{record.code}] {record.name}" if record.code else record.name
        result.append((record.id, name))
    return result
```

**Modern (Odoo 17, 18, 19, 20):**
```python
@api.depends('name', 'code')
def _compute_display_name(self):
    for record in self:
        record.display_name = f"[{record.code}] {record.name}" if record.code else record.name
```

#### B. Search & Filter on Computed Fields
- Implement `_search_<fieldname>(self, operator, value)` supporting `('=', '!=', 'in', 'not in')`.
- Return valid domain tuples. Never raise `NotImplementedError` for `=` or `!=`.

#### C. `_read_group` Modern Signature
In Odoo 17+, `_read_group` returns a list of tuples or dictionaries according to the `groupby` and `aggregates` parameters:
```python
# Modern usage:
result = self.env['sale.order']._read_group(
    domain=[('state', '=', 'sale')],
    groupby=['partner_id'],
    aggregates=['amount_total:sum', 'id:count'],
)
for partner, amount_sum, count in result:
    pass
```

---

### 3. Frontend & OWL Framework Migration

#### A. OWL 1 (v14/v15) vs OWL 2 (v16+)
- OWL 2 classes inherit from `Component` from `@odoo/owl`.
- Hooks must be called in `setup()`: `useState`, `useService`, `useRef`, `onWillStart`, `onMounted`.
- Template inheritance: `t-inherit` and `t-inherit-mode="extension"`.
- Never access non-existent globals or services. Use `this.orm = useService("orm")` and `this.action = useService("action")`.

#### B. Services Replacement
| Legacy | Modern OWL 2 Service |
| --- | --- |
| `this.rpc(...)` | `this.orm = useService("orm"); await this.orm.call(...)` |
| `this.do_action(...)` | `this.action = useService("action"); this.action.doAction(...)` |
| `this.displayNotification(...)` | `this.notification = useService("notification"); this.notification.add(...)` |

---

### 4. Migration Audit Checklist

1. **Manifest**: Check `version` matches target series (e.g. `18.0.1.0.0`), check all dependencies exist.
2. **Views**:
   - Grep for `<tree` and replace with `<list>`
   - Grep for `attrs=` and convert to direct Python boolean expressions
   - Grep for `states=` and convert to `readonly=` / `invisible=`
   - Check `<field name="view_mode">` contains `list,form` rather than `tree,form`
3. **Models**:
   - Check for `def name_get` and convert to `_compute_display_name`
   - Check for `fields.Date.today()` vs `fields.Date.context_today(self)`
   - Check for `search_count()` instead of `len(search())`
4. **Security**:
   - Verify `ir.model.access.csv` includes all models defined in the addon.
   - Guard `sudo()` operations with whitelist filtering.
