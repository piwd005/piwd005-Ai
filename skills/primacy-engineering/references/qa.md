# Scoped deterministic QA

Run from this installed skill directory. Select an explicit trusted local target. The helper
uses the standard library and subprocess argument lists. It never installs tools, edits code,
loads project lint configuration or enables auto-fix. Use existing reviewed executables, or
an approved isolated QA environment. No Antigravity or other model invocation is involved.

```sh
python3 scripts/qa.py --target /absolute/addon --checks ruff pylint-odoo oca-hooks --odoo-version 19.0 --tools-dir /absolute/qa-venv/bin
python3 scripts/qa.py --target /absolute/project --checks gitleaks --tools-dir /absolute/qa-venv/bin
```

| Check | Actual scope |
|---|---|
| Ruff | E4/E7/E9/F correctness rules on bounded Python files, isolated configuration, no fixes. Odoo package __init__.py imports are exempt from F401 because they register models |
| pylint-odoo | Selected SQL injection, manual commit, context, return and manifest checks against the requested Odoo series |
| OCA hooks | Addon XML/CSV/module checks through oca-checks-odoo-module, with no --fix |
| Gitleaks | Directory scan using default built-in rules, full redaction, no symlink-follow flag and no project ignore override |
| pip-audit | Known advisories for an explicit, complete hash-pinned lock, without pip resolution or builds |

For native Odoo checks, the target must be a single addon root. Odoo version is explicit.
A manifest with a conflicting 19.0/20.0 prefix is an error. The static tools are not a native
Odoo registry test. Their coverage of a new series can lag the server and requires assessment.
The Python scan excludes hidden/build/environment directories and refuses more than 500 files.
OCA hooks and Gitleaks apply their own file discovery. Review their scope for the target.

Gitleaks findings contain only rule, file and line metadata. Secret-bearing fields and scanner
stdout/stderr are discarded even with redaction requested. Other diagnostics are bounded to
8000 characters and may contain private source identifiers. Keep reports private unless reviewed.

Dependency audit is opt-in because it transmits package names and versions to the advisory
service. It refuses direct URLs, includes, editable requirements and unpinned inputs. Supply
single-line name==version entries with SHA-256 hashes for the complete environment graph.

```sh
python3 scripts/qa.py --target /absolute/project --checks pip-audit --requirements /absolute/reviewed.lock --allow-network --tools-dir /absolute/qa-venv/bin --timeout 180
```

The bundled assets/qa/requirements-macos-arm64-py312.lock records the exact QA tool wheel graph
reviewed on macOS arm64 CPython 3.12. It is a platform-specific test lock. Other platforms need
a reviewed resolution and matching artifact hashes. Core skill Python imports remain standard
library only. Gitleaks is a separate checksum-verified executable and is not bundled.
Provenance and licenses are recorded in assets/qa. No source code from these tools is vendored.

A missing executable, absent prerequisite or disabled network audit is NOT_RUN. A timeout,
invalid scope/lock or tool execution problem is ERROR. Findings are FAIL. Exit 0 requires all
selected checks to PASS. Exit 1 means findings. Exit 2 means incomplete/error checks. Never
turn missing tools into a passing QA result. Preserve actual outcomes in the task evidence.

The bundled Gitleaks configuration has one exact stopword for a reviewed, already-public
SHA-256 digest in historical evidence. It contains no directory-wide exclusions. A synthetic
credential canary is independently checked to ensure unrelated secret detection still fails.
The advisory test covers the QA-tool lock only, not every application dependency in a project.
