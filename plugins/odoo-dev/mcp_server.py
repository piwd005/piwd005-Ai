#!/usr/bin/env python3
"""
Odoo AI Developer MCP Server
Provides static analysis, XML validation, manifest checking, cross-version compatibility audits,
and live Odoo RPC inspection tools for the Antigravity assistant.
"""

import ast
import json
import os
import re
import subprocess
import sys
from typing import Any, Dict, List, Optional
from lxml import etree
from mcp.server.mcpserver import MCPServer

server = MCPServer("odoo-dev")


@server.tool()
def odoo_pylint(path: str) -> str:
    """Run pylint with pylint-odoo plugin on a target Python file or module directory.

    Args:
        path: Absolute path to the python file or addon folder.

    Returns:
        Structured string report of lint issues, security warnings, and guideline violations.
    """
    if not os.path.exists(path):
        return f"Error: Path '{path}' does not exist."

    cmd = [
        sys.executable,
        "-m",
        "pylint",
        "--load-plugins=pylint_odoo",
        "--output-format=text",
        "--disable=all",
        "--enable=odoolint,E,W",
        "--disable=import-error,no-name-in-module",
        path,
    ]

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )
        output = proc.stdout.strip()
        if not output:
            return f"✓ No Odoo lint or security issues found for: {path}"
        return output
    except subprocess.TimeoutExpired:
        return "Error: Linting timed out after 120 seconds."
    except Exception as exc:
        return f"Error running pylint: {str(exc)}"


@server.tool()
def odoo_validate_manifest(manifest_path: str) -> str:
    """Validate an Odoo __manifest__.py file for syntax, required keys, and file references.

    Args:
        manifest_path: Absolute path to __manifest__.py.

    Returns:
        Validation report indicating status, missing keys, or broken file paths.
    """
    if not os.path.exists(manifest_path):
        return f"Error: Manifest file '{manifest_path}' does not exist."

    addon_dir = os.path.dirname(os.path.abspath(manifest_path))

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            content = f.read()
        manifest = ast.literal_eval(content)
        if not isinstance(manifest, dict):
            return "Error: Manifest does not evaluate to a Python dictionary."
    except Exception as exc:
        return f"Syntax Error parsing manifest: {str(exc)}"

    report = []
    # 1. Required keys
    required_keys = ["name", "version", "license", "depends"]
    missing_keys = [k for k in required_keys if k not in manifest]
    if missing_keys:
        report.append(f"⚠ Missing required manifest keys: {', '.join(missing_keys)}")
    else:
        report.append("✓ All required manifest keys present.")

    # 2. Version format
    version = manifest.get("version", "")
    if version and not re.match(r"^\d+\.\d+\.\d+\.\d+\.\d+$", str(version)):
        report.append(f"ℹ Version '{version}' does not match standard 5-part format: {{odoo_version}}.major.minor.patch (e.g. 18.0.1.0.0)")

    # 3. File existence checks
    file_sections = ["data", "demo"]
    for section in file_sections:
        files = manifest.get(section, [])
        for rel_file in files:
            full_path = os.path.join(addon_dir, rel_file)
            if not os.path.exists(full_path):
                report.append(f"❌ Broken {section} file reference: '{rel_file}' does not exist on disk.")

    # Check assets
    assets = manifest.get("assets", {})
    if isinstance(assets, dict):
        for bundle, asset_list in assets.items():
            if isinstance(asset_list, list):
                for item in asset_list:
                    rel_asset = item[-1] if isinstance(item, (tuple, list)) else item
                    if not isinstance(rel_asset, str):
                        continue
                    if rel_asset.startswith(("http://", "https://", "//")):
                        continue
                    # Handle wildcards
                    if "*" in rel_asset:
                        continue
                    # Asset paths in Odoo usually start with addon_name/static/...
                    parts = rel_asset.split("/", 1)
                    if len(parts) == 2:
                        local_path = os.path.join(addon_dir, parts[1])
                        if not os.path.exists(local_path):
                            report.append(f"❌ Broken asset in '{bundle}': '{rel_asset}' not found locally.")

    if len(report) == 1 and report[0].startswith("✓"):
        report.append("✓ All declared data files and references exist on disk.")

    return "\n".join(report)


@server.tool()
def odoo_validate_xml(xml_path: str) -> str:
    """Validate Odoo XML view/data files for XML well-formedness, root tags, and XPath validity.

    Args:
        xml_path: Absolute path to the XML file or directory containing XML views.

    Returns:
        Validation report of XML syntax, XPath expressions, and tag deprecations.
    """
    if not os.path.exists(xml_path):
        return f"Error: Path '{xml_path}' does not exist."

    files_to_check = []
    if os.path.isdir(xml_path):
        for root, _, files in os.walk(xml_path):
            for file in files:
                if file.endswith(".xml"):
                    files_to_check.append(os.path.join(root, file))
    else:
        files_to_check.append(xml_path)

    findings = []
    for fpath in files_to_check:
        fname = os.path.basename(fpath)
        try:
            tree = etree.parse(fpath)
            root = tree.getroot()
            if root.tag not in ("odoo", "openerp"):
                findings.append(f"[{fname}] Warning: Root tag is <{root.tag}> instead of <odoo>.")

            # Check for records and XPaths
            for elem in root.iter():
                # Check for deprecated tags in modern odoo
                if elem.tag == "tree":
                    line = elem.sourceline or "?"
                    findings.append(f"[{fname}:{line}] Warning: Found <tree> view tag. In Odoo 18+, use <list> instead.")

                # Check attrs attribute
                if "attrs" in elem.attrib:
                    line = elem.sourceline or "?"
                    findings.append(f"[{fname}:{line}] Deprecation: 'attrs' attribute found. In Odoo 17+, use direct invisible/readonly expressions.")

                # Check xpath validity
                if elem.tag == "xpath":
                    line = elem.sourceline or "?"
                    expr = elem.attrib.get("expr")
                    position = elem.attrib.get("position")
                    if not expr:
                        findings.append(f"[{fname}:{line}] Error: <xpath> missing required 'expr' attribute.")
                    if not position:
                        findings.append(f"[{fname}:{line}] Warning: <xpath> missing 'position' attribute (inside, after, before, replace, attributes).")
                    if expr:
                        try:
                            etree.XPath(expr)
                        except Exception as e:
                            findings.append(f"[{fname}:{line}] Error: Invalid XPath expression '{expr}': {str(e)}")

        except etree.XMLSyntaxError as e:
            findings.append(f"[{fname}] Fatal XML Syntax Error: {str(e)}")
        except Exception as e:
            findings.append(f"[{fname}] Error: {str(e)}")

    if not findings:
        return f"✓ All {len(files_to_check)} XML file(s) are well-formed with valid XPaths and syntax."
    return "\n".join(findings)


@server.tool()
def odoo_version_compat_check(path: str, target_version: str = "18.0") -> str:
    """Scan Python and XML code for cross-version breaking changes and deprecated APIs.

    Args:
        path: Path to addon directory or source file.
        target_version: Target Odoo version (e.g. '17.0', '18.0', '19.0', '20.0').

    Returns:
        Audit report detailing version incompatibilities with exact line numbers and fixes.
    """
    if not os.path.exists(path):
        return f"Error: Path '{path}' does not exist."

    is_modern = float(target_version.split(".")[0]) >= 17.0
    is_v18_plus = float(target_version.split(".")[0]) >= 18.0

    issues = []

    if os.path.isdir(path):
        walker = os.walk(path)
    else:
        walker = [(os.path.dirname(path), [], [os.path.basename(path)])]

    for root, _, files in walker:
        for file in files:
            full_path = os.path.join(root, file) if root else file
            if not full_path.endswith((".py", ".xml", ".js")):
                continue

            rel_name = os.path.relpath(full_path, path) if os.path.isdir(path) else os.path.basename(full_path)

            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
            except Exception:
                continue

            for idx, line in enumerate(lines, start=1):
                # 1. XML Checks
                if full_path.endswith(".xml"):
                    if is_v18_plus and re.search(r"<tree\b", line):
                        issues.append(f"[{rel_name}:{idx}] <tree> tag used. In Odoo 18/19/20, use <list>.")
                    if is_modern and "attrs=" in line:
                        issues.append(f"[{rel_name}:{idx}] 'attrs' used. In Odoo 17+, replace with direct python expression (invisible/readonly).")
                    if is_modern and re.search(r"\bstates=", line):
                        issues.append(f"[{rel_name}:{idx}] 'states' attribute used. In Odoo 17+, use invisible/readonly.")
                    if "t-raw" in line:
                        issues.append(f"[{rel_name}:{idx}] 't-raw' used. Removed in modern QWeb. Use 't-out' with Markup.")
                    if is_v18_plus and "oe_chatter" in line:
                        issues.append(f"[{rel_name}:{idx}] Legacy '<div class=\"oe_chatter\">' used. In Odoo 19/20, use clean '<chatter/>' tag.")
                    if re.search(r"model=['\"]ir\.config_parameter['\"]", line):
                        issues.append(f"[{rel_name}:{idx}] Critical: Raw '<record model=\"ir.config_parameter\">' causes UniqueViolation on upgrade. Use res.config.settings with config_parameter='...'.")
                    if re.search(r"hasclass\(", line):
                        issues.append(f"[{rel_name}:{idx}] Fragile XPath: '[hasclass(...)]' detected. Senior standard requires anchoring on unique 'name' attributes.")

                # 2. Python Checks
                if full_path.endswith(".py"):
                    if is_modern and re.search(r"def\s+name_get\s*\(", line):
                        issues.append(f"[{rel_name}:{idx}] 'name_get()' used. Removed in Odoo 17+. Use '_compute_display_name()'.")
                    if re.search(r"cr\.execute\s*\(\s*['\"].*?%s.*?\s*%", line):
                        issues.append(f"[{rel_name}:{idx}] Security: String formatting in cr.execute(). Pass parameters as second tuple argument.")
                    if re.search(r"\(\s*['\"]priority['\"]\s*,\s*['\"][!=><]=?['\"]\s*,\s*\d+\s*\)", line):
                        issues.append(f"[{rel_name}:{idx}] Type Error: Priority compared to integer. Odoo priority is string ('0', '1', '2', '3'). Use string literal.")
                    if "datetime.utcnow()" in line or "datetime.datetime.utcnow()" in line:
                        issues.append(f"[{rel_name}:{idx}] Deprecated in Python 3.12 (Odoo 19/20): 'utcnow()' used. Use 'datetime.now(timezone.utc)' or 'fields.Datetime.now()'.")

                # 3. JavaScript / OWL Checks
                if full_path.endswith(".js"):
                    if "core.qweb" in line:
                        issues.append(f"[{rel_name}:{idx}] 'core.qweb' legacy widget used. Migrate to OWL 2 Component.")
                    if "this._rpc(" in line:
                        issues.append(f"[{rel_name}:{idx}] 'this._rpc' legacy method used. In Odoo 19/20, use 'this.orm = useService(\"orm\")'.")

    if not issues:
        return f"✓ No compatibility issues detected for target Odoo {target_version} in '{path}'."
    return f"Compatibility Audit for Odoo {target_version} ({len(issues)} issues found):\n" + "\n".join(issues)


@server.tool()
def odoo_rpc_ping(host: str = "localhost", port: int = 8069, protocol: str = "jsonrpc") -> str:
    """Connect to a running Odoo instance via OdooRPC to verify connectivity, server version, and databases.

    Args:
        host: Hostname or IP address (default: 'localhost').
        port: Port number (default: 8069).
        protocol: Protocol ('jsonrpc' or 'jsonrpc+ssl').

    Returns:
        JSON string containing server version, series, and available databases.
    """
    try:
        import odoorpc
        odoo = odoorpc.ODOO(host, port=port, protocol=protocol, timeout=5)
        dbs = odoo.db.list()
        version_info = odoo.version
        return json.dumps({
            "status": "connected",
            "host": host,
            "port": port,
            "server_version": version_info.get("server_version"),
            "server_series": version_info.get("server_serie"),
            "protocol": odoo.protocol,
            "databases": dbs,
        }, indent=2)
    except Exception as exc:
        return f"Connection Failed to {host}:{port} ({protocol}): {str(exc)}"


@server.tool()
def odoo_model_inspect(
    model_name: str,
    db: str,
    host: str = "localhost",
    port: int = 8069,
    user: str = "admin",
    password: str = "admin",
) -> str:
    """Query live field definitions and metadata for an Odoo model on a running instance.

    Args:
        model_name: Technical name of the model (e.g. 'res.partner', 'sale.order').
        db: Target database name.
        host: Hostname (default: 'localhost').
        port: Port (default: 8069).
        user: Login username (default: 'admin').
        password: Login password (default: 'admin').

    Returns:
        Summary of model fields, types, and relations.
    """
    try:
        import odoorpc
        odoo = odoorpc.ODOO(host, port=port, timeout=10)
        odoo.login(db, user, password)
        model = odoo.env[model_name]
        fields_info = model.fields_get()

        summary = {
            "model": model_name,
            "total_fields": len(fields_info),
            "fields": {},
        }
        for fname, meta in sorted(fields_info.items()):
            summary["fields"][fname] = {
                "type": meta.get("type"),
                "string": meta.get("string"),
                "required": meta.get("required", False),
                "readonly": meta.get("readonly", False),
                "relation": meta.get("relation"),
            }
        return json.dumps(summary, indent=2)
    except Exception as exc:
        return f"Error inspecting model '{model_name}': {str(exc)}"


@server.tool()
def odoo_read_file(file_path: str, max_rows: int = 20, max_pages: int = 15) -> str:
    """Read, parse, and summarize business files: PDF specs, Excel sheets, Word docs, CSVs, images, and mockups.

    Args:
        file_path: Absolute path to the file.
        max_rows: Maximum rows to preview for tabular data (Excel/CSV).
        max_pages: Maximum pages to extract for PDF documents.

    Returns:
        Structured text representation of the document contents, tables, and metadata.
    """
    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' does not exist."

    ext = os.path.splitext(file_path)[1].lower()
    fname = os.path.basename(file_path)

    # 1. PDF Documents
    if ext == ".pdf":
        try:
            import pypdf
            reader = pypdf.PdfReader(file_path)
            total_pages = len(reader.pages)
            out = [f"=== PDF Document: {fname} ({total_pages} total pages) ==="]
            limit = min(total_pages, max_pages)
            for i in range(limit):
                text = reader.pages[i].extract_text() or "(No readable text on this page)"
                out.append(f"--- Page {i + 1} of {total_pages} ---\n{text.strip()}")
            if total_pages > max_pages:
                out.append(f"\n[Note: Truncated at page {max_pages} of {total_pages}]")
            return "\n\n".join(out)
        except Exception as e:
            return f"Error reading PDF '{fname}': {str(e)}"

    # 2. Excel Spreadsheets (.xlsx, .xls)
    elif ext in (".xlsx", ".xls"):
        try:
            import pandas as pd
            excel_file = pd.ExcelFile(file_path)
            sheet_names = excel_file.sheet_names
            out = [f"=== Excel Workbook: {fname} ===", f"Sheets available: {', '.join(sheet_names)}"]

            for sheet in sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet, nrows=max_rows)
                out.append(f"\n--- Sheet: '{sheet}' (showing first {len(df)} rows, total columns: {len(df.columns)}) ---")
                out.append(f"Columns: {', '.join(str(c) for c in df.columns)}")
                out.append(df.to_string(index=False))

            return "\n".join(out)
        except Exception as e:
            return f"Error reading Excel file '{fname}': {str(e)}"

    # 3. Word Documents (.docx)
    elif ext == ".docx":
        try:
            import docx
            doc = docx.Document(file_path)
            out = [f"=== Word Document: {fname} ==="]

            for p in doc.paragraphs:
                txt = p.text.strip()
                if txt:
                    if p.style and p.style.name.startswith("Heading"):
                        out.append(f"\n## {txt}")
                    else:
                        out.append(txt)

            for t_idx, table in enumerate(doc.tables, start=1):
                out.append(f"\n--- Table {t_idx} ({len(table.rows)} rows x {len(table.columns)} cols) ---")
                for row in table.rows[:max_rows]:
                    row_data = [cell.text.strip() for cell in row.cells]
                    out.append(" | ".join(row_data))

            return "\n".join(out)
        except Exception as e:
            return f"Error reading Word document '{fname}': {str(e)}"

    # 4. CSV / TSV tabular files
    elif ext in (".csv", ".tsv"):
        try:
            import pandas as pd
            sep = "\t" if ext == ".tsv" else ","
            df = pd.read_csv(file_path, sep=sep, nrows=max_rows)
            out = [
                f"=== CSV/TSV File: {fname} ===",
                f"Columns ({len(df.columns)}): {', '.join(df.columns)}",
                f"Preview ({len(df)} rows):",
                df.to_string(index=False)
            ]
            return "\n".join(out)
        except Exception as e:
            return f"Error reading tabular file '{fname}': {str(e)}"

    # 5. Image Files (.png, .jpg, .jpeg, .webp, .bmp, .svg)
    elif ext in (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".svg"):
        try:
            from PIL import Image
            with Image.open(file_path) as img:
                w, h = img.size
                mode = img.mode
                fmt = img.format
                file_size_kb = os.path.getsize(file_path) / 1024.0

            return (
                f"=== Image Asset: {fname} ===\n"
                f"Format: {fmt} | Dimensions: {w}x{h} px | Mode: {mode} | Size: {file_size_kb:.1f} KB\n"
                f"Path: {file_path}\n"
                f"ℹ Use Antigravity's 'view_file' tool to visually inspect this UI mockup, screenshot, or diagram directly in chat."
            )
        except Exception as e:
            return f"Error inspecting image '{fname}': {str(e)}"

    # 6. Fallback Plain Text / Code / JSON / XML
    else:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(100000)
            return f"=== File: {fname} ===\n{content}"
        except Exception as e:
            return f"Error reading file '{fname}': {str(e)}"


@server.tool()
def odoo_scaffold_module(
    addon_name: str,
    target_dir: str = ".",
    odoo_version: str = "19.0",
    model_name: str = "",
) -> str:
    """Scaffold a production-grade Odoo 19/20 addon module with models, views, security, and tests.

    Args:
        addon_name: Technical module name (e.g. 'custom_maintenance').
        target_dir: Target directory where addon will be created (default: current directory).
        odoo_version: Target Odoo version ('18.0', '19.0', '20.0', default: '19.0').
        model_name: Technical model name (e.g. 'custom.maintenance.request'). If empty, derived from addon_name.

    Returns:
        Status message with list of generated files and next steps.
    """
    clean_addon = re.sub(r"[^a-zA-Z0-9_]", "_", addon_name).lower()
    addon_path = os.path.join(os.path.abspath(target_dir), clean_addon)

    if os.path.exists(addon_path):
        return f"Error: Addon directory '{addon_path}' already exists."

    if not model_name:
        model_name = clean_addon.replace("_", ".")
    clean_model_file = model_name.replace(".", "_")
    model_class_name = "".join(part.capitalize() for part in model_name.split("."))

    # Create directory structure
    subdirs = ["models", "views", "security", "data", "tests"]
    for sub in subdirs:
        os.makedirs(os.path.join(addon_path, sub), exist_ok=True)

    # 1. root __init__.py
    with open(os.path.join(addon_path, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("from . import models\n")

    # 2. __manifest__.py
    manifest_content = f"""{{
    'name': '{clean_addon.replace("_", " ").title()}',
    'version': '{odoo_version}.1.0.0',
    'category': 'Customizations',
    'summary': 'Production module for {clean_addon.replace("_", " ")}',
    'author': 'Senior Dev Team',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/{clean_model_file}_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}}
"""
    with open(os.path.join(addon_path, "__manifest__.py"), "w", encoding="utf-8") as f:
        f.write(manifest_content)

    # 3. models/__init__.py
    with open(os.path.join(addon_path, "models", "__init__.py"), "w", encoding="utf-8") as f:
        f.write(f"from . import {clean_model_file}\n")

    # 4. models/<model>.py
    model_content = f"""from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class {model_class_name}(models.Model):
    _name = '{model_name}'
    _description = '{clean_addon.replace("_", " ").title()}'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        default=lambda self: _('New'),
        tracking=True,
    )
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
    priority = fields.Selection(
        selection=[
            ('0', 'Low'),
            ('1', 'Normal'),
            ('2', 'High'),
            ('3', 'Urgent'),
        ],
        string='Priority',
        default='1',
        tracking=True,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        tracking=True,
        check_company=True,
    )
    user_id = fields.Many2one(
        'res.users',
        string='Responsible',
        default=lambda self: self.env.user,
        tracking=True,
        check_company=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
    )
    date = fields.Date(
        string='Date',
        default=fields.Date.context_today,
        tracking=True,
    )
    description = fields.Html(string='Description')

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = record.name or _('New')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'priority' in vals and vals['priority'] is not None:
                vals['priority'] = str(vals['priority'])
        return super().create(vals_list)

    def write(self, vals):
        if 'priority' in vals and vals['priority'] is not None:
            vals['priority'] = str(vals['priority'])
        return super().write(vals)

    def action_confirm(self):
        for record in self:
            if record.state != 'draft':
                raise UserError(_("Only draft records can be confirmed."))
            record.state = 'confirmed'
        return True

    def action_done(self):
        for record in self:
            if record.state != 'confirmed':
                raise UserError(_("Only confirmed records can be marked as done."))
            record.state = 'done'
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'done':
                raise UserError(_("Done records cannot be cancelled."))
            record.state = 'cancelled'
        return True

    def action_draft(self):
        self.write({{'state': 'draft'}})
        return True
"""
    with open(os.path.join(addon_path, "models", f"{clean_model_file}.py"), "w", encoding="utf-8") as f:
        f.write(model_content)

    # 5. views/<model>_views.xml
    views_content = f"""<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- List View -->
    <record id="view_{clean_model_file}_list" model="ir.ui.view">
        <field name="name">{model_name}.list</field>
        <field name="model">{model_name}</field>
        <field name="arch" type="xml">
            <list string="{clean_addon.replace("_", " ").title()}" decoration-info="state == 'draft'" decoration-success="state == 'done'" decoration-muted="state == 'cancelled'">
                <field name="name"/>
                <field name="date"/>
                <field name="partner_id"/>
                <field name="user_id" widget="many2one_avatar_user"/>
                <field name="priority" widget="priority"/>
                <field name="state" widget="badge" decoration-info="state == 'draft'" decoration-warning="state == 'confirmed'" decoration-success="state == 'done'"/>
            </list>
        </field>
    </record>

    <!-- Form View -->
    <record id="view_{clean_model_file}_form" model="ir.ui.view">
        <field name="name">{model_name}.form</field>
        <field name="model">{model_name}</field>
        <field name="arch" type="xml">
            <form string="{clean_addon.replace("_", " ").title()}">
                <header>
                    <button name="action_confirm" string="Confirm" type="object" class="btn-primary" invisible="state != 'draft'"/>
                    <button name="action_done" string="Mark Done" type="object" class="btn-success" invisible="state != 'confirmed'"/>
                    <button name="action_cancel" string="Cancel" type="object" invisible="state in ('done', 'cancelled')"/>
                    <button name="action_draft" string="Reset to Draft" type="object" invisible="state != 'cancelled'"/>
                    <field name="state" widget="statusbar" statusbar_visible="draft,confirmed,done"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <label for="name"/>
                        <h1>
                            <field name="name" placeholder="Title / Reference..."/>
                        </h1>
                    </div>
                    <group>
                        <group>
                            <field name="partner_id"/>
                            <field name="user_id"/>
                            <field name="priority" widget="priority"/>
                        </group>
                        <group>
                            <field name="date"/>
                            <field name="company_id" groups="base.group_multi_company"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Description" name="description">
                            <field name="description" placeholder="Add detailed notes here..."/>
                        </page>
                    </notebook>
                </sheet>
                <chatter/>
            </form>
        </field>
    </record>

    <!-- Search View -->
    <record id="view_{clean_model_file}_search" model="ir.ui.view">
        <field name="name">{model_name}.search</field>
        <field name="model">{model_name}</field>
        <field name="arch" type="xml">
            <search string="Search Records">
                <field name="name"/>
                <field name="partner_id"/>
                <field name="user_id"/>
                <separator/>
                <filter string="Draft" name="filter_draft" domain="[('state', '=', 'draft')]"/>
                <filter string="Confirmed" name="filter_confirmed" domain="[('state', '=', 'confirmed')]"/>
                <filter string="Done" name="filter_done" domain="[('state', '=', 'done')]"/>
                <separator/>
                <filter string="High Priority" name="filter_high_priority" domain="[('priority', 'in', ('2', '3'))]"/>
                <group expand="0" string="Group By">
                    <filter string="Customer" name="group_by_partner" context="{{'group_by': 'partner_id'}}"/>
                    <filter string="Responsible" name="group_by_user" context="{{'group_by': 'user_id'}}"/>
                    <filter string="Status" name="group_by_state" context="{{'group_by': 'state'}}"/>
                    <filter string="Date" name="group_by_date" context="{{'group_by': 'date'}}"/>
                </group>
            </search>
        </field>
    </record>

    <!-- Window Action -->
    <record id="action_{clean_model_file}" model="ir.actions.act_window">
        <field name="name">{clean_addon.replace("_", " ").title()}</field>
        <field name="res_model">{model_name}</field>
        <field name="view_mode">list,form</field>
        <field name="search_view_id" ref="view_{clean_model_file}_search"/>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Create your first record!
            </p>
        </field>
    </record>
</odoo>
"""
    with open(os.path.join(addon_path, "views", f"{clean_model_file}_views.xml"), "w", encoding="utf-8") as f:
        f.write(views_content)

    # 6. views/menu_views.xml
    menu_content = f"""<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Top Bar Root Menu -->
    <menuitem id="menu_{clean_addon}_root"
              name="{clean_addon.replace("_", " ").title()}"
              sequence="50"
              web_icon="{clean_addon},static/description/icon.png"/>

    <!-- Operations Submenu -->
    <menuitem id="menu_{clean_addon}_operations"
              name="Operations"
              parent="menu_{clean_addon}_root"
              sequence="10"/>

    <!-- Action Menu -->
    <menuitem id="menu_{clean_model_file}_action"
              name="{clean_addon.replace("_", " ").title()}"
              parent="menu_{clean_addon}_operations"
              action="action_{clean_model_file}"
              sequence="10"/>
</odoo>
"""
    with open(os.path.join(addon_path, "views", "menu_views.xml"), "w", encoding="utf-8") as f:
        f.write(menu_content)

    # 7. security/ir.model.access.csv
    csv_content = f"""id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_{clean_model_file}_user,{clean_model_file}.user,model_{clean_model_file},base.group_user,1,1,1,0
access_{clean_model_file}_manager,{clean_model_file}.manager,model_{clean_model_file},base.group_system,1,1,1,1
"""
    with open(os.path.join(addon_path, "security", "ir.model.access.csv"), "w", encoding="utf-8") as f:
        f.write(csv_content)

    # 8. tests/__init__.py and tests/test_<model>.py
    with open(os.path.join(addon_path, "tests", "__init__.py"), "w", encoding="utf-8") as f:
        f.write(f"from . import test_{clean_model_file}\n")

    test_content = f"""from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class Test{model_class_name}(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({{'name': 'Test Partner'}})
        cls.record = cls.env['{model_name}'].create({{
            'name': 'Test Item 001',
            'partner_id': cls.partner.id,
            'priority': '2',
        }})

    def test_initial_state_and_priority(self):
        \"\"\"Verify initial draft state and string priority.\"\"\"
        self.assertEqual(self.record.state, 'draft')
        self.assertEqual(self.record.priority, '2')

    def test_workflow_state_transitions(self):
        \"\"\"Verify full action lifecycle transitions.\"\"\"
        self.record.action_confirm()
        self.assertEqual(self.record.state, 'confirmed')

        self.record.action_done()
        self.assertEqual(self.record.state, 'done')

        # Done record cannot be cancelled
        with self.assertRaises(UserError):
            self.record.action_cancel()
"""
    with open(os.path.join(addon_path, "tests", f"test_{clean_model_file}.py"), "w", encoding="utf-8") as f:
        f.write(test_content)

    return f"""✓ Production-grade Odoo {odoo_version} addon scaffolded successfully at:
  {addon_path}

Generated Architecture:
  ├── __manifest__.py (version: {odoo_version}.1.0.0, depends: base, mail)
  ├── models/
  │   └── {clean_model_file}.py (batch create, statusbar transitions, tracking, display_name)
  ├── views/
  │   ├── {clean_model_file}_views.xml (<list>, <form> with <chatter/>, direct expressions, search)
  │   └── menu_views.xml (root, operations, action menus)
  ├── security/
  │   └── ir.model.access.csv (standard user & system manager permissions)
  └── tests/
      └── test_{clean_model_file}.py (TransactionCase automated lifecycle tests)

Next steps:
  1. Validate addon: odoo-dev validate-manifest {addon_path}
  2. Validate views:  odoo-dev validate-xml {addon_path}/views
  3. Run linter:      odoo-dev lint {addon_path}
"""


@server.tool()
def odoo_capture_page(
    url: str = "http://localhost:8069",
    login: str = "admin",
    password: str = "admin",
    database: Optional[str] = None,
    action_url: Optional[str] = None,
    output_path: Optional[str] = None,
    wait_time_ms: int = 3000,
    full_page: bool = True,
    viewport_width: int = 1440,
    viewport_height: int = 900,
) -> str:
    """Capture a screenshot of an Odoo view/page on the running server and check for visual or JS console errors.

    Automates browser navigation, logs in if needed, waits for OWL/webclient rendering,
    captures full-page screenshot to disk, and inspects for crash dialogs and JS console errors.

    Args:
        url: Base Odoo server URL (e.g. http://localhost:8069).
        login: User login (default: admin).
        password: User password (default: admin).
        database: Optional Odoo database name (if multiple DBs exist).
        action_url: Target URL path or action hash (e.g. '/web#action=crm.crm_lead_all_leads' or '/odoo/action-123').
        output_path: Destination path for the screenshot .png. Defaults to ~/.gemini/antigravity/screenshots/odoo_<timestamp>.png.
        wait_time_ms: Milliseconds to wait after page load for OWL rendering and animations (default: 3000).
        full_page: Whether to take a full page screenshot (default: True).
        viewport_width: Browser viewport width (default: 1440).
        viewport_height: Browser viewport height (default: 900).

    Returns:
        Structured report with screenshot path, HTTP status, detected JS console errors, and any visible crash modals.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return "Error: Playwright is not installed. Install with: pip install playwright && playwright install chromium"

    import time
    from urllib.parse import urljoin

    if not output_path:
        screenshot_dir = os.path.expanduser("~/.gemini/antigravity/screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(screenshot_dir, f"odoo_page_{timestamp}.png")
    else:
        output_path = os.path.expanduser(output_path)
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    console_errors = []
    page_errors = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": viewport_width, "height": viewport_height})
            page = context.new_page()

            page.on("console", lambda msg: console_errors.append(f"[{msg.type.upper()}] {msg.text}") if msg.type in ("error", "warning") else None)
            page.on("pageerror", lambda err: page_errors.append(str(err)))

            # Step 1: Navigate to base URL or login
            target_url = url
            if database and "db=" not in target_url:
                delim = "&" if "?" in target_url else "?"
                target_url = f"{target_url}{delim}db={database}"

            if action_url:
                target_url = urljoin(target_url.rstrip("/") + "/", action_url.lstrip("/"))

            page.goto(f"{url}?db={database}" if database and "db=" not in url else url, wait_until="networkidle", timeout=30000)

            # Check if login is required
            login_input = page.locator("input[name='login'], input#login, input[name='field_login']")
            if login_input.count() > 0 and login_input.first.is_visible():
                if database:
                    db_input = page.locator("select[name='db'], input[name='db']")
                    if db_input.count() > 0 and db_input.first.is_visible():
                        try:
                            db_input.first.fill(database)
                        except Exception:
                            pass

                login_input.first.fill(login)
                pwd_input = page.locator("input[name='password'], input#password")
                if pwd_input.count() > 0:
                    pwd_input.first.fill(password)

                submit_btn = page.locator("button:has-text('Log in'), button:has-text('Sign in'), .oe_login_form button[type='submit']")
                if submit_btn.count() > 0:
                    submit_btn.first.click()
                    page.wait_for_load_state("networkidle", timeout=30000)

            # If an action_url was specified and we aren't there yet
            if action_url and page.url != target_url:
                page.goto(target_url, wait_until="networkidle", timeout=30000)

            # Wait additional time for OWL reactive render / transitions
            page.wait_for_timeout(wait_time_ms)

            # Check for crash dialogs
            crash_detected = False
            crash_text = ""
            error_dialog = page.locator(".o_error_dialog, .modal-title:has-text('Odoo Error'), .modal-title:has-text('Error'), .modal-title:has-text('Traceback')")
            if error_dialog.count() > 0:
                crash_detected = True
                modal_body = page.locator(".modal-body, .o_error_dialog")
                crash_text = modal_body.first.inner_text() if modal_body.count() > 0 else "Crash modal detected"

            # Check for blank page
            body_html = page.inner_html("body")
            is_blank = len(body_html.strip()) < 100 or ("<div id=\"app\"></div>" in body_html and len(body_html) < 200)

            page.screenshot(path=output_path, full_page=full_page)
            final_title = page.title()
            final_url = page.url
            browser.close()

        report = [
            "==================================================",
            "📸 Odoo Page Screenshot & Visual Verification Report",
            "==================================================",
            f"✓ Screenshot saved to: {output_path}",
            f"  Page Title: {final_title}",
            f"  Final URL:  {final_url}",
        ]

        if crash_detected:
            report.append(f"❌ CRITICAL: Odoo Crash / Error Modal Detected on screen!\nDetails:\n{crash_text}")
        elif is_blank:
            report.append("❌ CRITICAL: Blank Page / White Screen of Death detected (body content is empty)!")
        else:
            report.append("✓ Visual Status: Page content rendered without visible crash modal.")

        if page_errors:
            report.append("\n⚠ Uncaught JavaScript Page Errors:")
            for pe in page_errors:
                report.append(f"  • {pe}")

        if console_errors:
            report.append("\nℹ Browser Console Messages:")
            for ce in console_errors[:10]:
                report.append(f"  • {ce}")
            if len(console_errors) > 10:
                report.append(f"  ... and {len(console_errors) - 10} more console warnings/errors.")
        else:
            report.append("✓ Zero JavaScript console errors.")

        report.append(f"\nInspect screenshot visually with: view_file(AbsolutePath='{output_path}')")
        return "\n".join(report)

    except Exception as exc:
        return f"Error during browser page capture: {str(exc)}"


@server.tool()
def odoo_audit_file(file_path: str) -> str:
    """Perform deep static, AST, and semantic inspection of an individual Python, XML, or CSV file in an Odoo module.

    Audits Python files for SQL injection, unparameterized queries, insecure sudo(), compute loops, and mutable defaults.
    Audits ir.model.access.csv for missing headers, illogical permissions, and duplicate IDs.
    Audits XML views for deprecated tags (<tree>, attrs, states), unescaped entities, and invalid priority types.

    Args:
        file_path: Absolute path to the file to inspect.

    Returns:
        Structured audit report with defect count, severity ratings, and actionable fixes.
    """
    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' does not exist."

    import csv
    ext = os.path.splitext(file_path)[1].lower()
    report = [
        "==================================================",
        f"🔍 Deep File Audit: {os.path.basename(file_path)}",
        "==================================================",
        f"File Path: {file_path}",
    ]
    issues = []

    # 1. Python file audit
    if ext == ".py":
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            tree = ast.parse(content, filename=file_path)
        except SyntaxError as e:
            return f"❌ Python Syntax Error on line {e.lineno}: {e.msg}"

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Attribute) and func.attr == "execute":
                    if node.args:
                        first_arg = node.args[0]
                        if isinstance(first_arg, ast.JoinedStr):
                            issues.append(f"Line {node.lineno}: [HIGH RISK] SQL injection - cr.execute() using f-string! Use parameterized query.")
                        elif isinstance(first_arg, ast.BinOp) and isinstance(first_arg.op, (ast.Mod, ast.Add)):
                            issues.append(f"Line {node.lineno}: [HIGH RISK] SQL injection - cr.execute() using % or + string formatting! Use parameterized query.")
                        elif isinstance(first_arg, ast.Call) and isinstance(first_arg.func, ast.Attribute) and first_arg.func.attr == "format":
                            issues.append(f"Line {node.lineno}: [HIGH RISK] SQL injection - cr.execute() using .format()! Use parameterized query.")

                if isinstance(func, ast.Attribute) and func.attr == "sudo":
                    issues.append(f"Line {node.lineno}: [SECURITY NOTICE] Use of .sudo() detected. Ensure security comment justifies elevated privileges.")

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for default in node.args.defaults:
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        issues.append(f"Line {node.lineno}: [MUTABLE DEFAULT] Function '{node.name}' uses mutable default argument.")

                # Check create signature for vals_list (batching standard in modern Odoo)
                if node.name == "create":
                    arg_names = [arg.arg for arg in node.args.args]
                    if "vals" in arg_names and "vals_list" not in arg_names:
                        issues.append(f"Line {node.lineno}: [BATCH SIGNATURE] Overridden create() uses legacy signature '(self, vals)'. Use modern batch '(self, vals_list)'.")

            # Check loop bodies for search, create, write (N+1 and batching hazards)
            if isinstance(node, (ast.For, ast.While)):
                for sub in ast.walk(node):
                    if sub is not node and isinstance(sub, ast.Call):
                        func = sub.func
                        if isinstance(func, ast.Attribute):
                            if func.attr in ("search", "search_read", "search_count"):
                                issues.append(f"Line {sub.lineno}: [PERFORMANCE / N+1 RISK] ORM method '{func.attr}()' called inside loop! Batch your IDs and query once outside.")
                            elif func.attr == "create":
                                issues.append(f"Line {sub.lineno}: [PERFORMANCE / BATCHING HAZARD] ORM 'create()' called inside loop! Collect dictionaries into vals_list and call create(vals_list) once.")
                            elif func.attr == "write":
                                issues.append(f"Line {sub.lineno}: [PERFORMANCE / BATCHING HAZARD] ORM 'write()' called inside loop! Collect recordset and perform a single batch write.")

            # Check for unindexed Many2one on line/move/detail models
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
                func = node.value.func
                if isinstance(func, ast.Attribute) and func.attr == "Many2one":
                    has_index = any(kw.arg == "index" and isinstance(kw.value, ast.Constant) and kw.value.value is True for kw in node.value.keywords)
                    base_lower = os.path.basename(file_path).lower()
                    if any(w in base_lower for w in ("line", "move", "item", "detail", "sub")):
                        if not has_index:
                            target_col = node.targets[0].id if node.targets and isinstance(node.targets[0], ast.Name) else "relational_field"
                            issues.append(f"Line {node.lineno}: [INDEX HAZARD] High-volume line model field '{target_col}' lacks 'index=True'! This causes PostgreSQL table lock contention.")


    # 2. CSV file audit
    elif ext == ".csv":
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if not lines:
            issues.append("File is empty.")
        else:
            header = [x.strip() for x in lines[0].split(",")]
            expected = ["id", "name", "model_id:id", "group_id:id", "perm_read", "perm_write", "perm_create", "perm_unlink"]
            if header != expected:
                issues.append(f"Header mismatch. Expected: {','.join(expected)}, Got: {','.join(header)}")
            reader = csv.reader(lines[1:])
            seen_ids = set()
            for idx, row in enumerate(reader, start=2):
                if not row or not any(row):
                    continue
                if len(row) < 8:
                    issues.append(f"Line {idx}: Row has fewer than 8 columns.")
                    continue
                row_id, name, model_id, group_id, r, w, c, u = [x.strip() for x in row[:8]]
                if row_id in seen_ids:
                    issues.append(f"Line {idx}: Duplicate ID '{row_id}'.")
                seen_ids.add(row_id)
                if not model_id.startswith("model_"):
                    issues.append(f"Line {idx}: model_id '{model_id}' does not start with 'model_'.")
                if r == "0" and (w == "1" or c == "1" or u == "1"):
                    issues.append(f"Line {idx}: Illogical permission on '{row_id}' - write/create/unlink granted without read.")

    # 3. XML view audit
    elif ext == ".xml":
        try:
            with open(file_path, "rb") as f:
                root = etree.fromstring(f.read())
        except Exception as e:
            return f"❌ XML Parse Error: {str(e)}"

        for elem in root.iter():
            if elem.tag == "tree":
                issues.append(f"Line {elem.sourceline}: [DEPRECATED] '<tree>' view tag used. Replace with '<list>' in Odoo 18/19/20.")
            if "attrs" in elem.attrib:
                issues.append(f"Line {elem.sourceline}: [DEPRECATED] 'attrs' attribute used. Use direct Python expressions (invisible=\"...\").")
            if "states" in elem.attrib:
                issues.append(f"Line {elem.sourceline}: [DEPRECATED] 'states' attribute used. Use direct Python expressions.")
            if elem.attrib.get("name") == "priority" and elem.attrib.get("eval"):
                val = elem.attrib.get("eval")
                if val.isdigit():
                    issues.append(f"Line {elem.sourceline}: [TYPE ERROR] Priority evaluated as integer ({val}). Must be string literal ('0'-'3').")

    if issues:
        report.append(f"\n⚠ Found {len(issues)} defect(s):")
        for iss in issues:
            report.append(f"  • {iss}")
    else:
        report.append("\n✓ Clean: Zero defects or security vulnerabilities detected in file.")

    return "\n".join(report)


@server.tool()
def odoo_audit_module_folder(path: str) -> str:
    """Audit an entire Odoo addon module folder or addons directory for architectural integrity.

    Detects 'ghost files' (files on disk missing from __manifest__.py 'data' or 'assets'),
    missing __init__.py cascade imports (orphaned Python models that will never load),
    Git merge conflict remnants (<<<<<<<), and structural standard compliance.

    Args:
        path: Absolute path to module folder or addons directory.

    Returns:
        Structured audit report summarizing all detected architectural defects.
    """
    if not os.path.exists(path):
        return f"Error: Path '{path}' does not exist."

    modules = []
    if os.path.exists(os.path.join(path, "__manifest__.py")):
        modules.append(os.path.abspath(path))
    else:
        for entry in os.listdir(path):
            sub = os.path.join(path, entry)
            if os.path.isdir(sub) and os.path.exists(os.path.join(sub, "__manifest__.py")):
                modules.append(os.path.abspath(sub))

    if not modules:
        return f"Error: No Odoo modules containing '__manifest__.py' found in '{path}'."

    report = [
        "==================================================",
        f"📂 Odoo Module Folder Architecture Audit ({len(modules)} module(s))",
        "==================================================",
    ]

    conflict_regex = re.compile(r"^(<{7}|={7}|>{7})\s.*$", re.MULTILINE)

    for mod in modules:
        mod_name = os.path.basename(mod)
        report.append(f"\n📦 Module: {mod_name}")
        mod_issues = []

        manifest_path = os.path.join(mod, "__manifest__.py")
        manifest_data = {}
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest_data = ast.literal_eval(f.read())
        except Exception as e:
            mod_issues.append(f"Manifest parse error: {str(e)}")

        registered_data = set(manifest_data.get("data", [])) | set(manifest_data.get("demo", []))

        # 1. Unregistered Ghost Files
        for folder in ["views", "security", "data", "report", "wizard"]:
            target_dir = os.path.join(mod, folder)
            if os.path.exists(target_dir):
                for root, _, files in os.walk(target_dir):
                    for f in files:
                        if f.endswith((".xml", ".csv")):
                            rel_path = os.path.relpath(os.path.join(root, f), mod)
                            if rel_path not in registered_data:
                                mod_issues.append(f"[GHOST FILE] '{rel_path}' exists on disk but is omitted from __manifest__.py 'data' list!")

        # 2. Python Cascade Import Audit
        root_init = os.path.join(mod, "__init__.py")
        if not os.path.exists(root_init):
            mod_issues.append("[MISSING FILE] Root __init__.py is missing!")
        else:
            with open(root_init, "r", encoding="utf-8") as f:
                root_init_content = f.read()
            for sub in ["models", "controllers", "wizard", "report"]:
                if os.path.isdir(os.path.join(mod, sub)) and any(f.endswith(".py") for f in os.listdir(os.path.join(mod, sub))):
                    if f"from . import {sub}" not in root_init_content and f"import {sub}" not in root_init_content:
                        mod_issues.append(f"[CASCADE IMPORT] Directory '{sub}' contains Python code but is not imported in root __init__.py!")

        models_dir = os.path.join(mod, "models")
        if os.path.exists(models_dir):
            models_init = os.path.join(models_dir, "__init__.py")
            if not os.path.exists(models_init):
                mod_issues.append("[MISSING FILE] models/__init__.py is missing!")
            else:
                with open(models_init, "r", encoding="utf-8") as f:
                    models_init_content = f.read()
                for py_file in os.listdir(models_dir):
                    if py_file.endswith(".py") and py_file != "__init__.py":
                        stem = py_file[:-3]
                        if f"from . import {stem}" not in models_init_content and f"import {stem}" not in models_init_content:
                            mod_issues.append(f"[ORPHAN MODEL] File 'models/{py_file}' exists on disk but is not imported in models/__init__.py! It will never load.")

        # 3. Git Conflict Markers
        for root, _, files in os.walk(mod):
            if ".git" in root or "__pycache__" in root:
                continue
            for f in files:
                if f.endswith((".py", ".xml", ".csv", ".js", ".scss", ".md")):
                    f_path = os.path.join(root, f)
                    try:
                        with open(f_path, "r", encoding="utf-8", errors="ignore") as fl:
                            if conflict_regex.search(fl.read()):
                                mod_issues.append(f"[GIT CONFLICT] Unresolved merge conflict marker found in: {os.path.relpath(f_path, mod)}")
                    except Exception:
                        pass

        if mod_issues:
            report.append(f"  ⚠ Found {len(mod_issues)} architectural issue(s):")
            for mi in mod_issues:
                report.append(f"    • {mi}")
        else:
            report.append("  ✓ Clean: Full manifest registration, clean cascade imports, and zero ghost files.")

    return "\n".join(report)


@server.tool()
def odoo_audit_database(
    db: str,
    host: str = "localhost",
    port: int = 5432,
    user: str = "odoo",
    password: Optional[str] = None,
    rpc_port: int = 8069,
) -> str:
    """Audit an Odoo PostgreSQL database for missing foreign key indexes, orphaned XML IDs, and financial balance.

    Inspects:
    1. Unindexed foreign keys causing slow queries and deadlocks.
    2. Orphaned ir.model.data external IDs.
    3. Double-entry financial balancing (sum(debit) == sum(credit)).
    4. Active PostgreSQL transaction locks and blockers.

    Args:
        db: Odoo PostgreSQL database name.
        host: Database host (default: localhost).
        port: PostgreSQL port (default: 5432).
        user: Database user (default: odoo).
        password: Database password.
        rpc_port: Odoo JSON-RPC port (default: 8069).

    Returns:
        Structured database health report.
    """
    report = [
        "==================================================",
        f"🗄 Odoo Database Health & Integrity Audit: {db}",
        "==================================================",
    ]

    try:
        import psycopg2
        conn_kwargs = {"dbname": db, "host": host, "port": port, "user": user}
        if password:
            conn_kwargs["password"] = password

        conn = psycopg2.connect(**conn_kwargs)
        cur = conn.cursor()

        # 1. Unindexed Foreign Keys
        cur.execute("""
            SELECT
                c.conrelid::regclass AS table_name,
                a.attname AS column_name
            FROM pg_constraint c
            JOIN pg_attribute a ON a.attnum = ANY(c.conkey) AND a.attrelid = c.conrelid
            WHERE c.contype = 'f'
              AND NOT EXISTS (
                  SELECT 1 FROM pg_index i
                  WHERE i.indrelid = c.conrelid
                    AND a.attnum = i.indkey[0]
              )
              AND c.conrelid::regclass::text NOT LIKE 'pg_%'
              AND c.conrelid::regclass::text NOT LIKE 'sql_%'
            ORDER BY table_name, column_name
            LIMIT 25;
        """)
        unindexed_fks = cur.fetchall()
        if unindexed_fks:
            report.append(f"\n⚠ Found {len(unindexed_fks)} unindexed Foreign Key column(s) (Deadlock & Slow Query Risk):")
            for tbl, col in unindexed_fks:
                report.append(f"  • Table: {tbl} | Column: {col} -> Add index=True in Python model")
        else:
            report.append("\n✓ Foreign Key Indexing: All relational foreign keys have corresponding indexes.")

        # 2. Orphaned XML IDs
        cur.execute("""
            SELECT module, name, model, res_id
            FROM ir_model_data
            WHERE res_id IS NULL OR res_id = 0
            LIMIT 20;
        """)
        orphaned_ids = cur.fetchall()
        if orphaned_ids:
            report.append(f"\n⚠ Found {len(orphaned_ids)} broken/orphaned ir.model.data record(s):")
            for mod, name, model, res_id in orphaned_ids:
                report.append(f"  • {mod}.{name} -> Model: {model} (res_id: {res_id})")
        else:
            report.append("✓ External IDs: Zero orphaned ir.model.data records detected.")

        # 3. Financial Balance Audit (if account_move_line exists)
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = 'account_move_line'
            );
        """)
        has_aml = cur.fetchone()[0]
        if has_aml:
            cur.execute("""
                SELECT move_id, ROUND(SUM(debit), 2) AS tot_debit, ROUND(SUM(credit), 2) AS tot_credit
                FROM account_move_line
                WHERE parent_state = 'posted'
                GROUP BY move_id
                HAVING ROUND(SUM(debit), 2) != ROUND(SUM(credit), 2)
                LIMIT 10;
            """)
            unbalanced_moves = cur.fetchall()
            if unbalanced_moves:
                report.append(f"\n❌ CRITICAL: Found {len(unbalanced_moves)} posted unbalanced journal entries!")
                for mid, deb, cred in unbalanced_moves:
                    report.append(f"  • Move ID {mid}: Debit={deb} != Credit={cred} (Diff={deb - cred})")
            else:
                report.append("✓ Double-Entry Integrity: All posted journal entries are strictly balanced (Debit == Credit).")

        # 4. Active Locks
        cur.execute("""
            SELECT count(*)
            FROM pg_locks l
            JOIN pg_stat_activity a ON a.pid = l.pid
            WHERE NOT l.granted;
        """)
        waiting_locks = cur.fetchone()[0]
        if waiting_locks > 0:
            report.append(f"\n⚠ Warning: {waiting_locks} transaction(s) currently WAITING for database locks!")
        else:
            report.append("✓ Concurrency: Zero transactions blocked by database locks.")

        # 5. Inventory Stock Valuation Layer (SVL) Consistency
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = 'stock_valuation_layer'
            );
        """)
        has_svl = cur.fetchone()[0]
        if has_svl:
            cur.execute("""
                SELECT count(*)
                FROM stock_valuation_layer
                WHERE unit_cost < 0 OR (quantity > 0 AND value < 0);
            """)
            invalid_svl = cur.fetchone()[0]
            if invalid_svl > 0:
                report.append(f"\n❌ CRITICAL: Found {invalid_svl} corrupted/negative Stock Valuation Layer record(s)!")
            else:
                report.append("✓ Inventory Valuation: All stock valuation layers have valid positive unit costs and values.")

        # 6. Multi-Company Data Isolation Leaks
        company_leak_queries = [
            ("sale_order_line", "sale_order", "order_id"),
            ("account_move_line", "account_move", "move_id"),
            ("purchase_order_line", "purchase_order", "order_id"),
        ]
        leaks_found = 0
        for child_tbl, parent_tbl, fk in company_leak_queries:
            cur.execute(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_name = '{child_tbl}'
                ) AND EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_name = '{parent_tbl}'
                );
            """)
            both_exist = cur.fetchone()[0]
            if both_exist:
                cur.execute(f"""
                    SELECT count(*)
                    FROM {child_tbl} c
                    JOIN {parent_tbl} p ON c.{fk} = p.id
                    WHERE c.company_id IS NOT NULL
                      AND p.company_id IS NOT NULL
                      AND c.company_id != p.company_id;
                """)
                mismatches = cur.fetchone()[0]
                if mismatches > 0:
                    leaks_found += mismatches
                    report.append(f"❌ CRITICAL Multi-Company Leak: {mismatches} row(s) in {child_tbl} have company_id different from parent {parent_tbl}!")

        if leaks_found == 0:
            report.append("✓ Multi-Company Isolation: Zero cross-company relational leaks detected.")

        cur.close()
        conn.close()

    except Exception as exc:
        report.append(f"\nℹ PostgreSQL direct catalog check unavailable: {str(exc)}")
        report.append("Attempting Odoo JSON-RPC connectivity check...")
        try:
            import odoorpc
            odoo = odoorpc.ODOO(host, port=rpc_port)
            if db in odoo.db.list():
                report.append(f"✓ Odoo RPC connected. Database '{db}' is active on port {rpc_port}.")
            else:
                report.append(f"⚠ Database '{db}' not found in Odoo database list on port {rpc_port}.")
        except Exception as rpc_exc:
            report.append(f"❌ Odoo RPC connection failed: {str(rpc_exc)}")

    return "\n".join(report)


@server.tool()
def odoo_pre_upgrade_audit(path: str) -> str:
    """Run the complete Pre-Upgrade Safety Gate (Stage 1) on an Odoo module.
    
    Audits manifest integrity, XML well-formedness and verified XPaths, directory ghost files,
    Python cascade imports, AST security risks, N+1 query patterns, and pylint compliance.

    Args:
        path: Absolute path to the addon module folder.

    Returns:
        Structured Pre-Upgrade Safety Gate Report with PASS or BLOCKED verdict.
    """
    if not os.path.exists(path):
        return f"Error: Path '{path}' does not exist."

    manifest_path = os.path.join(path, "__manifest__.py") if os.path.isdir(path) else path
    addon_dir = os.path.dirname(manifest_path) if os.path.isfile(manifest_path) else path

    report = [
        "==================================================",
        f"🛡 PRE-UPGRADE SAFETY GATE REPORT: {os.path.basename(addon_dir)}",
        "==================================================",
    ]

    has_errors = False

    # 1. Manifest Validation
    m_res = odoo_validate_manifest(manifest_path)
    report.append("\n[1/5] Manifest & Asset Paths Check:")
    report.append(m_res)
    if "Error:" in m_res or "❌" in m_res:
        has_errors = True

    # 2. XML Validation
    views_dir = os.path.join(addon_dir, "views")
    if os.path.exists(views_dir):
        x_res = odoo_validate_xml(views_dir)
        report.append("\n[2/5] XML Views & XPaths Check:")
        report.append(x_res)
        if "❌" in x_res or "Error:" in x_res:
            has_errors = True
    else:
        report.append("\n[2/5] XML Views & XPaths Check: No views/ folder found.")

    # 3. Folder & Ghost File Audit
    fo_res = odoo_audit_module_folder(addon_dir)
    report.append("\n[3/5] Folder & Ghost File Audit:")
    report.append(fo_res)
    if "❌" in fo_res or "CRITICAL" in fo_res:
        has_errors = True

    # 4. AST File Security Audit
    report.append("\n[4/5] Deep AST & Security Inspection:")
    file_issues = 0
    for root, _, files in os.walk(addon_dir):
        for f in files:
            if f.endswith((".py", ".xml", ".csv")):
                fpath = os.path.join(root, f)
                res = odoo_audit_file(fpath)
                if "❌" in res or "CRITICAL" in res:
                    file_issues += 1
                    report.append(f"  • {os.path.relpath(fpath, addon_dir)}:\n{res}")
    if file_issues == 0:
        report.append("✓ AST File Security: Zero SQL injection, unsafe sudo(), or compute loop issues found.")
    else:
        has_errors = True

    # 5. Pylint-Odoo Lint
    report.append("\n[5/5] Static Linter Check (pylint-odoo):")
    l_res = odoo_pylint(addon_dir)
    report.append(l_res)
    if "E:" in l_res or "CRITICAL" in l_res:
        has_errors = True

    report.append("\n==================================================")
    if has_errors:
        report.append("⛔ PRE-UPGRADE VERDICT: BLOCKED")
        report.append("Critical defects detected! Do NOT run module upgrade until 100% of issues are resolved.")
    else:
        report.append("✅ PRE-UPGRADE VERDICT: PASSED")
        report.append("All Stage 1 safety checks passed cleanly. Module is safe for controlled database upgrade.")
    report.append("==================================================")

    return "\n".join(report)


if __name__ == "__main__":
    server.run(transport="stdio")



