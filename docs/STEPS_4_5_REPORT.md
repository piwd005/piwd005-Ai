# Steps 4–5: local browser, functional and AI/MCP tests

Date: 2026-11-15. Kit release: 0.3.0. Base kit revision:
4ef6dc5bbb46a67691304442b30b7623c2cec385. Reused Primacy checkout revision:
3cd98c5dc022c7ff5dbf83f5be726dfb43493032, with individual source hashes in
skills/primacy-engineering/assets/contracts/primacy-bindings.json.

## Implemented

The existing Primacy page-context and task-classifier modules run directly from an explicitly
selected checkout. Existing execution-model methods, controller preflight paths, functional
guidance and workflow-quality evaluator are extracted by AST after verifying exact source
hashes. No Odoo application imports, provider main functions or private implementations are
copied into this kit. Hash drift fails and requires deliberate review/re-pinning.

The portable skill now routes testing, functional, AI and MCP tasks to executable local recipes.
Optional Playwright and official MCP SDK dependencies have isolated, artifact-pinned locks
and provenance. Standard-library core helpers and client adapters remain unchanged.

## Local results

| Check | Actual result |
| --- | --- |
| Existing package, catalog, adapter and real QA scanner regressions | PASS: 20 unittest methods |
| Actual Primacy execution and functional contracts | PASS: 4 unittest methods, including denial subcases |
| Actual Primacy JS browser/context and classifier assertions | PASS: Chrome 157.0.8103.51, widths 1280 and 390 |
| Official SDK stdio client/server protocol fixture | PASS: 1 asynchronous test with seven malformed/scope-changing input denials and unknown mutation tool denial |
| Ruff on new Python fixture code | PASS |
| Skill validator, generated catalog check and redacted Gitleaks scan | PASS |
| MCP dependency lock verification and pip check | PASS |
| Clean npm ci from portable lock, scripts/browser downloads disabled | PASS |
| pip-audit, 28 pinned MCP dependencies | PASS: no known vulnerabilities at audit time |
| npm audit, reconstructed Playwright tree | PASS: zero reported vulnerabilities |

Confirmation cases cover canonical argument hashing, forged token, user/company/database
changes, expiry, completed/cancelled status, nonce changes, stored-plan tampering, stale target
snapshot and cancellation/reuse denial. They do not exercise the actual database unique
constraint or concurrent transactions. Inventory/manufacturing guidance includes real manual
checks and configured-scope/permission denial with synthetic environment objects.

Browser tests use a fresh headless context and a loopback synthetic DOM; external requests are
blocked. They validate actual helper selection versus visible/matching scope, paging, primitive
dirty fields, token handoff, UUID shape, accessible label/button interaction and mobile width.
This is not full accessibility certification or a test of the running Odoo UI.

MCP initializes and negotiates protocol with a real official SDK subprocess, discovers one
read-only fixture tool, calls it, validates strict bounded query input and verifies recovery
after rejection. Server-owned synthetic scope cannot be changed through query arguments.
No legacy REST controller is represented as a verified standard MCP server.

## Fixes during implementation

The first MCP harness used pre-2.x camelCase Python attributes and failed. Corrected to SDK
2.3 snake_case fields, then reran successfully. Ruff import/style findings were corrected.
The initial npm prefix-generated lock contained temporary path keys; normalized the portable
lock and verified clean npm ci and browser execution from the reconstructed installation.
No demonstrated production Primacy defect required an application change.

## Reproduction

See skills/primacy-engineering/references/local-contracts.md for commands, explicit environment
variables and prerequisites. Optional fixtures are outside default unittest discovery so
missing third-party packages cannot masquerade as passing/skipped core tests. Run all three
fixture commands explicitly when their contracts change. Results are summarized in
evaluations/local-contracts-2026-11-15.json; assertions fail with nonzero exits.

## Remaining limits

Native Odoo 19/20 browser UI, real ACL/record-rule enforcement, actual stock/accounting
reconciliation, database idempotency/concurrency and live MCP authorization are NOT_RUN.
The source checkout's existing native Odoo tests remain the required next layer in a
disposable database. Production OAuth audience checks, HTTP origins, SSRF, cancellation and
permission changes during execution are not established by a stdio fixture. The 20-second
harness deadline only bounds these local tests. Dependency audits are time-specific.

No expensive Codex/Antigravity model runs, new runtime installation in either IDE, production
calls or customer records were used. The previous 54-case behavioral evaluation results are
historical and unchanged; this release makes no new claim that all 54 pass on both clients.
No global client permissions/configuration were changed.
