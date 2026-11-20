# Local browser, functional and AI/MCP contracts

Use the fixtures in [assets/contracts](../assets/contracts/test_primacy.py) for relevant changes.
The core skill remains standard-library only. Optional MCP and Playwright dependencies belong
in an isolated test environment. Review their pinned locks before installation; do not run
installers from source catalogs. MCP 2.3 uses snake_case Python SDK fields.

Set PRIMACY_SOURCE_ROOT to an authorized Primacy checkout. primacy-bindings.json pins six
reviewed source hashes at the recorded revision; drift fails closed. Review changed functions
and update hashes deliberately. The AST harness compiles only selected methods with synthetic
identity/time/config objects. It never imports the Odoo application or runs provider evaluation
main functions. The JS harness checks hashes before loading the two pure modules.

```sh
PRIMACY_SOURCE_ROOT=/path/to/primacy python3 assets/contracts/test_primacy.py -v
python3 -m venv /tmp/primacy-contract-tests
/tmp/primacy-contract-tests/bin/pip install --require-hashes -r assets/contracts/requirements-mcp.lock
/tmp/primacy-contract-tests/bin/python assets/contracts/test_mcp.py -v
# In a separate temporary directory, copy package.json and package-lock.json, then:
PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci --ignore-scripts --no-audit --no-fund
PRIMACY_SOURCE_ROOT=/path/to/primacy PRIMACY_PLAYWRIGHT_MODULE=/absolute/temp/node_modules/playwright/index.mjs node assets/contracts/browser.mjs
```

Run from the skill directory. Python lock is Python 3.12/macOS arm64; generate and review a
platform-specific lock for another runtime. Node >=20 and installed Chrome are required.
No browser download, user browser profile or paid model invocation is needed. Browser starts
headless with a fresh context, serves a loopback synthetic DOM and blocks external requests.
Close the context/server on failure. Native Odoo views, ACLs and real business transactions
require separate staging UAT; this DOM fixture verifies the real page-context helper only.

Browser assertions distinguish selected, visible and matching records, pager offset, primitive
dirty values, server-token handoff and desktop/mobile interactions. AI checks cover latest-user
privacy, UTF-8 bounds, strict classifier decisions, exact credit addition, canonical plans,
controller plan integrity/stale-snapshot/cancellation, forgery, identity/company/database/expiry/status/nonce denials. Functional checks run real manual
guidance through the existing inventory/manufacturing evaluator with scoped permission fakes.

MCP checks initialize, discover and call an official SDK stdio subprocess, enforce bounded
strict typed query input, reject company/model/URL/mutation inputs and unknown tools, then
verify recovery after rejection. Fixed synthetic company scope is server-owned. The 20-second
suite deadline prevents a hanging harness; it does not prove production timeout/cancellation,
OAuth audience checks, HTTP origin protection or SSRF defense. Tool annotations are hints;
access control must execute server-side on every real call. REST endpoints named MCP need
separate transport and authorization review before promotion as standard MCP servers.

For actual functional UAT, use a disposable database, target edition/module set, role/company
matrix and independent expected stock/accounting values. Exercise partial quantities,
lot/serial tracking, backorders, permission loss, stale approval and repeated confirmation.
Capture resulting records/states, errors and reconciliation; screenshots alone are insufficient.
Mark unavailable layers NOT_RUN. Preserve the 54 historical model evaluations separately.
