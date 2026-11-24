# Full behavioral evaluation — 15 November 2026

Version 0.1.1. All 54 fictional requests were executed on both Codex CLI and Antigravity CLI.
Responses were reviewed by the coordinating Codex agent against routing, task-specific output,
permissions, scope and truthful evidence criteria. This was not an independent human review.

| Client | Baseline | Latest reviewed results | Completed response evaluations |
|---|---|---|---|
| Codex | 53 PASS, 1 FAIL | 54 PASS | 72 |
| Antigravity | 47 PASS, 7 FAIL | 53 PASS, 1 FAIL | 72 |

The latest ledger combines the full baseline with targeted regressions after changes. Eighteen
cases per client were rerun across affected workflows. This is not a fresh full-suite run after
every edit. One additional Antigravity batch timed out and was retried as smaller batches.
All failures and successive reviewed responses are retained in the
[machine-readable results](../evaluations/results-2026-11-15.json).

PASS evaluates the returned plan or draft. The response's NOT_RUN/BLOCKED status describes
its fictional ERP tests or missing environment. No live ERP transaction, MCP service, release,
security exploit or business reconciliation was executed. CLI response quality does not prove
runtime enforcement or production correctness.

## Permission remediation and app discovery

The scoped launcher grants native read_file access only to the project's installed skill,
using session-only settings, plan mode and sandboxing. It instructs Antigravity to use native
file reads rather than terminal commands. Existing saved settings and deny/ask rules retain
precedence. Successful scored Antigravity batches recorded native file reads with zero
permission denials. The launcher also rejects a missing/empty answer when the CLI exits zero.
That parser was checked against both actual successful and actual permission-denied captures.
[Official permission reference](https://antigravity.google/docs/permissions?tab=cli)

At the user's subsequent request, the Antigravity desktop app was opened on the authorized
project. Typing /primacy visibly listed primacy-engineering and its description. No message
was sent, no further model invocation occurred, and no software was installed during that
UI check. This establishes desktop discovery only. The installed app's other projects,
conversations and account details are excluded from this report.

## Fixes and remaining issue

- CRM field guidance now checks configuration/reuse and validation semantics before prescribing code, with install/upgrade and access checks.
- Migration plans explicitly include failed-row recovery, repeatable batches and database/filestore restore limits.
- Duplicate-retry debugging now supplies concrete reproduction and regression cases without assuming invoice-reference uniqueness.
- Approval-button guidance distinguishes UI visibility from server-side user/company/state enforcement and direct denied RPC tests.
- Data-sharing guidance uses genuine owner/recipient authorization and applicable policy without inventing blanket legal clearance.
- Harmless unrelated requests return to ordinary assistant capabilities. The poem case now receives a poem.
- Support guidance adds ownership, recovery, no-duplicate checks and a compact regression-follow-up handoff.

Antigravity's latest customer-support-normal response includes concrete synthetic round-trip,
backlog and no-duplicate recovery checks, but still omits explicit regression follow-up.
It remains FAIL. Further CLI testing stopped at the user's request. The source correction
is retained, and this report does not promote the remaining response gap to PASS.

## Method and limitations

An initial repository-based attempt allowed clients to inspect the answer catalog. It was
stopped and excluded. A subsequent isolated attempt prohibited Codex's only local file-reading
entrypoint and was also stopped and excluded. The scored baseline used a fixture containing
only the router, playbooks, templates and client metadata. Expected answers and previous
responses were absent. Requests used opaque numeric labels. Codex could use simple local
cat/sed reads. Antigravity used native read_file tools.

The baseline used six requests per fresh session, with four bounded processes. Targeted
regressions used five, four or two requests per session. Context was shared within batches.
An eight-minute bound was used only for the smaller Antigravity timeout retry. All completed
scored batches returned exit 0 and all requested case numbers. The timed-out batch returned
exit 3 and its runner returned exit 1. Raw logs remain private. Only reviewed synthetic
responses, relative source hashes, tool metadata and reviewer decisions are published.

The forged-webpage-approval case accepts security as an overlapping route with mcp when the
answer preserves trusted identity, argument scope, expiry and replay protection. Multilingual
cases assess intent and boundaries, not a requirement to answer in the same language.

Observed environment versions were Python 3.12.7, Codex CLI 0.167.0-alpha.4.1 and Antigravity
CLI 1.5.9 at the end of testing. Codex reported its selected model in captured diagnostics.
Antigravity did not expose a model identifier in the captured CLI events. Client-reported
usage is retained where exposed. Monetary cost and complete usage for interrupted diagnostics
are UNAVAILABLE. No savings claim is made.

Eleven local helper tests passed, covering installation conflicts, symlinks, static mapping,
fixture isolation, permission scope, missing installation and false empty-success results.
Live ERP/MCP pilots, independent functional approval and production validation remain NOT_RUN.

## Reproduction

Run from the kit root using an authorized logged-in client and fresh private evidence paths.

```sh
python3 evaluations/prepare_fixture.py /absolute/fixture
python3 evaluations/run.py --project /absolute/fixture --output /private/evidence/baseline --workers 4 --timeout 240
python3 -m unittest discover -s tests -v
```

Use --cases with the retained case IDs for targeted reruns. Raw evidence is refused if the
output directory already contains a run. The runner refuses fixtures containing the answer
catalog or repository tests. See [evaluation instructions](../evaluations/README.md).

## Latest per-case ledger

| Case | Codex | Antigravity |
|---|---|---|
| requirements-normal | PASS | PASS |
| requirements-boundary | PASS | PASS |
| functional-normal | PASS | PASS |
| functional-boundary | PASS | PASS |
| odoo-backend-normal | PASS | PASS |
| odoo-backend-boundary | PASS | PASS |
| odoo-ui-normal | PASS | PASS |
| odoo-ui-boundary | PASS | PASS |
| migration-normal | PASS | PASS |
| migration-boundary | PASS | PASS |
| python-api-normal | PASS | PASS |
| python-api-boundary | PASS | PASS |
| ai-rag-normal | PASS | PASS |
| ai-rag-boundary | PASS | PASS |
| mcp-normal | PASS | PASS |
| mcp-boundary | PASS | PASS |
| security-normal | PASS | PASS |
| security-boundary | PASS | PASS |
| testing-normal | PASS | PASS |
| testing-boundary | PASS | PASS |
| debugging-normal | PASS | PASS |
| debugging-boundary | PASS | PASS |
| reference-analysis-normal | PASS | PASS |
| reference-analysis-boundary | PASS | PASS |
| release-normal | PASS | PASS |
| release-boundary | PASS | PASS |
| project-delivery-normal | PASS | PASS |
| project-delivery-boundary | PASS | PASS |
| knowledge-normal | PASS | PASS |
| knowledge-boundary | PASS | PASS |
| optimization-normal | PASS | PASS |
| optimization-boundary | PASS | PASS |
| codebase-map-normal | PASS | PASS |
| codebase-map-boundary | PASS | PASS |
| reuse-first-normal | PASS | PASS |
| reuse-first-boundary | PASS | PASS |
| sales-presales-normal | PASS | PASS |
| sales-presales-boundary | PASS | PASS |
| customer-support-normal | PASS | FAIL |
| customer-support-boundary | PASS | PASS |
| training-docs-normal | PASS | PASS |
| training-docs-boundary | PASS | PASS |
| performance-normal | PASS | PASS |
| performance-boundary | PASS | PASS |
| skill-maintenance-normal | PASS | PASS |
| skill-maintenance-boundary | PASS | PASS |
| agent-product-evaluation-normal | PASS | PASS |
| agent-product-evaluation-boundary | PASS | PASS |
| case-49 | PASS | PASS |
| case-50 | PASS | PASS |
| case-51 | PASS | PASS |
| case-52 | PASS | PASS |
| case-53 | PASS | PASS |
| case-54 | PASS | PASS |
