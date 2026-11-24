# 🛡️ piwd005-Ai Workstation Backup & 1-Click Disaster Recovery

This directory contains the full, production-hardened backup archive of the **piwd005-Ai Developer Suite** and the complete AI engineering workstation environment.

With this backup stored directly in the repository and on the `backup` branch, you can restore your complete AI pair programming environment to any machine or VPS in seconds with zero manual configuration.

---

## 📦 What is Included in the Backup Archive?

`workstation_full_backup.tar.gz` (~5.8 MB) packages:
1. **Developer Seniority Directives & Memory (`AGENTS.md`, `GEMINI.md`)**:
   - Universal Hexa-Persona Mandate.
   - 15 Unbreakable Laws of Principal Odoo Engineering (Odoo 19 & 20).
   - Proven Developer Trajectory: Senior Odoo Developer (since 2025), Android Developer, Senior Laravel Developer (since 2023), Senior CodeIgniter Developer (since 2021), Core PHP & MySQL (since 2019).
2. **40+ AI Engineering Skills**:
   - Odoo 19 & 20 senior development, OWL 2.0, architectural blueprint, migrations, security audit, database health.
   - Polyglot & Multi-Stack Skills: Laravel Senior Architect, CodeIgniter Senior Dev, Android Kotlin Jetpack Compose, Universal Architect, Fullstack Dev, Security Auditor, QA Inspector.
3. **Plugins & MCP Servers**:
   - `odoo-dev`: AST linter, pre-upgrade safety gate, XPath verifier, XML auditor.
   - `super-dev`: Polyglot C4 blueprint generator, security SAST scanner, PHP scaffolding engine (Laravel Action/Request/Model, CodeIgniter Service/Repository/Controller).
4. **CLI Executables**:
   - `odoo-dev` and `super-dev` installed directly to `~/.local/bin/`.
5. **Configuration & MCP Schemas**:
   - Dynamic and pre-packaged MCP server schemas (`odoo-dev`, `super-dev`).

---

## 🚀 1-Click Restore Instructions

### Option A: From Cloned Repo (`main` branch)
```bash
git clone https://github.com/piwd005/piwd005-Ai.git
cd piwd005-Ai/backup
chmod +x restore.sh
./restore.sh
```

### Option B: From Dedicated `backup` Branch
```bash
git clone -b backup https://github.com/piwd005/piwd005-Ai.git
cd piwd005-Ai/backup
chmod +x restore.sh
./restore.sh
```

### Option C: Quick Curl / Single Command (if downloaded archive directly)
```bash
tar -xzf workstation_full_backup.tar.gz -C "$HOME"
cd "$HOME/odoo_antigravity_sync"
./install.sh
```

---

## ✅ Post-Restore Verification

After running `restore.sh`, verify that everything is active:
```bash
# Verify CLI tools
odoo-dev --help
super-dev --help

# Run system diagnostic
super-dev doctor
odoo-dev doctor
```
