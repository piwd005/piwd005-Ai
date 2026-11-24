# Steps 1–3 implementation report

15 November 2026 · kit version 0.2.0

## Delivered

The installed skill now carries a generated 62-resource index and maps every resource to
one or more of its 24 routes. scripts/sources.py selects route/version metadata locally.
The repository registry is canonical. scripts/build_catalog.py generates the portable copy,
and --check plus installer tests catch stale or missing metadata. Candidate status never
grants copying or execution permission. Five external QA tools have explicit CLI admissions.
No upstream skill/application bodies, wheels or scanner binaries are distributed.

Original Odoo 19 and 20 guidance adds source-matched ORM/constraint behavior, transactions,
controller access, frontend differences, view/report checks, native tests and migration
reconciliation. Immutable Community revisions and reviewed file hashes are bundled in
odoo-version-evidence.json. The 19.0 inspected Owl bundle reports 2.8.4. The 20.0 official web
guidance targets Owl 3. Version-specific API guidance remains conditional on the installed
customer build, edition and modules. Upstream root licensing and file exceptions were reviewed
for reference use. No protected Enterprise code or upstream guide body was copied.

The QA runner supports Ruff, selected pylint-odoo checks, OCA module checks, Gitleaks and
pip-audit. It never installs dependencies or applies fixes. Existing tool executables or an
explicit tools directory are required. Missing prerequisites are NOT_RUN, execution problems
are ERROR and findings are FAIL. Exit 0 requires every selected check to pass. Native Odoo
checks require a single addon root and an explicit series. Project lint configurations,
fix modes and shell-string execution are not enabled by this baseline.

## Actual local results

| Check | Observed result |
|---|---|
| Unit/integration suite | 20 tests passed, exit 0, with the real QA environment selected |
| Portable catalog | 62 sources, all 24 routes, deterministic generated copy and installed-copy selection verified |
| Version selection | 19.0 selection excludes 20.0-only entries and the reverse selection excludes 19.0-only entries |
| Ruff on kit | PASS, no selected-rule findings |
| Gitleaks on kit | PASS after assessment of a public artifact-digest false positive |
| Clean synthetic addon 19.0 | Ruff, pylint-odoo and OCA checks PASS |
| Clean synthetic addon 20.0 | Ruff, pylint-odoo and OCA checks PASS |
| Deliberately defective Python | Ruff detects F821 and pylint-odoo detects invalid-commit on both series fixtures |
| Deliberately duplicate loaded XML ID | OCA hook detects xml-duplicate-record-id |
| Synthetic credential canary | Gitleaks detects it and the runner returns only rule/file/line metadata |
| Dependency advisory audit | No known vulnerabilities reported for all 50 distributions in the complete QA-tool lock |
| Missing tool/network permission, invalid lock, timeout and malformed diagnostics | Non-passing states verified |
| Skill format validator | PASS |

These are static-tool and package tests on synthetic fixtures. They do not load an Odoo
registry or demonstrate native 19/20 installation, upgrade, HTTP, browser, financial or stock
behavior. No production or customer data was used. No new paid model, Codex CLI evaluation
or Antigravity invocation was run. The previous behavioral evaluation remains historical,
including its one Antigravity support-response failure.

## Reviewed tool versions and reproducibility

| External QA tool | Tested version |
|---|---|
| Ruff | 0.17.5 |
| pylint-odoo | 10.0.12, with pylint 4.0.10 |
| oca-odoo-pre-commit-hooks | 0.2.27 |
| Gitleaks | 8.30.1, Darwin arm64 archive checksum verified |
| pip-audit | 2.10.1 |

Tests used macOS arm64 and CPython 3.12.7. Fifty downloaded wheel artifacts were hash-pinned
and installed into an isolated temporary QA environment with --no-index and --require-hashes.
Wheels, binaries and environments are excluded from Git. The platform-specific lock is
assets/qa/requirements-macos-arm64-py312.lock inside the skill. Other platforms require a
reviewed resolution and artifact hashes. The core helper code uses only the Python standard
library. Source provenance and the separate Gitleaks checksum are included.

## Findings resolved during implementation

An early Ruff baseline flagged model-registration imports in addon __init__.py files. The
adapter now exempts F401 only for package entrypoints within an explicitly versioned addon.
Generic Python package imports remain checked. A regression test verifies both behaviors.
The XML mutation fixture initially omitted its file from the manifest, so the OCA checker
correctly did not inspect it. The test now declares the loaded data file and verifies its
specific duplicate-ID diagnostic.

Six initial Gitleaks findings were the same already-public SHA-256 digest associated with
historical python-api.md evidence. One exact stopword documents that reviewed digest. There
are no file-wide exclusions. The synthetic canary confirms that unrelated credentials still
produce FAIL. A synthetic key was also constant-folded into a test bytecode cache during
fixture development. Its construction now occurs at runtime so source/bytecode contains no
complete canary value. Scanner output never publishes secret-bearing fields.

OCA licensing metadata is inconsistent. The hooks wheel/repository license text is AGPL-3.0
while package metadata says LGPL. pylint-odoo's README says AGPL-3.0, its PyPI field spells
APGL3, and its downloaded wheel lacks a license file. These caveats are retained in provenance.
The integration calls external tools and does not redistribute or incorporate their code.
Review applicable notices before redistributing those tools themselves.

Initial urllib metadata requests failed certificate verification. curl with working system
trust retrieved the metadata without disabling TLS verification. All wheel installs used
pinned hashes. The advisory audit transmitted public tool package names/versions with an
explicit network flag and disabled dependency resolution/builds.

## Commands

Run from the kit root. Substitute the approved local QA environment path.

```sh
python3 scripts/build_catalog.py
python3 scripts/build_catalog.py --check
PRIMACY_QA_TOOLS_DIR=/absolute/qa-venv/bin python3 -m unittest discover -s tests -v
python3 skills/primacy-engineering/scripts/qa.py --target . --checks ruff gitleaks --tools-dir /absolute/qa-venv/bin
python3 skills/primacy-engineering/scripts/qa.py --target . --checks pip-audit --requirements skills/primacy-engineering/assets/qa/requirements-macos-arm64-py312.lock --allow-network --tools-dir /absolute/qa-venv/bin --timeout 180
```

Every final command above exited 0. [QA setup](QA_SETUP.md) explains installation scope,
network audit, scanner baselines and output handling. [Resource usage](RESOURCE_USAGE.md)
distinguishes admitted tools, reviewed references and remaining candidates.

## Update and rollback

Back up the existing installed primacy-engineering folder before applying the reviewed
canonical copy. Compare old installed files with the previous Git revision and preserve
unexpected edits. Copy only the skill, including its new references/assets/scripts. Do not
copy virtual environments or raw audit logs. Restore the timestamped backup to roll back.
The canonical repository can be checked out at the previous commit for source rollback.
Client global settings and production systems are unaffected by this update.
