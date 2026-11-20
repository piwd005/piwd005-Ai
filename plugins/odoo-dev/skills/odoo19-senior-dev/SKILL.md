---
name: odoo19-senior-dev
description: >-
  Master guide and reference for Odoo 19 senior-level development.
  Covers Odoo 19 ORM paradigms, <list> views, chatter <chatter/>, direct python expressions
  for invisible/readonly, _compute_display_name, OWL frontend standards with useService,
  defensive relational navigation, security auditing, and single-turn zero-defect implementation.
  Use when developing, refactoring, or reviewing modules for Odoo 19.
---

# Odoo 19 Senior Developer Master Guide

This skill encapsulates the architecture, ORM standards, view specifications, and frontend OWL conventions required to develop production-grade addons for **Odoo 19**.

---

## 1. Odoo 19 Architecture & View Standards

### A. View Syntax Requirements
- **List Views**: Strictly `<list>`. The `<tree>` tag is obsolete and must never be used.
  ```xml
  <record id="view_partner_extended_list" model="ir.ui.view">
      <field name="name">res.partner.list.inherit</field>
      <field name="model">res.partner</field>
      <field name="inherit_id" ref="base.view_partner_tree"/>
      <field name="arch" type="xml">
          <xpath expr="//field[@name='email']" position="after">
              <field name="custom_code"/>
          </xpath>
      </field>
  </record>
  ```
- **Window Actions**: `view_mode` must use `list,form` (never `tree,form`).
- **Direct Python Expressions**:
  - `invisible="state != 'draft'"`
  - `readonly="state in ('done', 'cancelled')"`
  - `required="is_mandatory == True"`
  - `attrs="{'invisible': ...}"` and `states="..."` are completely removed.
- **Chatter Integration**: Always use the modern `<chatter/>` tag directly inside `<form>` (after `</sheet>`).
  ```xml
  <form string="My Model">
      <header>...</header>
      <sheet>...</sheet>
      <chatter/>
  </form>
  ```
  Ensure the model inherits `['mail.thread', 'mail.activity.mixin']` and `mail` is in `__manifest__.py`'s `depends`.

### B. Zero-Tolerance for Guessed XPaths
- Never anchor on styling classes (e.g. `hasclass('oe_title')`), buttons without names, or arbitrary positions.
- **Always anchor on unique `name` attributes**:
  - `//field[@name='partner_id']`
  - `//page[@name='internal_notes']`
  - `//header/button[@name='action_confirm']`
- If you need to position relative to a notebook, name the page uniquely.
- Verify parent view existence in the base module before writing the xpath.

---

## 2. Odoo 19 Python ORM Best Practices

### A. Display Name Computation
In Odoo 19, `name_get()` is gone. Always implement `_compute_display_name()`:
```python
@api.depends('name', 'reference')
def _compute_display_name(self):
    for record in self:
        if record.reference:
            record.display_name = f"[{record.reference}] {record.name}"
        else:
            record.display_name = record.name or ''
```

### B. Batch Operations (`create` and `write`)
Odoo 19 expects `create()` to handle a list of dictionaries (`vals_list`):
```python
@api.model_create_multi
def create(self, vals_list):
    for vals in vals_list:
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('my.model.sequence') or _('New')
    return super().create(vals_list)
```

### C. Defensive Relational Field Navigation
Records can be unassigned (`False`/empty recordset). Never chain attributes on relational fields without checking:
```python
# BAD - Crashes with AttributeError if partner_id is False:
phone = record.partner_id.phone

# SENIOR STANDARD - Defensive:
phone = record.partner_id.phone if record.partner_id else False
# Or:
phone = getattr(record.partner_id, 'phone', False)
```

### D. Selection Field Normalization & Priority
- Odoo `priority` fields are strings (`'0'`, `'1'`, `'2'`, `'3'`), NOT integers.
- Domain filters MUST compare against string literals: `[('priority', '=', '3')]`.
- Normalize incoming values in `create()` and `write()`:
  ```python
  if 'priority' in vals and vals['priority'] is not None:
      vals['priority'] = str(vals['priority'])
  ```

### E. Computed Field Search Methods
When declaring a computed field with `search='_search_my_field'`:
- Support all standard operators: `('=', '!=', 'in', 'not in')`.
- Never return `NotImplementedError` for `=` or `!=`.
```python
def _search_is_overdue(self, operator, value):
    today = fields.Date.context_today(self)
    if (operator in ('=', '==') and value) or (operator == '!=' and not value):
        return [('due_date', '<', today), ('state', '!=', 'done')]
    return ['|', ('due_date', '>=', today), ('state', '=', 'done')]
```

---

## 3. Odoo 19 OWL Frontend Standards

### A. Services & Hooks
In Odoo 19 OWL, always import and use standard services via hooks in `setup()`:
```javascript
/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class MyDashboard extends Component {
    static template = "my_addon.Dashboard";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");
        this.dialog = useService("dialog");
        this.user = useService("user");

        this.state = useState({
            loading: true,
            records: [],
        });

        onWillStart(async () => {
            await this.loadData();
        });
    }

    async loadData() {
        this.state.records = await this.orm.searchRead(
            "my.model",
            [["user_id", "=", this.user.userId]],
            ["name", "state", "amount"]
        );
        this.state.loading = false;
    }
}
```

### B. Defensive UI Context Navigation
Never chain props assuming objects exist:
```javascript
// Senior Standard:
const context = this.props.list?.context || this.props.list?.config?.context || {};
```

---

## 4. Odoo 19 QWeb PDF Report Architecture

When implementing or inheriting QWeb reports with `web.external_layout`:
- **Header Box Protection**: Always populate `<t t-set="address">` to place customer contact in Odoo's designated header box.
- Never place raw columns at the top of `<div class="page">` without `<t t-set="address">` — doing so causes `wkhtmltopdf` to overlap header and body content.
- Structure document body into Bootstrap cards, neatly formatted tables with status badges, and an aligned signature block.

```xml
<template id="report_custom_document">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="doc">
            <t t-call="web.external_layout">
                <t t-set="address">
                    <div t-field="doc.partner_id" t-options='{"widget": "contact", "fields": ["address", "name", "phone"], "no_marker": True}'/>
                    <p t-if="doc.partner_id.vat">Tax ID: <span t-field="doc.partner_id.vat"/></p>
                </t>
                <div class="page">
                    <h2 class="mt-3 mb-4">
                        <span t-field="doc.name"/>
                    </h2>
                    <!-- Structured Table -->
                    <table class="table table-sm table-striped">
                        <thead>
                            <tr>
                                <th>Description</th>
                                <th class="text-end">Quantity</th>
                                <th class="text-end">Unit Price</th>
                                <th class="text-end">Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr t-foreach="doc.line_ids" t-as="line">
                                <td><span t-field="line.name"/></td>
                                <td class="text-end"><span t-field="line.quantity"/></td>
                                <td class="text-end"><span t-field="line.price_unit"/></td>
                                <td class="text-end"><span t-field="line.price_total"/></td>
                            </tr>
                        </tbody>
                    </table>
                    <!-- Signature Block -->
                    <div class="row mt-5">
                        <div class="col-6">
                            <p><strong>Prepared By:</strong></p>
                            <p t-field="doc.create_uid.name"/>
                        </div>
                        <div class="col-6 text-end">
                            <p><strong>Authorized Signature:</strong></p>
                            <div class="border-bottom d-inline-block" style="width: 200px; height: 50px;"/>
                        </div>
                    </div>
                </div>
            </t>
        </t>
    </t>
</template>
```

---

## 5. Senior Checklist for Odoo 19 Implementation

- [ ] Every button in XML has a matching python method (`action_*`) or OWL handler.
- [ ] List views use `<list>` tag; window actions use `list,form`.
- [ ] No `attrs=`, no `states=`, no `name_get()`.
- [ ] Relational field accesses are guarded against `False`.
- [ ] `ir.model.access.csv` includes all models with strict CRUD privileges.
- [ ] `__manifest__.py` has correct version (`19.0.1.0.0`), license (`LGPL-3`), and complete `depends`.
- [ ] Module passes `odoo-dev lint` and `odoo-dev validate-manifest`.
