# Provenance

Original playbooks and helpers were authored for Primacy from the user's design briefs.
The source catalog retains user-supplied research claims and links. No third-party skill
bodies or application implementations are vendored. Registry entries are not license clearance.
Four earlier repository reviews are summarized in docs/UPSTREAM_REVIEW.md. Verify exact
selected files and terms again before future admission. Retain file-level notices if admitted.

Odoo 19/20 references were checked against pinned Community source, whose root license
is LGPL-3.0 with file-level exceptions possible. The added procedures are original guidance
and link to those sources. No upstream guide or implementation body is copied. QA tools
run as external CLIs. Their wheels/binaries are not redistributed. Ruff and Gitleaks declare
MIT, pip-audit declares Apache-2.0, and OCA tool licensing discrepancies are preserved in
assets/qa/provenance.json inside the skill. Inspect those terms before redistributing tool code.

## Optional local contract test tools (0.3.0)

Playwright 1.65.1 and playwright-core 1.65.1: Apache-2.0, Microsoft,
https://github.com/microsoft/playwright. MCP Python SDK 2.3.0: MIT,
https://github.com/modelcontextprotocol/python-sdk. Tools and their transitive dependencies
are installed externally only when explicitly selected. No SDK implementation, wheel,
node_modules or Chrome binary is redistributed. Exact artifact integrity and platform
scope are in skills/primacy-engineering/assets/contracts/{package-lock.json,provenance.json}.
Retain upstream notices when distributing those dependencies separately.
