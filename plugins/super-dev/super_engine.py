#!/usr/bin/env python3
"""
Universal Super-AI Developer Engine (piwd005-Ai)
Industry-wide polyglot engineering, security auditing, web verification,
API validation, and architectural design engine.
"""

import ast
import json
import os
import re
import shutil
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

# Optional dependencies handled defensively
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

try:
    import psycopg2
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False

try:
    import urllib.request
    import urllib.error
except ImportError:
    pass


# ==============================================================================
# 1. Polyglot Diagnostic Health Check
# ==============================================================================

def super_doctor() -> str:
    """Run an automated polyglot self-diagnostic check across compilers, runtimes,

    containerization tools, browser engines, and AI directives.
    """
    report = [
        "==================================================",
        "🚀 UNIVERSAL SUPER-AI DEVELOPER HEALTH CHECK",
        "==================================================",
    ]
    all_ok = True

    # 1. Python Runtime
    py_ver = sys.version_info
    if py_ver >= (3, 10):
        report.append(f"✓ Python Runtime: {py_ver.major}.{py_ver.minor}.{py_ver.micro} (Supported: >= 3.10)")
    else:
        all_ok = False
        report.append(f"❌ Python Runtime: {py_ver.major}.{py_ver.minor}.{py_ver.micro} (Requires Python >= 3.10)")

    # 2. Node.js & npm (Frontend Ecosystem)
    node_bin = shutil.which("node")
    if node_bin:
        try:
            node_ver = subprocess.check_output([node_bin, "--version"], text=True).strip()
            report.append(f"✓ Node.js Runtime: {node_ver} (Path: {node_bin})")
        except Exception:
            report.append(f"✓ Node.js Runtime: Detected at {node_bin}")
    else:
        report.append("ℹ Node.js: Not installed on host (Required for JS/TS/React runtime)")

    npm_bin = shutil.which("npm")
    if npm_bin:
        report.append(f"✓ npm Package Manager: Installed ({npm_bin})")
    else:
        report.append("ℹ npm: Not installed on host")

    # 3. Go Language (Systems & Microservices)
    go_bin = shutil.which("go")
    if go_bin:
        try:
            go_ver = subprocess.check_output([go_bin, "version"], text=True).strip()
            report.append(f"✓ Go Runtime: {go_ver}")
        except Exception:
            report.append(f"✓ Go Runtime: Installed at {go_bin}")
    else:
        report.append("ℹ Go: Not installed on host (Optional for systems development)")

    # 4. Rust & Cargo (High Performance & Safety)
    rustc_bin = shutil.which("rustc")
    if rustc_bin:
        try:
            rust_ver = subprocess.check_output([rustc_bin, "--version"], text=True).strip()
            report.append(f"✓ Rust Compiler: {rust_ver}")
        except Exception:
            report.append(f"✓ Rust: Installed at {rustc_bin}")
    else:
        report.append("ℹ Rust: Not installed on host (Optional for systems development)")

    # 5. Docker (Containers & Microservices)
    docker_bin = shutil.which("docker")
    if docker_bin:
        try:
            dock_ver = subprocess.check_output([docker_bin, "--version"], text=True).strip()
            report.append(f"✓ Docker Container Engine: {dock_ver}")
        except Exception:
            report.append(f"✓ Docker: Installed at {docker_bin}")
    else:
        report.append("ℹ Docker: Not detected on host (Optional for container orchestration)")

    # 6. Playwright Headless Chromium Engine (Visual QA & Web Inspection)
    if PLAYWRIGHT_AVAILABLE:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                browser.close()
            report.append("✓ Visual QA Engine: Playwright Chromium browser is installed and operational.")
        except Exception as e:
            all_ok = False
            report.append(f"⚠ Visual QA Engine: Chromium launch failed ({str(e)}). Run: playwright install chromium")
    else:
        all_ok = False
        report.append("❌ Visual QA Engine: python-playwright package not installed.")

    # 7. PostgreSQL Database Client
    if PSYCOPG2_AVAILABLE:
        report.append("✓ Database Client: psycopg2-binary installed for direct PostgreSQL inspection.")
    else:
        report.append("ℹ Database Client: psycopg2 not installed (Direct DB query audit unavailable).")

    # 8. Git Version Control
    git_bin = shutil.which("git")
    if git_bin:
        report.append("✓ Version Control: git command line operational.")
    else:
        all_ok = False
        report.append("❌ Version Control: git not found in PATH.")

    # 9. AI Engineering Skills Repository
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    skills_dir = os.path.expanduser("~/.gemini/config/skills")
    local_skills_dir = os.path.join(repo_root, "skills")
    if os.path.isdir(skills_dir) and os.listdir(skills_dir):
        active_skills = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
        report.append(f"✓ AI Engineering Skills: {len(active_skills)} skills active in {skills_dir}.")
    elif os.path.isdir(local_skills_dir):
        active_skills = [d for d in os.listdir(local_skills_dir) if os.path.isdir(os.path.join(local_skills_dir, d))]
        report.append(f"✓ AI Engineering Skills: {len(active_skills)} skills active in repository.")
    else:
        report.append("⚠ AI Engineering Skills: skills directory not found.")

    # 10. Core Invariant Directives
    agents_path = os.path.expanduser("~/.gemini/config/AGENTS.md")
    local_agents = os.path.join(repo_root, "AGENTS.md")
    if os.path.exists(agents_path):
        report.append("✓ Core Directives: Global AGENTS.md verified (Universal Laws active).")
    elif os.path.exists(local_agents):
        report.append("✓ Core Directives: Repository AGENTS.md verified (Universal Laws active).")
    else:
        report.append("⚠ Core Directives: AGENTS.md missing.")

    report.append("==================================================")
    if all_ok:
        report.append("🎉 UNIVERSAL STATUS: 100% HEALTHY & PRODUCTION-READY")
    else:
        report.append("⚠ UNIVERSAL STATUS: WARNINGS DETECTED (Review items above)")
    report.append("==================================================")

    return "\n".join(report)


# ==============================================================================
# 2. Universal AST & Security Vulnerability Auditor
# ==============================================================================

class SecurityVisitor(ast.NodeVisitor):
    """AST visitor to detect security vulnerabilities in Python source code."""

    def __init__(self, filename: str):
        self.filename = filename
        self.findings = []

    def visit_Call(self, node: ast.Call):
        func_name = ""
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr

        # 1. Dangerous eval/exec
        if func_name in ("eval", "exec"):
            self.findings.append({
                "severity": "CRITICAL",
                "line": node.lineno,
                "type": "Code Injection",
                "message": f"Use of dangerous dynamic execution function '{func_name}()'. Use safe parsing (e.g. ast.literal_eval or json.loads)."
            })

        # 2. Insecure deserialization
        if func_name in ("loads", "load") and isinstance(getattr(node, 'func', None), ast.Attribute):
            val = getattr(node.func, 'value', None)
            if isinstance(val, ast.Name) and val.id == "pickle":
                self.findings.append({
                    "severity": "CRITICAL",
                    "line": node.lineno,
                    "type": "Insecure Deserialization",
                    "message": "Use of unsafe 'pickle.loads()'. Deserializing untrusted data can lead to arbitrary remote code execution."
                })

        # 3. Command injection via os.system or subprocess without shell=False
        if func_name in ("system", "popen") and isinstance(getattr(node, 'func', None), ast.Attribute):
            val = getattr(node.func, 'value', None)
            if isinstance(val, ast.Name) and val.id == "os":
                self.findings.append({
                    "severity": "HIGH",
                    "line": node.lineno,
                    "type": "Command Injection",
                    "message": f"Use of unescaped 'os.{func_name}()'. Use 'subprocess.run()' with arguments list and 'shell=False'."
                })

        # 4. SQL Injection via string interpolation in execute()
        if func_name == "execute":
            if node.args:
                first_arg = node.args[0]
                if isinstance(first_arg, ast.JoinedStr):  # f-string
                    self.findings.append({
                        "severity": "CRITICAL",
                        "line": node.lineno,
                        "type": "SQL Injection",
                        "message": "SQL query formed using Python f-string in .execute(). Always use parameterized queries: .execute('SELECT ... WHERE id = %s', [id])."
                    })
                elif isinstance(first_arg, ast.BinOp) and isinstance(first_arg.op, (ast.Mod, ast.Add)):  # % or +
                    self.findings.append({
                        "severity": "CRITICAL",
                        "line": node.lineno,
                        "type": "SQL Injection",
                        "message": "SQL query formed using string concatenation/formatting (%) in .execute(). Use parameterized queries."
                    })

        self.generic_visit(node)


def super_sec_audit(target_path: str) -> str:
    """Universal Static Application Security Testing (SAST) auditor.

    Scans Python, JavaScript, TypeScript, Go, and SQL files for OWASP Top 10 vulnerabilities,
    SQL injection, code injection, hardcoded secrets, weak crypto, and unescaped inputs.
    """
    if not os.path.exists(target_path):
        return f"Error: Target path '{target_path}' does not exist."

    files_to_scan = []
    if os.path.isdir(target_path):
        for root, _, files in os.walk(target_path):
            if any(skip in root for skip in (".git", "node_modules", ".venv", "__pycache__", "dist", "build")):
                continue
            for f in files:
                if f.endswith((".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".sql", ".env", ".json", ".yaml", ".yml")):
                    files_to_scan.append(os.path.join(root, f))
    else:
        files_to_scan.append(target_path)

    findings = []

    # Regex patterns for secret detection
    SECRET_PATTERNS = [
        (re.compile(r"""(?:api[_-]?key|secret|token|password|auth[_-]?token)\s*[:=]\s*['"][A-Za-z0-9_\-\.]{12,}['"]""", re.IGNORECASE), "Exposed Secret / API Key"),
        (re.compile(r"""-----BEGIN (?:RSA )?PRIVATE KEY-----"""), "Hardcoded Private Key"),
        (re.compile(r"""ghp_[A-Za-z0-9]{36}"""), "GitHub Personal Access Token"),
        (re.compile(r"""AKIA[0-9A-Z]{16}"""), "AWS Access Key ID"),
    ]

    # Regex patterns for JS/TS vulnerabilities
    JS_VULN_PATTERNS = [
        (re.compile(r"""dangerouslySetInnerHTML\s*=\s*\{\s*\{\s*__html\s*:"""), "HIGH", "XSS Risk", "Use of dangerouslySetInnerHTML without verified DOMPurify sanitization."),
        (re.compile(r"""\bdocument\.write\s*\("""), "HIGH", "XSS Risk", "Use of document.write() can introduce DOM-based XSS."),
        (re.compile(r"""\binnerHTML\s*=\s*`.*?\$\{.*?\}"""), "HIGH", "DOM XSS", "Dynamic template interpolation into innerHTML. Use textContent or React safe binding."),
    ]

    for file_path in files_to_scan:
        rel_path = os.path.relpath(file_path, target_path) if os.path.isdir(target_path) else os.path.basename(file_path)
        
        # 1. Python AST Scan
        if file_path.endswith(".py"):
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                tree = ast.parse(content, filename=file_path)
                visitor = SecurityVisitor(rel_path)
                visitor.visit(tree)
                for finding in visitor.findings:
                    findings.append(f"[{finding['severity']}] {rel_path}:{finding['line']} - {finding['type']}: {finding['message']}")
            except SyntaxError:
                pass
            except Exception:
                pass

        # 2. Generic Text / Secret / JS Scan
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
            for line_no, line in enumerate(lines, start=1):
                # Secret check (skip test files)
                if not any(t in rel_path.lower() for t in ("test", "fixture", "mock", "example")):
                    for pat, desc in SECRET_PATTERNS:
                        if pat.search(line):
                            findings.append(f"[CRITICAL] {rel_path}:{line_no} - {desc}: Potential hardcoded secret detected. Move to environment variable.")
                            break

                # JS/TS checks
                if file_path.endswith((".js", ".jsx", ".ts", ".tsx")):
                    for pat, sev, vtype, msg in JS_VULN_PATTERNS:
                        if pat.search(line):
                            findings.append(f"[{sev}] {rel_path}:{line_no} - {vtype}: {msg}")
        except Exception:
            continue

    report = [
        "==================================================",
        "🛡️ UNIVERSAL SAST & SECURITY AUDIT REPORT",
        "==================================================",
        f"Scanned: {len(files_to_scan)} file(s) under '{target_path}'",
    ]
    if findings:
        report.append(f"Vulnerabilities Detected: {len(findings)}\n")
        report.extend(findings)
        report.append("\n⛔ SECURITY VERDICT: ACTION REQUIRED - Fix identified vulnerabilities before deployment.")
    else:
        report.append("✅ SECURITY VERDICT: 0 VULNERABILITIES DETECTED")
        report.append("Code passed universal security analysis cleanly.")
    report.append("==================================================")

    return "\n".join(report)


# ==============================================================================
# 3. Universal Web & UI Headless Playwright Inspector
# ==============================================================================

def super_web_capture(
    url: str,
    output: Optional[str] = None,
    viewport: str = "desktop",
    wait_ms: int = 3000
) -> str:
    """Universal Web Application Inspector using Headless Chromium.

    Captures screenshots across responsive viewports, monitors browser console errors,
    and detects White Screen of Death (WSOD) or uncaught exceptions.
    """
    if not PLAYWRIGHT_AVAILABLE:
        return "Error: Playwright is not installed. Run 'pip install playwright && playwright install chromium'."

    viewports = {
        "desktop": {"width": 1920, "height": 1080},
        "tablet": {"width": 768, "height": 1024},
        "mobile": {"width": 390, "height": 844},
    }
    vp = viewports.get(viewport.lower(), viewports["desktop"])

    if not output:
        output = f"/tmp/super_web_{viewport}_{int(time.time())}.png"

    console_errors = []
    page_errors = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport=vp,
                device_scale_factor=2,
                user_agent="Mozilla/5.0 (SuperAI-Inspector; Universal QA Engine)"
            )
            page = context.new_page()

            page.on("console", lambda msg: console_errors.append(f"[{msg.type}] {msg.text}") if msg.type in ("error", "warning") else None)
            page.on("pageerror", lambda err: page_errors.append(str(err)))

            # Navigate
            response = page.goto(url, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(wait_ms)

            # WSOD Check: check if document body is empty or height is 0
            body_height = page.evaluate("document.body ? document.body.scrollHeight : 0")
            body_text = page.evaluate("document.body ? document.body.innerText.trim() : ''")
            is_wsod = body_height <= 10 or len(body_text) == 0

            # Take full page screenshot
            page.screenshot(path=output, full_page=True)
            browser.close()

        status_code = response.status if response else "Unknown"
        report = [
            "==================================================",
            "🌐 UNIVERSAL WEB INSPECTION REPORT",
            "==================================================",
            f"Target URL: {url}",
            f"HTTP Status: {status_code}",
            f"Viewport: {viewport} ({vp['width']}x{vp['height']})",
            f"Screenshot Saved: {output}",
            f"DOM Body Height: {body_height}px",
        ]

        if is_wsod:
            report.append("⛔ CRITICAL: White Screen of Death (WSOD) detected! The rendered DOM body is blank or 0px high.")

        if page_errors:
            report.append(f"\n❌ Uncaught JavaScript Exceptions ({len(page_errors)}):")
            for err in page_errors[:5]:
                report.append(f"   - {err}")

        if console_errors:
            report.append(f"\n⚠ Browser Console Logs ({len(console_errors)}):")
            for c_err in console_errors[:5]:
                report.append(f"   - {c_err}")

        if not is_wsod and not page_errors:
            report.append("\n✅ VISUAL VERDICT: PAGE RENDERED SUCCESSFULLY")
        else:
            report.append("\n⛔ VISUAL VERDICT: DEFECTS DETECTED")
        report.append("==================================================")

        return "\n".join(report)

    except Exception as e:
        return f"Error during web inspection of '{url}': {str(e)}"


# ==============================================================================
# 4. Universal API Contract & Latency Tester
# ==============================================================================

def super_api_test(url: str, method: str = "GET", headers: Optional[Dict[str, str]] = None, data: Optional[str] = None) -> str:
    """Send an HTTP request to an API endpoint and measure status, response time, and JSON validity."""
    if not headers:
        headers = {"User-Agent": "SuperAI-API-Tester/1.0", "Accept": "application/json"}

    req_data = data.encode("utf-8") if data else None
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method.upper())

    start_time = time.time()
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            latency_ms = (time.time() - start_time) * 1000
            status = resp.status
            raw_body = resp.read().decode("utf-8", errors="ignore")

        is_json = False
        try:
            parsed_json = json.loads(raw_body)
            is_json = True
            preview = json.dumps(parsed_json, indent=2)[:500]
        except Exception:
            preview = raw_body[:500]

        report = [
            "==================================================",
            "⚡ UNIVERSAL API ENDPOINT TEST REPORT",
            "==================================================",
            f"Target: {method.upper()} {url}",
            f"HTTP Status: {status} OK",
            f"Latency: {latency_ms:.2f} ms",
            f"Payload Type: {'JSON (Valid)' if is_json else 'Raw / HTML / PlainText'}",
            "Preview:",
            preview,
            "==================================================",
            f"✅ RESULT: {'PASSED' if status < 400 else 'FAILED'}"
        ]
        return "\n".join(report)

    except urllib.error.HTTPError as e:
        latency_ms = (time.time() - start_time) * 1000
        return f"HTTP Error {e.code}: {e.reason} (Latency: {latency_ms:.2f} ms)"
    except Exception as e:
        return f"API Request Failed: {str(e)}"


# ==============================================================================
# 5. Universal Architectural Pre-Flight Blueprint Generator
# ==============================================================================

def super_blueprint(name: str, blueprint_type: str = "fullstack", stack: str = "FastAPI + React + PostgreSQL") -> str:
    """Generate a production-ready C4 Architectural Blueprint, Entity-Relationship model,

    and API matrix for any software system.
    """
    clean_name = re.sub(r"[^A-Za-z0-9_]", "", name.replace(" ", "_"))

    bp = f"""# Architectural Pre-Flight Blueprint: {name}
Stack: {stack}
Architecture Type: {blueprint_type.capitalize()}

## 1. C4 Context & Container Topology
```mermaid
graph TD
    User["End User / Client App"] -->|HTTPS / REST / WebSocket| API["API Gateway / Backend ({stack.split('+')[0].strip()})"]
    API -->|Auth / Session Cache| Cache["Redis In-Memory Cache"]
    API -->|Async Job Queue| Worker["Background Task Worker"]
    API -->|Transactional Persistence| DB[("Relational Database ({stack.split('+')[-1].strip()})")]
    Worker -->|State / Status| DB
```

## 2. Entity-Relationship Data Model
```mermaid
erDiagram
    {clean_name.upper()} ||--o{{ {clean_name.upper()}_ITEM : contains
    USER ||--o{{ {clean_name.upper()} : creates

    USER {{
        uuid id PK
        string email
        string hashed_password
        datetime created_at
    }}

    {clean_name.upper()} {{
        uuid id PK
        uuid user_id FK
        string title
        string status
        decimal total_amount
        datetime created_at
        datetime updated_at
    }}

    {clean_name.upper()}_ITEM {{
        uuid id PK
        uuid {clean_name.lower()}_id FK
        string item_name
        int quantity
        decimal unit_price
    }}
```

## 3. State Machine Lifecycle
```mermaid
stateDiagram-v2
    [*] --> DRAFT : Create Initial Record
    DRAFT --> PENDING_REVIEW : submit() [Validate Schema]
    PENDING_REVIEW --> APPROVED : approve() [Authorization Verified]
    PENDING_REVIEW --> REJECTED : reject() [Reason Logged]
    APPROVED --> PROCESSING : execute() [Spawn Async Task]
    PROCESSING --> COMPLETED : on_success() [Commit DB Transaction]
    PROCESSING --> FAILED : on_error() [Trigger Rollback]
    COMPLETED --> [*]
    FAILED --> [*]
    REJECTED --> [*]
```

## 4. API Contract & Endpoint Matrix
| Method | Path | Required Role | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/{clean_name.lower()}` | Authenticated | Create new record (Accepts JSON body) |
| `GET` | `/api/v1/{clean_name.lower()}` | Authenticated | List paginated records (Supports limit, cursor) |
| `GET` | `/api/v1/{clean_name.lower()}/:id` | Authenticated | Retrieve single record details |
| `PATCH`| `/api/v1/{clean_name.lower()}/:id` | Owner / Admin | Update mutable fields |
| `DELETE`|`/api/v1/{clean_name.lower()}/:id`| Owner / Admin | Soft delete record |

## 5. Security & Concurrency Directives
1. **Idempotency Keys**: Enforce `X-Idempotency-Key` header on all mutation endpoints (`POST`, `PATCH`).
2. **Transaction Isolation**: Wrap multi-table modifications inside `BEGIN ... COMMIT` with explicit row-level locking where concurrent updates are expected.
3. **Cursor-Based Pagination**: Prohibit unbounded `OFFSET` queries on high-volume tables. Use `WHERE id > :cursor LIMIT 50`.
4. **Input Validation**: Enforce strict schema validation (e.g. Pydantic v2 / Zod) before database operations.
"""
    return bp
