---
name: odoo-visual-inspector
description: "Principal-grade Server Visual Screenshot & UI Health Inspector for Odoo 19 & 20. Executes automated page captures via Playwright/DevTools, detects Blank Pages (White Screen of Death), uncaught JavaScript errors, Odoo crash modals (.o_error_dialog), and verifies UI alignment and responsive layouts."
---

# Odoo Visual Screenshot & UI Health Inspector (Principal Standard)

> **MANDATORY LAW (Stage 4 of Pre-Upgrade Safety Gate)**:
> Never declare an implementation, view change, or bugfix complete without physically capturing and visually inspecting screenshots of every modified page on the running server, monitoring browser console errors, and verifying UI health.

---

## 1. The Visual Inspection Protocol

Static syntax checks and `--stop-after-init` upgrades verify only that Python compiles and XML parses into the database. They **DO NOT** verify:
1. Whether OWL component templates compile in the browser virtual DOM.
2. Whether missing `@web/...` imports cause an asset bundle crash resulting in a **White Screen of Death (Blank Page)**.
3. Whether button actions, statusbars, or widgets render with fatal traceback modals (`.o_error_dialog`).
4. Whether responsive layouts, toolbars, z-indices, or tables are visually overlapping or truncated.

---

## 2. Automated Page Capture Pipeline

Execute page captures using the integrated MCP tool `odoo_capture_page` or CLI `odoo-dev screenshot`:

```bash
# Capture a view or action URL
odoo-dev screenshot --url http://localhost:8069 --login admin --password admin --db mydb --action-url "/odoo/action-123" --output /path/to/screenshot.png
```

### What Automated Capture Does:
1. Launches headless Chromium via Playwright.
2. Navigates to the Odoo instance and authenticates session cookies.
3. Navigates to the targeted action, form, list, or kanban view.
4. Waits for OWL virtual DOM reconciliation (`networkidle` + configurable settling time).
5. Monitors the browser `console` event stream for uncaught JavaScript exceptions, unhandled Promise rejections, and 404 asset failures.
6. Queries the DOM for modal crash containers: `.o_error_dialog`, `.modal.o_technical_modal`, `.alert-danger`.
7. Saves a full-page high-resolution PNG screenshot to `~/.gemini/antigravity/screenshots/`.
8. Returns a detailed health report with the file URI.

---

## 3. Mandatory Inspection Checklist (Using `view_file`)

After capturing each screenshot, physically inspect it using `view_file(AbsolutePath=...)`. Check all 6 visual vectors:

| Inspection Vector | What to Look For | Critical Failure Symptom |
| :--- | :--- | :--- |
| **1. White Screen / Blank Page** | Full UI layout rendered: navbar loaded, systray visible, breadcrumb bar populated, action manager populated. | Completely blank white viewport, missing navbar, frozen loading spinner. |
| **2. Traceback Modals** | Zero error modals or overlay backdrops visible. | Red alert banner, `.o_error_dialog`, "Odoo Server Error", traceback stack. |
| **3. Statusbar & Lifecycle** | Active state highlighted with correct color; transition buttons clearly visible in header. | Missing statusbar arrows, overlapping buttons, inactive state styles. |
| **4. Alignment & Cards** | Form sheet (`<sheet>`) centered; Bootstrap cards neatly spaced; fields aligned in two columns; no text truncation. | Overflowing text, distorted input boxes, overlapping tables, unpadded cards. |
| **5. Chatter Widget** | Modern `<chatter/>` widget renders below sheet with "Send message", "Log note", and "Activities" buttons. | Missing chatter, legacy `.oe_chatter` unstyled block, broken follower avatars. |
| **6. Console Error Stream** | Zero fatal JS errors in the capture report output. | `TypeError: Cannot read properties of undefined`, missing `@web/core` export. |

---

## 4. Closed-Loop Visual Remediation

If ANY visual glitch, layout overlap, console error, or crash modal is identified:
1. **Trace Root Cause**:
   - Blank Page -> Check `__manifest__.py` `'assets'` paths and JS import paths (`@web/...`, `@module/...`).
   - Crash Modal -> Check Python backend method signature or missing relational field in XML view.
   - Layout Overlap -> Check XML `<group>` / `<page>` nesting, Bootstrap classes, or CSS z-index.
2. **Fix in Code**: Correct the responsible XML view, CSS/SCSS, Python model, or JS/OWL file.
3. **Re-Run Safety Gate & Upgrade**:
   `odoo-dev pre-upgrade <module_path>`
   `python3 odoo-bin -u <module> -d <db> --stop-after-init`
4. **Re-Capture Screenshot**: Run `odoo-dev screenshot` again.
5. **Re-Inspect**: Confirm 100% pixel-perfect rendering with `view_file`.
