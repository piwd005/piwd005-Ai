---
name: odoo-folder-auditor
description: "Principal-grade Directory, Addon Architecture, and Ghost File Auditor for Odoo. Detects files on disk missing from __manifest__.py ('data' or 'assets'), missing __init__.py cascade imports, circular module dependencies, Git conflict remnants, and structure compliance."
---

# Odoo Folder & Addon Architecture Auditor (Principal Standard)

This skill audits entire Odoo module directories and multi-addon repositories to detect missing manifest registrations, broken import cascades, and architectural flaws.

---

## 1. Core Inspection Vectors

### A. Unregistered "Ghost Files" Detection (Critical)
A very common senior developer trap: creating an XML view, security file, or JS component that physically exists on disk, but forgetting to register it in `__manifest__.py`.
- **Manifest `'data'` Check**: Scans `views/`, `data/`, `security/`, `wizard/`, `report/` for all `.xml` and `.csv` files. Every file must be declared in `'data'` or `'demo'`.
- **Manifest `'assets'` Check**: Scans `static/src/` for all `.js`, `.scss`, and `.xml` templates. Every asset must be matched by an entry or glob pattern in `'assets'` under `'web.assets_backend'` or declared asset bundles.

### B. Python Cascade Import Audit (`__init__.py`)
Odoo only loads Python models if they are imported into the module's namespace via `__init__.py`:
- Root `__init__.py` must import every subdirectory containing Python files (e.g., `from . import models`, `from . import wizard`, `from . import controllers`).
- Subdirectory `models/__init__.py` must import every `.py` file inside `models/`.
- Flags any "orphaned" Python file that will never be loaded by the Odoo registry.

### C. Git Conflict Markers & Corrupted Bytecode
- Detects unresolved Git merge conflicts:
  - `<<<<<<< HEAD`
  - `=======`
  - `>>>>>>> branch`
- Detects stray backup and swap files: `.swp`, `~`, `.bak`, `.orig`, `.DS_Store`.

### D. Circular Module Dependencies
- Analyzes the `'depends'` list in `__manifest__.py` across all modules in the repository.
- Detects circular dependency chains (e.g. Module A depends on Module B, which depends on Module A), which cause server boot failure.

### E. Standard Directory Structure Compliance
Verifies the canonical Odoo architecture:
```
my_module/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── my_model.py
├── views/
│   ├── my_model_views.xml
│   └── menus.xml
├── security/
│   ├── ir.model.access.csv
│   └── record_rules.xml
├── data/
│   └── sequence_data.xml (with noupdate="1")
├── static/
│   └── src/
│       ├── js/
│       ├── scss/
│       └── xml/
└── tests/
    ├── __init__.py
    └── test_my_model.py
```

---

## 2. Using the Folder Auditor Tool

Audit an entire module or repository folder:
```bash
odoo-dev folder-audit /path/to/my_module
odoo-dev folder-audit /path/to/custom_addons/
```
The tool reports all unregistered files, unimported Python models, merge artifacts, and directory health scores.
