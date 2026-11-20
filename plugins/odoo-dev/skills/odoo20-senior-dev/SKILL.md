---
name: odoo20-senior-dev
description: >-
  Advanced engineering guide and standard for Odoo 20 development.
  Covers Odoo 20 framework architecture, Python 3.12+ integration, high-performance ORM,
  Hoot frontend testing (@odoo/hoot), multi-company isolation, safe dynamic metadata creation,
  interactive business lifecycles, and enterprise-grade code quality.
  Use when developing, architecting, or verifying modules for Odoo 20.
---

# Odoo 20 Senior Developer Master Guide

This skill provides senior-level engineering standards, bleeding-edge ORM patterns, frontend Hoot testing conventions, and architectural best practices for **Odoo 20**.

---

## 1. Odoo 20 Core Framework & Python 3.12+ Standards

### A. Python 3.12+ Typing and Concurrency
- Python 3.12 is the primary runtime for Odoo 20.
- Leverage type annotations on public methods and helper functions.
- Avoid deprecated datetime calls (never use `datetime.datetime.utcnow()`; use `datetime.datetime.now(datetime.timezone.utc)` or `fields.Datetime.now()`).
- Always use `fields.Date.context_today(self)` instead of raw `date.today()` to respect the user's active timezone.

### B. Odoo 20 Manifest Specifications
```python
{
    'name': 'Enterprise Feature Extension',
    'version': '20.0.1.0.0',
    'category': 'Operations',
    'summary': 'Next-gen enterprise workflow integration for Odoo 20',
    'author': 'Senior Dev Team',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'web',
        'mail',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/my_model_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'my_addon/static/src/scss/**/*',
            'my_addon/static/src/components/**/*',
        ],
        'web.assets_unit_tests': [
            'my_addon/static/tests/**/*',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
```

---

## 2. Advanced ORM & High-Performance Data Processing

### A. Aggregations with `_read_group`
Never query all records into memory just to calculate sums or counts. Always use `_read_group`:
```python
# Odoo 20 Senior Standard:
order_data = self.env['sale.order']._read_group(
    domain=[('state', '=', 'sale'), ('company_id', '=', self.env.company.id)],
    groupby=['partner_id', 'date_order:month'],
    aggregates=['amount_total:sum', 'id:count'],
)
for partner, month, total_amount, order_count in order_data:
    # Process aggregated buckets efficiently with O(1) database work
    pass
```

### B. Safe Dynamic View & Metadata Generation (`ir.model.data`)
When creating views or templates dynamically in Python (`ir.ui.view`):
- Never blindly call `self.env['ir.model.data'].create(...)` — this causes unique constraint crashes on re-execution!
- Always check if the `ir.model.data` entry already exists (`module`, `name`) and update its `res_id`:
```python
def _register_external_id(self, xml_id, model, res_id):
    module, name = xml_id.split('.', 1)
    imd = self.env['ir.model.data'].search([('module', '=', module), ('name', '=', name)], limit=1)
    if imd:
        imd.write({'res_id': res_id, 'model': model})
    else:
        self.env['ir.model.data'].create({
            'module': module,
            'name': name,
            'model': model,
            'res_id': res_id,
            'noupdate': True,
        })
```

### C. Safe System Parameters (`ir.config_parameter`)
- Never insert raw `<record model="ir.config_parameter">` into data XML files; this causes fatal `UniqueViolation` database crashes on module upgrade.
- Implement settings via `res.config.settings` with `config_parameter='...'`:
  ```python
  class ResConfigSettings(models.TransientModel):
      _inherit = 'res.config.settings'

      auto_sync_enabled = fields.Boolean(
          string='Enable Auto Sync',
          config_parameter='my_addon.auto_sync_enabled',
          default=True,
      )
  ```
- Query parameters safely with fallback defaults:
  ```python
  ICP = self.env['ir.config_parameter'].sudo()
  is_enabled = ICP.get_param('my_addon.auto_sync_enabled', 'True') != 'False'
  ```

---

## 3. Complete Interactive Lifecycle for Business Models

When introducing a configurable child model or checklist (e.g. worksheet lines, inspection points, milestone checklists from templates):
1. **Dynamic Onchange**: Implement `@api.onchange('template_id')` for immediate UI responsiveness.
2. **Explicit Manual Sync Button**: Provide a button (e.g. `action_load_template_items`) so users can re-sync without re-creating the entire document.
3. **Auto-Initialization**: Initialize missing lines automatically in `create()` if a template is assigned.
4. **Editable Views**: Do not lock child lists (`create="0" delete="0" readonly="1"`) unless explicitly required by business rules.
5. **Default Master Data**: Always package realistic default templates in `noupdate="1"` data XML.

```python
class ProjectInspection(models.Model):
    _name = 'project.inspection'
    _description = 'Project Inspection'
    _inherit = ['mail.thread']

    name = fields.Char(string='Title', required=True)
    template_id = fields.Many2one('project.inspection.template', string='Template')
    line_ids = fields.One2many('project.inspection.line', 'inspection_id', string='Checklist Items')

    @api.onchange('template_id')
    def _onchange_template_id(self):
        if self.template_id:
            self._apply_template_lines()

    def action_reload_template(self):
        """Allow user to manually reload template lines at any time."""
        for record in self:
            if not record.template_id:
                raise UserError(_("Please select a template first."))
            record._apply_template_lines()
        return True

    def _apply_template_lines(self):
        self.ensure_one()
        # Keep existing custom answers if lines already exist, or rebuild
        new_lines = []
        for line in self.template_id.line_ids:
            new_lines.append((0, 0, {
                'name': line.name,
                'question_type': line.question_type,
                'sequence': line.sequence,
            }))
        self.line_ids = [(5, 0, 0)] + new_lines
```

---

## 4. Odoo 20 Frontend Testing with Hoot (`@odoo/hoot`)

In Odoo 20, the Hoot test framework is standard for testing OWL components:

```javascript
/** @odoo-module **/

import { describe, expect, test } from "@odoo/hoot";
import { mountWithCleanup, makeMockEnv } from "@web/../tests/web_test_helpers";
import { MyKanbanWidget } from "@my_addon/components/my_kanban_widget";

describe("MyKanbanWidget (Odoo 20)", () => {
    test("component mounts and reacts to user clicks", async () => {
        await makeMockEnv({
            serverData: {
                models: {
                    "my.model": {
                        fields: {
                            id: { type: "integer" },
                            name: { type: "string" },
                            status: { type: "selection" },
                        },
                        records: [
                            { id: 1, name: "Task A", status: "open" },
                            { id: 2, name: "Task B", status: "closed" },
                        ],
                    },
                },
            },
        });

        const fixture = await mountWithCleanup(MyKanbanWidget, {
            props: { modelName: "my.model" },
        });

        expect(fixture.querySelectorAll(".o_kanban_card")).toHaveCount(2);
        expect(fixture.querySelector(".o_kanban_header")).toHaveText("Overview");
    });
});
```

---

## 5. Explicit Action View Mapping

When binding views to window actions (`ir.actions.act_window.view`):
- Always provide `<field name="view_id" ref="..."/>` when a specific custom view is required.
- Omitting `view_id` causes Odoo to resolve default or wrong views.

```xml
<record id="action_view_custom_model_list" model="ir.actions.act_window.view">
    <field name="sequence" eval="1"/>
    <field name="view_mode">list</field>
    <field name="view_id" ref="view_custom_model_list"/>
    <field name="act_window_id" ref="action_custom_model"/>
</record>
<record id="action_view_custom_model_form" model="ir.actions.act_window.view">
    <field name="sequence" eval="2"/>
    <field name="view_mode">form</field>
    <field name="view_id" ref="view_custom_model_form"/>
    <field name="act_window_id" ref="action_custom_model"/>
</record>
```
