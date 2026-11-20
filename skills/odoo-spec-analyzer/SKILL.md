---
name: odoo-spec-analyzer
description: >-
  Analyze, extract, and translate client business documents, wireframes, Excel spreadsheets,
  PDF specifications, and Word BRDs into structured Odoo technical architecture and clean code.
  Use when given customer requirements documents, BOM sheets, invoice samples, mockup screenshots,
  or data import templates to design models, fields, and workflows.
---

# Odoo Specification & Document Analysis Guide

Transform unstructured client requirements, wireframe screenshots, PDF specifications, Excel templates, and Word BRDs into production-quality Odoo models, views, and workflows.

---

## 1. Document Reading & Extraction Process

When the user provides a document or path:
1. **Identify the File Type & Run Reader**:
   - **Excel (`.xlsx`, `.xls`)**: Run `odoo-dev read <path>` to extract sheets, column headers, data types, and sample records.
   - **PDF (`.pdf`)**: Run `odoo-dev read <path>` to extract page text, document structure, and tables.
   - **Word (`.docx`)**: Run `odoo-dev read <path>` to extract headings, requirements, and specifications.
   - **Images / Mockups (`.png`, `.jpg`, `.jpeg`, `.webp`)**: Use Antigravity's `view_file` to visually examine UI layouts, field positioning, buttons, and state transitions.

2. **Synthesize the Business Model**:
   - What is the primary entity? (e.g. `service.ticket`, `custom.bom`, `inspection.request`)
   - What are the line items / child records? (One2many relations)
   - What master data models are linked? (Many2one relations to `res.partner`, `res.users`, `product.product`, `account.tax`)

---

## 2. Document-to-Odoo Mapping Rules

### A. Mapping Excel Columns to Odoo Fields
| Excel Column Sample | Detected Type | Odoo Field Definition | UI Widget / Attributes |
| :--- | :--- | :--- | :--- |
| "Invoice Number", "Reference", "Code" | Text / Alphanumeric | `fields.Char(string='Reference', required=True, copy=False, index=True)` | `placeholder="e.g. INV/2026/001"` |
| "Total Amount", "Unit Price", "Cost" | Decimal currency | `fields.Monetary(string='Unit Price', currency_field='currency_id')` | `widget="monetary"` |
| "Quantity", "Hours", "Weight" | Float | `fields.Float(string='Quantity', digits='Product Unit of Measure')` | `digits=(16, 2)` |
| "Date", "Effective Date" | Date | `fields.Date(string='Date', default=fields.Date.context_today)` | `widget="date"` |
| "Status", "Stage", "Type" | Closed list of values | `fields.Selection(selection=[('draft', 'Draft'), ...], default='draft')` | `widget="statusbar"` or `widget="badge"` |
| "Customer", "Vendor", "Employee" | Master record lookup | `fields.Many2one('res.partner', string='Customer', check_company=True)` | `options="{'no_create': True}"` |
| "Detailed Notes", "Terms", "Description" | Multiline text / HTML | `fields.Html(string='Terms and Conditions')` or `fields.Text(...)` | - |

---

## 3. UI Mockup / Wireframe Image Analysis

When analyzing UI screenshots or wireframes with `view_file`:
1. **Header**:
   - Identify action buttons (e.g. *Confirm*, *Approve*, *Print*, *Cancel*).
   - Identify statusbar stages (`statusbar_visible`).
2. **Sheet Title**:
   - Does it have a sequence or document title? (`<div class="oe_title"><h1>...</h1></div>`).
3. **Left/Right Column Groups**:
   - Two-column layout `<group><group>...</group><group>...</group></group>`.
4. **Notebook Pages**:
   - Tabs for lines, order details, delivery info, or custom notes (`<notebook><page string="..." name="...">`).
5. **Chatter**:
   - Note if followers, activities, or message log are present at the bottom $\rightarrow$ add `<chatter/>`.

---

## 4. Deliverable Structure for the User

After analyzing a customer document or image, always present:
1. **Executive Functional Summary**: What business flow this document represents.
2. **Data Model Architecture**: Models, fields, relations, constraints.
3. **View Layout Plan**: Form view structure, list columns, search filters, menus.
4. **Implementation Plan & Code**: Immediate clean implementation matching the client's specification.
