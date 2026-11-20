---
name: odoo-data-migration
description: >-
  Enterprise data migration, schema evolution, and upgrade scripting for Odoo.
  Covers writing pre-migration and post-migration scripts (OpenUpgrade standards),
  safe column renames, XML ID remapping, data transformation, and schema migrations
  without data loss or downtime. Use when upgrading databases across major versions
  or refactoring existing data models in production.
---

# Odoo Enterprise Data Migration & Upgrade Scripting

Master guide for writing rock-solid, zero-data-loss database migration scripts across Odoo releases.

---

## 1. Migration Directory Architecture

Standard OpenUpgrade / Odoo migration layout inside your addon:

```text
my_addon/
└── migrations/
    └── 19.0.1.0.0/
        ├── pre-migrate.py    # Runs BEFORE module models and views load
        └── post-migrate.py   # Runs AFTER new schema and XML data have loaded
```

---

## 2. Pre-Migration Scripting (`pre-migrate.py`)

Used to rename columns, preserve data before a model definition changes, or drop obsolete constraints:

```python
from odoo.tools.sql import rename_column, table_exists, column_exists

def migrate(cr, version):
    if not version:
        return

    # 1. Safe Column Rename (prevents Odoo from dropping old column and losing data)
    if column_exists(cr, 'sale_order', 'legacy_code') and not column_exists(cr, 'sale_order', 'reference_code'):
        rename_column(cr, 'sale_order', 'legacy_code', 'reference_code')

    # 2. Preserve Data into Temporary Table if model structure changes
    if table_exists(cr, 'old_table_name'):
        cr.execute("""
            CREATE TABLE IF NOT EXISTS temp_data_backup AS 
            SELECT id, name, value FROM old_table_name;
        """)
```

---

## 3. Post-Migration Scripting (`post-migrate.py`)

Used to transform data, populate newly added required fields, remap XML IDs, or set defaults:

```python
from odoo import api, SUPERUSER_ID

def migrate(cr, version):
    if not version:
        return

    env = api.Environment(cr, SUPERUSER_ID, {})

    # 1. Populate New Required Field with Sensible Defaults
    cr.execute("""
        UPDATE custom_record 
        SET priority = '1' 
        WHERE priority IS NULL;
    """)

    # 2. Remap XML External IDs (ir.model.data) if a view or action was renamed
    cr.execute("""
        UPDATE ir_model_data 
        SET name = 'view_custom_record_list' 
        WHERE module = 'my_addon' AND name = 'view_custom_record_tree';
    """)

    # 3. Clean Obsolete Views to Prevent Upgrade Crashes
    cr.execute("""
        DELETE FROM ir_ui_view 
        WHERE id IN (
            SELECT res_id FROM ir_model_data 
            WHERE module = 'my_addon' AND name = 'view_obsolete_form'
        );
    """)
```

---

## 4. Verification & Rollback Protection

1. Always test migrations on a sanitized database dump before running on production.
2. Check PostgreSQL error logs for broken constraints or orphan records.
3. Verify record counts before and after migration:
   ```sql
   SELECT count(*) FROM target_table;
   ```
