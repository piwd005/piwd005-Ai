# Private-Ai: Global AI Developer Suite & Engineering Kit

Complete, production-hardened AI developer environment containing **32+ specialized engineering skills**, the **Primacy AI Engineering Kit**, the **odoo-dev MCP Server with 13 tools**, **4 AI specialist subagent directives**, **Global Engineering Directives (AGENTS.md & GEMINI.md)**, and the **odoo-dev CLI**.

This repository allows you to sync and install your exact AI configuration to any other PC in a single command.

---

## 🚀 Quick Install on Any Other PC

Clone this private repository onto your new machine and run the installer:

```bash
# 1. Clone your private repository
git clone https://github.com/piwd005/Private-Ai.git ~/Private-Ai

# 2. Enter repository and run the 1-click installer
cd ~/Private-Ai
./install.sh
```

Restart your Antigravity / AI assistant session, and all skills, MCP tools, and rules are immediately active!

---

## 📦 What's Included

### 1. Global AI Engineering Skills (`skills/`)
All 32+ skills installed to `~/.gemini/config/skills/`, globally active across every conversation:
- **Primacy AI Engineering Kit (`primacy-engineering`)**: 24 on-demand playbooks, 6 profiles, bounded static addon mapper (`map_addon.py`), QA runner (`qa.py`), and source catalog.
- **Odoo Architecture & Development**:
  - `odoo19-senior-dev`, `odoo20-senior-dev`
  - `odoo-ai-scaffold`, `odoo-architectural-blueprint`
  - `odoo-functional-consultant`, `odoo-solution-architect`
  - `odoo-owl`, `odoo-owl-mastery`
  - `odoo-performance-database`, `odoo-debugging-guru`
  - `odoo-migration`, `odoo-data-migration`
  - `odoo-enterprise-parity`, `odoo-spec-analyzer`
  - `odoo-guidelines`, `odoo-web-guidelines`, `odoo-security`
  - `odoo-test-generator`, `odoo-visual-inspector`
- **Quality & Safety Audits**:
  - `odoo-file-auditor` (AST security, unsafe sudo, compute loops)
  - `odoo-folder-auditor` (Ghost files, cascade imports)
  - `odoo-db-auditor` (Foreign key indexes, financial balancing, orphaned XML IDs)
- **Efficiency & Anti-Bloat Suite**:
  - `ponytail`, `ponytail-audit`, `ponytail-review`, `ponytail-debt`, `ponytail-gain`, `ponytail-help`

### 2. Global Directives & Invariance Rules (`AGENTS.md` & `GEMINI.md`)
Enforces unconditionally across every chat turn:
- **Quad Persona Mandate**: Functional Consultant, Solution Architect, Implementation Developer, QA Inspector.
- **15 Unbreakable Laws of Principal Odoo Engineering**: Modern `<list>` views, `<chatter/>`, direct expressions, batch ORM, defensive relational navigation.
- **4-Stage Pre-Upgrade Safety Gate**: Static AST & DB audit, zero-defect remediation gate, controlled upgrade, visual screenshot verification.
- **Primacy AI Engineering Kit Integration Law**: Playbook selection, navigation profiles, L1/L2/L3 evidence validation.

### 3. odoo-dev MCP Server (`plugins/odoo-dev/`)
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
12. `odoo_audit_database`: PostgreSQL health check (unindexed FKs, balanced ledgers).
13. `odoo_pre_upgrade_audit`: Combined 6-vector pre-upgrade safety audit.

### 4. odoo-dev Command-Line Tool (`bin/odoo-dev`)
Installed to `~/.local/bin/odoo-dev` for direct terminal usage:
```bash
odoo-dev lint /path/to/module
odoo-dev validate-manifest /path/to/module
odoo-dev validate-xml /path/to/module/views
odoo-dev pre-upgrade /path/to/module
odoo-dev screenshot --url http://localhost:8069 --output page.png
odoo-dev db-audit --db mydb --user admin --password admin
```

---

## 🔄 Syncing Updates

Whenever you improve your skills, directives, or tools:

```bash
# On your development PC:
cd ~/Private-Ai
git pull
./install.sh

# To push changes:
git add .
git commit -m "feat: update skills and rules"
git push origin main
```
