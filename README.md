# piwd005-Ai: Global AI Developer Suite & Primacy Engineering Kit

A unified, production-hardened AI developer environment combining the official **Primacy AI Engineering Kit v0.3.5** with the **Workstation Odoo Developer Suite**: **32+ specialized engineering skills**, **4 AI specialist subagent personas**, **18 Unbreakable Laws of Principal Odoo Engineering**, the **odoo-dev MCP Server with 13 tools**, and the **odoo-dev CLI**.

This repository integrates senior engineering standards with complete multi-PC portability.

---

## 🚀 Quick Install on Any Workstation

Clone this repository onto any new machine or development environment and execute the 1-click installer:

```bash
# 1. Clone your repository
git clone https://github.com/piwd005/piwd005-Ai.git ~/piwd005-Ai

# 2. Enter repository and run the 1-click installer
cd ~/piwd005-Ai
./install.sh
```

Restart your Antigravity / AI assistant session, and all skills, MCP tools, subagents, and rules are immediately active!

---

## 🏗 Key Components & Architecture

### 1. Primacy AI Engineering Kit (v0.3.5)
Directly imported from senior engineering (`https://github.com/primacyinfotechpvtltd/Primacy-AI-Engineering-Kit.git`):
- **Canonical Skill (`skills/primacy-engineering/`)**: 24 on-demand playbooks, 6 navigation profiles, bounded static addon mapper (`map_addon.py`), QA runner (`qa.py`), and 54 behavioral evaluation specifications.
- **Client Adapters (`adapters/`)**: Multi-client support for Antigravity (`adapters/antigravity/run.py`), Codex (`adapters/codex/`), and Claude Code (`adapters/claude-code/`), unified via `adapters/install.py`.
- **Registry & Source Catalog (`registry/`)**: Candidate admission, route mappings (`routes.json`), source indexing (`sources.json`), and locked dependencies (`dependencies.lock.json`).
- **Comprehensive Documentation & Evidence (`docs/` & `evaluations/`)**: 19 detailed technical reports including Native Odoo testing, Odoo 20 browser verification, Indian GST & multicurrency settlement, PriERP GST/EDI sandboxes, and security notes.
- **Automated Test Suite (`tests/`)**: 20 unit tests covering catalog QA, fixture isolation, and installation mechanics:
  ```bash
  python3 -m unittest discover -s tests -v
  python3 scripts/build_catalog.py --check
  ```

---

### 2. Global AI Engineering Skills (`skills/`)
32+ specialized skills installed to `~/.gemini/config/skills/`, globally active across every conversation:
* **Primacy AI Engineering**:
  * `primacy-engineering` (24 playbooks, 6 profiles, bounded static mapper, Indian GST/EDI evidence)
* **Odoo Core Architecture & Development**:
  * `odoo19-senior-dev`, `odoo20-senior-dev`
  * `odoo-ai-scaffold`, `odoo-architectural-blueprint`
  * `odoo-functional-consultant`, `odoo-solution-architect`
  * `odoo-owl`, `odoo-owl-mastery`
  * `odoo-performance-database`, `odoo-debugging-guru`
  * `odoo-migration`, `odoo-data-migration`
  * `odoo-enterprise-parity`, `odoo-spec-analyzer`
  * `odoo-guidelines`, `odoo-web-guidelines`, `odoo-security`
  * `odoo-test-generator`, `odoo-visual-inspector`
* **Quality, Health & Safety Audits**:
  * `odoo-file-auditor` (AST security, unsafe sudo, compute loops, N+1 queries)
  * `odoo-folder-auditor` (Ghost files, cascade imports, circular dependencies)
  * `odoo-db-auditor` (Unindexed foreign keys, orphaned XML IDs, double-entry financial balancing, stock valuation layers)
* **Efficiency & Anti-Bloat Suite**:
  * `ponytail`, `ponytail-audit`, `ponytail-review`, `ponytail-debt`, `ponytail-gain`, `ponytail-help`

---

### 3. Global Directives & Invariance Rules (`AGENTS.md` & `GEMINI.md`)
Enforces unconditionally across every chat turn on this workstation:
* **The Quad Persona Mandate**: Simultaneously thinking and acting as:
  1. *Lead Functional Consultant* (Standard-first evaluation, financial ledger balancing `debit == credit`, AVCO/FIFO stock valuation).
  2. *Chief Solution Architect* (Modular decoupling, one-model-per-file in `models/`, multi-company boundaries, async queues).
  3. *Principal Implementation Developer* (Zero-defect batch ORM, `<list>`, `<chatter/>`, direct expressions, OWL 2.0 `useService`).
  4. *Principal QA Inspector* (Pre-Upgrade Safety Gate, visual screenshot verification, database health audits).
* **The 18 Unbreakable Laws of Principal Odoo Engineering**:
  1. Every Button Must Work Interactive Law
  2. Zero-Tolerance for Guessed XPaths
  3. Defensive Relational Field Navigation
  4. Modern View Syntax & Tags (`<list>`, `<chatter/>`, direct expressions, `_compute_display_name`)
  5. Selection Field Type Integrity (Strings `'0'`, `'1'`, `'2'`, `'3'`)
  6. Safe System Parameters (`res.config.settings` with typed getters/setters)
  7. Professional QWeb Report Architecture (`<t t-set="address">`)
  8. High-Performance Batch ORM & Safe SQL (`create(self, vals_list)`)
  9. OWL 2.0 Web Components & Hoot Testing (`@odoo/hoot`)
  10. Complete Interactive Lifecycle for Business Models
  11. Concurrency & Deadlock Prevention (`SELECT FOR UPDATE` ID ordering)
  12. Systematic Parity & Zero Duplicate Fields (6-dimension audits)
  13. Architectural Pre-Flight Blueprint (`odoo-dev blueprint <model>`)
  14. Strict Batch ORM & Zero Loop DB Calls
  15. Modern Odoo 20 Declarative Constraints, Indexes & Typing Law (`models.Constraint`, `BinaryBytes`)
  16. Absolute Mobile Responsiveness & Boundless Root Architecture Law
  17. Manufacturing Scheduling & Interactive Gantt Timeline Law (`mrp.workorder` topological sort, ORM flush)
  18. Mobile Navigation Drawer Z-Index & Full-Height Stacking Law (`z-index: 1090 !important` over modal backdrops)
* **The 4-Stage Pre-Upgrade Safety Gate**:
  1. *Stage 1*: Static risk assessment (`odoo-dev pre-upgrade <module>`) before touching database.
  2. *Stage 2*: 100% issue remediation gate.
  3. *Stage 3*: Controlled module upgrade (`odoo-bin -u <module> --stop-after-init`).
  4. *Stage 4*: Server runtime screenshot inspection (`odoo-dev screenshot`) and database health audit (`odoo-dev db-audit`).

---

### 4. odoo-dev MCP Server & Subagents (`plugins/odoo-dev/`)
13 production-grade MCP tools connected via Model Context Protocol:
1. `odoo_pylint`: Run pylint-odoo on any file or module.
2. `odoo_validate_manifest`: Check manifests, required keys, and file paths on disk.
3. `odoo_validate_xml`: Well-formedness and verified XPath targets check.
4. `odoo_version_compat_check`: Scan for cross-version deprecations (Odoo 16 -> 20).
5. `odoo_rpc_ping`: Ping live Odoo instances via JSON-RPC.
6. `odoo_model_inspect`: Inspect database schema, fields, and types via live RPC.
7. `odoo_read_file`: Parse PDFs, Excel spreadsheets, Word docs, and CSVs.
8. `odoo_scaffold_module`: Scaffold production-grade modules with zero guesswork.
9. `odoo_capture_page`: Playwright browser visual page captures and crash modal detection.
10. `odoo_audit_file`: AST-level deep inspection for security vulnerabilities.
11. `odoo_audit_module_folder`: Detect ghost files and missing imports.
12. `odoo_audit_database`: PostgreSQL health check (unindexed FKs, balanced ledgers, SVL, cross-company leaks).
13. `odoo_pre_upgrade_audit`: Combined 6-vector pre-upgrade safety audit.

**4 Registered Subagent Personas (`plugins/odoo-dev/agents/`)**:
- `odoo-elite-developer`: Implementation specialist for zero-defect ORM, OWL 2.0, and Hoot testing.
- `odoo-functional-director`: Enterprise business process mapping, double-entry accounting, and inventory costing.
- `odoo-principal-architect`: Enterprise system design, modular decoupling, multi-company scaling, and async integrations.
- `odoo-qa-inspector`: Pre-upgrade gatekeeper, Playwright automated visual page capture, and database health auditor.

---

### 5. odoo-dev CLI Utility (`bin/odoo-dev`)
Installed to `~/.local/bin/odoo-dev` for direct terminal execution:
```bash
# 1. Pre-Upgrade Safety Gate (Stage 1 Audit)
odoo-dev pre-upgrade /path/to/addon

# 2. Architectural Blueprint Generator
odoo-dev blueprint custom.maintenance

# 3. Headless Chromium Full-Page Screenshot & Crash Detector
odoo-dev screenshot --url http://localhost:8069 --login admin --password admin --action-url "/odoo/action-123"

# 4. PostgreSQL Database Health & Multi-Company Auditor
odoo-dev db-audit <dbname> --user odoo --host localhost

# 5. AST & File Security Auditor
odoo-dev file-audit /path/to/file.py

# 6. Ghost File & Cascade Import Auditor
odoo-dev folder-audit /path/to/addons

# 7. Production Addon Scaffolder
odoo-dev scaffold custom_module --version 19.0 --model custom.module

# 8. Linting & Manifest / XML Validation
odoo-dev lint /path/to/addon
odoo-dev validate-manifest /path/to/addon
odoo-dev validate-xml /path/to/addon/views
```

---

## 🔄 Development & Syncing Workflow

Whenever you improve your skills, directives, or tools:

```bash
# On your development PC:
cd ~/piwd005-Ai
git pull
./install.sh

# Run test suite:
python3 -m unittest discover -s tests -v
python3 scripts/build_catalog.py --check

# Push improvements:
git add .
git commit -m "feat: sync primacy engineering kit and latest workstation capabilities"
git push origin main
```
