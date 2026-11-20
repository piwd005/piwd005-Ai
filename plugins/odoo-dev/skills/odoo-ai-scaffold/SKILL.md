---
name: odoo-ai-scaffold
description: >-
  Scaffold production-quality Odoo addon modules, models, views, security,
  and workflows. Supports Odoo 16, 17, 18, 19, and 20 with zero guesswork,
  complete directory structures, proper inheritance, clean manifests, and
  automated test fixtures. Use when creating new Odoo modules or adding full
  model/view architectures.
---

# Odoo AI Module & Architecture Scaffolding

Scaffold production-grade Odoo modules with correct architecture, modern field types, defensive views, robust security, and unit tests.

## Standard Module Directory Layout

Every clean Odoo addon must follow this directory structure:

```text
my_addon/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── my_model.py
├── views/
│   ├── my_model_views.xml
│   └── menu_views.xml
├── security/
│   ├── security.xml (optional: groups & rules)
│   └── ir.model.access.csv
├── data/
│   └── sequence_data.xml (optional: noupdate records)
├── demo/
│   └── demo_data.xml (optional: test records)
├── static/
│   ├── description/
│   │   ├── icon.png
│   │   └── index.html
│   └── src/
│       ├── js/
│       ├── xml/
│       └── scss/
└── tests/
    ├── __init__.py
    └── test_my_model.py
```

## 1. `__manifest__.py` Best Practices

Always provide complete manifests with version prefixing matching the target Odoo release:

```python
{
    'name': 'Module Display Name',
    'version': '18.0.1.0.0',  # Format: {odoo_version}.{major}.{minor}.{patch}
    'category': 'Sales/Sales',
    'summary': 'Concise one-line summary of module capability',
    'description': """
Detailed description of functionality, features, and workflows.
    """,
    'author': 'Your Name / Company',
    'website': 'https://www.example.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',  # Include when using chatter (mail.thread, mail.activity.mixin)
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/my_model_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
```

## 2. Models (`models/my_model.py`)

- Inherit from `models.Model`.
- Include `mail.thread` and `mail.activity.mixin` when user collaboration or chatter is required.
- Lay out class in the standard order:
  1. `_name`, `_description`, `_inherit`, `_order`, `_rec_name`
  2. Default methods (`_default_*`)
  3. Field declarations (standard fields, relational fields, computed fields)
  4. SQL Constraints (`_sql_constraints`)
  5. Python Constraints (`@api.constrains`)
  6. Computes and onchanges (`@api.depends`, `@api.onchange`)
  7. CRUD overrides (`create`, `write`, `unlink`)
  8. Action / Button methods (prefix with `action_`)
  9. Business / Private helper methods (prefix with `_`)

```python
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class MyModel(models.Model):
    _name = 'my.model'
    _description = 'My Model Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Name', required=True, tracking=True)
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        required=True,
        tracking=True,
    )
    partner_id = fields.Many2one('res.partner', string='Partner', tracking=True)
    amount = fields.Monetary(string='Amount', currency_field='currency_id')
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )
    notes = fields.Html(string='Notes')

    # Actions
    def action_confirm(self):
        for record in self:
            if record.state != 'draft':
                raise ValidationError(_("Only draft records can be confirmed."))
            record.state = 'confirmed'
        return True
```

## 3. Views (`views/my_model_views.xml`)

Targeting Odoo 17+:
- Form views: include `<header>`, `<sheet>`, and optional chatter `<chatter/>` (or `<div class="oe_chatter">`).
- List views: use `<list>` tag in Odoo 18, 19, and 20 (`<tree>` in Odoo 16 and 17).
- Attributes: Use direct Python expressions: `invisible="state != 'draft'"` instead of `attrs="{'invisible': ...}"`.
- Button actions: Always check methods exist on the model.

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- List / Tree View -->
    <record id="view_my_model_list" model="ir.ui.view">
        <field name="name">my.model.list</field>
        <field name="model">my.model</field>
        <field name="arch" type="xml">
            <list string="My Records" decoration-info="state == 'draft'" decoration-success="state == 'done'">
                <field name="name"/>
                <field name="partner_id"/>
                <field name="amount"/>
                <field name="state" widget="badge" decoration-info="state == 'draft'" decoration-success="state == 'done'"/>
            </list>
        </field>
    </record>

    <!-- Form View -->
    <record id="view_my_model_form" model="ir.ui.view">
        <field name="name">my.model.form</field>
        <field name="model">my.model</field>
        <field name="arch" type="xml">
            <form string="My Record">
                <header>
                    <button name="action_confirm" string="Confirm" type="object" class="btn-primary" invisible="state != 'draft'"/>
                    <field name="state" widget="statusbar" statusbar_visible="draft,confirmed,done"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1>
                            <field name="name" placeholder="Title..."/>
                        </h1>
                    </div>
                    <group>
                        <group>
                            <field name="partner_id"/>
                        </group>
                        <group>
                            <field name="currency_id" invisible="1"/>
                            <field name="amount"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Notes" name="notes">
                            <field name="notes"/>
                        </page>
                    </notebook>
                </sheet>
                <chatter/>
            </form>
        </field>
    </record>

    <!-- Search View -->
    <record id="view_my_model_search" model="ir.ui.view">
        <field name="name">my.model.search</field>
        <field name="model">my.model</field>
        <field name="arch" type="xml">
            <search string="Search Records">
                <field name="name"/>
                <field name="partner_id"/>
                <filter string="Draft" name="draft" domain="[('state', '=', 'draft')]"/>
                <filter string="Confirmed" name="confirmed" domain="[('state', '=', 'confirmed')]"/>
                <group expand="0" string="Group By">
                    <filter string="Partner" name="group_by_partner" context="{'group_by': 'partner_id'}"/>
                    <filter string="Status" name="group_by_state" context="{'group_by': 'state'}"/>
                </group>
            </search>
        </field>
    </record>

    <!-- Window Action -->
    <record id="action_my_model" model="ir.actions.act_window">
        <field name="name">My Records</field>
        <field name="res_model">my.model</field>
        <field name="view_mode">list,form</field>
        <field name="search_view_id" ref="view_my_model_search"/>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Create your first record!
            </p>
        </field>
    </record>
</odoo>
```

## 4. Security (`security/ir.model.access.csv`)

Always declare access permissions for models. Standard header and format:

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_my_model_user,my.model.user,model_my_model,base.group_user,1,1,1,0
access_my_model_manager,my.model.manager,model_my_model,base.group_system,1,1,1,1
```

## 5. Automated Tests (`tests/test_my_model.py`)

Always provide unit tests inheriting from `TransactionCase`:

```python
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestMyModel(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({'name': 'Test Customer'})
        cls.record = cls.env['my.model'].create({
            'name': 'Sample Record',
            'partner_id': cls.partner.id,
            'amount': 150.0,
        })

    def test_initial_state(self):
        """Test record created in draft state."""
        self.assertEqual(self.record.state, 'draft')

    def test_action_confirm(self):
        """Test confirming a record transitions state to confirmed."""
        self.record.action_confirm()
        self.assertEqual(self.record.state, 'confirmed')

    def test_action_confirm_invalid(self):
        """Test that confirming non-draft record raises ValidationError."""
        self.record.state = 'done'
        with self.assertRaises(ValidationError):
            self.record.action_confirm()
```
