# Odoo 20 core resolution and manufacturing/accounting browser verification

Date: 2026-11-16, Asia/Kolkata. Skill release: 0.3.2.
Base kit: 67c402dfad0f4cc6a8c5ec2b686458cce4c7908a.
This follow-up supersedes the Core 20 blocker and manufacturing/accounting browser limits
in the historical 0.3.1 report. No Antigravity or paid model run was performed.

## Dependency resolved locally

The authentic prierp_core 20.0.1.0.19 module was present in the local cached origin/20.0 ref
of the user-owned prierp-acc repository. The local branch named 20.0 had only stock accounting;
checking that branch alone had missed the dependency. Selected project revision:

dd055e7d1a7097f7cea877823ac912c0a590b679, core tree
7332166abfc0a1501765bd17d72fd4da033ac5ef.

Exported just the authorized core module to the private QA addon path and verified all 140
source files byte-for-byte against git archive. No manifest version edits, missing-dependency
removal, license bypass or 19-series core substitution was used. The cached pin is qualified
here; it is not represented as the newest remote release. Runtime verification reported the
core installed at 20.0.1.0.19 and its normal local trial state. It was not registered with
PiCloud and no live subscription or external provider was connected.

The installed Primacy AI addon was the existing 20.0.9.49 candidate at source baseline
785673377a79516415af85b2fa6eb8722499f5d3, with isolated private fixes described below.
The verified core, AI addon and QA addon were also retained in a persistent private local
addon directory outside publication. Existing project checkouts and production were not
modified by that dependency export; no private source is bundled in this skill release.

## Isolation and approval review

Automatic approval review initially rejected an unconstrained install because the core has
PiCloud license/credits request code. Addressed the concern before loading it: every install,
Odoo shell and QA server ran through the macOS sandbox profile included in the test assets.
The profile was tested: localhost PostgreSQL connected successfully, while an external TCP
connection was denied with EPERM. It permits localhost outbound traffic and denies external
outbound traffic. Thus browser route blocking is supplemented by backend OS confinement.
Cron remained disabled. No licensing enforcement code/state was disabled or falsified.

Only the disposable databases created during the previous test task were used. Existing
user/customer databases and the unrelated running Odoo instance were left unchanged. Test
seeds use fresh synthetic products/vendors and private mode 0600 login files; they refuse
non-QA databases and existing credential output before mutation. Both guards were tested
with fake environments, without connecting to another database.

## Results

| Check | Actual result |
| --- | --- |
| Core 20 and Primacy AI dependency install | PASS: genuine 20-series core installed |
| Odoo 20 native execution tests | PASS: 41 |
| Odoo 20 native functional-engine tests | PASS: 24 |
| Odoo 20 native security tests | PASS: 28 |
| Odoo 20 native workflow tests | PASS: 12 |
| Odoo 20 native business reconciliation | PASS: 3 |
| Combined Odoo 20 native suite | 108 tests, zero failures, errors or skips |
| Native manufacturing browser workflow, Odoo 19 and 20 | PASS on both |
| Native supplier bill and credit browser workflow, Odoo 19 and 20 | PASS on both |
| Primacy 20 UI receipt/backorder, mobile contact and manual guidance | PASS |
| Actual chat-trigger success/rejection regression | PASS on both Owl variants after local fix |
| Existing kit/scanner regressions | PASS: 20 tests |
| Seed guards, fixture lint/JS syntax, skill validator/catalog | PASS |

Odoo runtime sources remain pinned to 006220901d6b466fc296edbbcec962d2168a0782 (19) and
50b51284b32960690293c5f9510e8ce6834664aa (20). Browser: existing Chrome 157.0.8103.51,
external Playwright 1.65.1 from the previous lock. No new dependency or global IDE setup.
The historical Odoo 19 native suite's 104 tests were not repeated: its application source
was unchanged in this task; the newly requested browser workflows ran on both series.

## Real browser workflow and reconciled evidence

The seed creates a draft manufacturing order for one item and puts 10 components in source
stock. It never confirms/completes manufacturing. Through actual native buttons, the browser
confirms the order, enters one actual produced unit, then uses Produce. Read-only verification
finds Done, 2 consumed, 1 finished, 8 component units remaining and 1 finished item in stock.
The rendered native statusbar must also show Done before the screenshot.

The accounting seed creates a draft no-tax supplier bill with two units at 50. The browser
uses native Confirm, opens Credit Note, fills the reversal reason, uses the native Reverse
wizard and confirms the resulting credit. Read-only assertions find the bill and linked
credit posted at 100 each, balanced journal lines, offset expense balances and zero residuals
for both documents. Both rendered statusbars must reach Posted before evidence capture.
All business completion/posting/reversal writes come from UI buttons; the verification RPC
helper rejects write methods and permits only read/search_read/search_count.

The separate Primacy 20 UI check also validates receipt/backorder quantities, contact save
and mobile reopen, then opens unpaid manual inventory guidance. No stock-picking or AI credit
record counts change from that guidance. Both browser suites require no unexpected browser
errors. The core's normal trial banner is visible in the synthetic screenshots.

## Failures found and fixed

- A newly discovered 20-series purchase test used the removed product_uom_id field. Corrected
  its isolated fixture to purchase.order.line.uom_id and reran all 108 tests successfully.
  The actual production purchase helper already used the correct field.
- The 20-series trigger still had an unawaited action restore inside a synchronous catch.
  Applied the already verified minimal async-await correction to the private QA copy. The
  actual-class regression reproduces the old behavior and verifies the fixed success and
  rejection paths; the real Primacy 20 browser check passes with rebuilt assets.
- The original tiny trigger harness lacked Owl 3 props hooks. Added props/lifecycle fakes
  for that variant, while continuing to test the actual source class on both series.
- Evidence review found that a screenshot could capture a stale Draft screen after the
  posting response had committed. Added explicit rendered Done/Posted assertions before
  capture and reran both business browser workflows. A subsequent cold-form timeout also
  exposed an unhandled response-wait promise in the harness; it now waits for the visible
  action control first and handles click/response promises together. No arbitrary sleep
  or server write was used to make the status match. The database and UI assertions now agree.

Private application fixes and their review patch remain local, excluded from Git publication.
The separate private application repository was not pushed. This upload contains original
skill/test fixtures, sanitized results and synthetic screenshots only.

## Reproduction and artifacts

Read [the native test recipes](../skills/primacy-engineering/references/native-odoo-testing.md).
New assets: seed_business_ui.py, business_ui.mjs and local-only-macos.sb. The existing source
trigger regression now supports Owl 2 and Owl 3. Use explicit private fixture, origin,
evidence-directory and Playwright-module variables as documented; run the matching Odoo
checkout under verified OS network confinement. Never publish the credential fixture.

Sanitized results and hashes: evaluations/core20-browser-2026-11-16.json.
Reviewed screenshots: evaluations/core20-browser-evidence/.

## Remaining limits

This is local Community plus Primacy qualification at the exact revisions above, under a
normal trial that can expire. It is not a production deployment or a general certification
of every addon. No real provider, live MCP authorization, paid model evaluation, tax/GST
localization, multicurrency, manufacturing lots/serials, partial production browser flow,
full accessibility audit or concurrency/load test was run. Those require separate acceptance
cases and authorized environments. No external license registration was performed.
