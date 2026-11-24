# Native Odoo UI and functional follow-up — 0.3.1

Historical results. The Core 20 blocker and manufacturing/accounting browser limits below
are superseded by [the 0.3.2 follow-up](ODOO20_CORE_BROWSER_REPORT.md).

Local date: 2026-11-16 (Asia/Kolkata; raw server logs use UTC 2026-11-15).
Base kit: 43ae702bc8cdb00149948964b09bafcf67574039.

## Verified results

| Layer | Actual result |
| --- | --- |
| Odoo 19 Primacy execution contracts | PASS: 39 native transaction tests |
| Odoo 19 Primacy functional engine | PASS: 22 native transaction tests |
| Odoo 19 Primacy security | PASS: 28 native transaction tests |
| Odoo 19 Primacy workflow adapter | PASS: 12 native transaction tests |
| Odoo 19 business reconciliation | PASS: 3 native transaction tests |
| Odoo 19 final combined result | 104 tests, 0 failures, 0 errors, 0 skips |
| Odoo 20 business reconciliation | PASS: 3 tests, 0 failures, 0 errors, 0 skips |
| Odoo 19 actual browser UI | PASS: receipt/backorder, contact save/mobile reopen, manual Primacy inventory guidance |
| Odoo 20 actual browser UI | PASS: receipt/backorder and contact save/mobile reopen |
| Actual Primacy chat trigger regression | PASS: async restore success and rejection |
| Kit regressions, real QA tools selected | PASS: 20 tests |
| Skill validator, Python fixture lint, JS syntax and secret scan | PASS |
| Primacy AI addon on Odoo 20 | BLOCKED: required prierp_core unavailable in the supplied 20-series addon set |

Browser: installed Chrome 157.0.8103.51, fresh contexts, widths 1440 and 390. Actual Odoo
form controls, native backorder dialogs and persisted database state were exercised. This
replaces the earlier synthetic-DOM-only limitation for the specific UI flows above.

The final Odoo logs report 104 and 3 actual tests; the larger per-module statistics include
setup/teardown. Optional fixture tests were discovered by Odoo itself, not imported by the
addon during normal server startup. No expensive Antigravity or paid model runs occurred.

## Runtime and scope

Fresh databases were created solely for this task, without customer data or demo records.
Existing databases and the already-running Odoo instance were left unchanged. Separate
loopback servers used exact database filters, no database list and zero cron threads.
Browser requests to external origins were blocked. No provider credentials, shipping/payment
connections or outgoing-email services were configured in the QA databases.

Inspected runtime revisions:

- Odoo 19 Community: 006220901d6b466fc296edbbcec962d2168a0782.
- Odoo 20 Community: 50b51284b32960690293c5f9510e8ce6834664aa.
- Primacy 19 source baseline: 3cd98c5dc022c7ff5dbf83f5be726dfb43493032, with the two local fixes below.
- Primacy 20 addon candidate: 785673377a79516415af85b2fa6eb8722499f5d3; addon version 20.0.9.49.
  Its installation failed before Primacy tests because prierp_core was missing. Business
  tests on Odoo 20 therefore use the independent QA addon; they do not certify that AI addon.

The existing Python 3.12 environment and installed Chrome were reused. Native ORM tests
ran against PostgreSQL with actual ACLs, company contexts and transactions. Existing Primacy
execution tests still fake HTTP/provider/progress boundaries where their original tests do;
they do not certify a real model provider or parallel request idempotency.

## Actual business evidence

The native browser and ORM receipt flows demanded 5 units, processed 3, selected Create
Backorder, reached Done, increased destination stock by 3 and left exactly 2 outstanding in
one backorder. Earlier native tracking/backorder guard tests also passed on Odoo 19.

Manufacturing started with 10 components, completed one finished item using 2 components,
reached Done and reconciled component/finished stock to 8 and 1 on both Odoo series.
Accounting posted a supplier bill for 100 and its credit for 100, checked balanced journal
entries, offset expense balances and zero residuals after native posting/reconciliation.
This is a simple synthetic no-tax scenario; it does not establish Indian GST or another
localization, multicurrency, valuation methods or customer-specific accounting treatment.

The contact was edited through the real form, saved, read back through the authenticated
ORM endpoint and reopened at mobile width. Primacy manual inventory guidance was submitted
through its actual UI; stock-picking and AI credit-ledger counts stayed unchanged. No AI
execution/Prepare with AI button was pressed. These are representative workflows, not a
claim that every Odoo screen or all ERP workflows have been tested.

## Failures found and corrected

1. Workflow tests existed but were absent from pi_erp_agentic_ai/tests/__init__.py. Added
   their import; all 12 workflow tests now run, including permissions/company checks.
2. Direct opening of the Primacy chat trigger produced an unhandled ControllerNotFoundError.
   actionService.restore() returns a promise, so its synchronous try/catch missed rejection.
   Awaited restore inside the mounted callback. The actual-class regression and rebuilt
   native browser assets verify both the rejected and successful restore paths.
3. The initial Odoo 19 environment lacked CRM: one existing test errored and three skipped.
   Installed CRM in the disposable database and reran: all 104 tests passed with no skips.
4. New fixture assumptions were corrected from runtime evidence: stock.move.name is absent
   on the inspected 19 source, refund posting requires invoice_date, and native credit
   posting had already reconciled the payable lines. The final assertions verify the result
   without attempting duplicate reconciliation.
5. Odoo 20 stock.move uses uom_id, and the inspected BOM no longer has consumption. Fixtures
   now branch explicitly for the inspected 19/20 series; all three business checks pass.
6. Browser harness fixes await web_save before readback and use DOM readiness plus specific
   controls. Initial early-read/navigation timeouts are preserved as harness failures in
   this report; they are not represented as production application defects. The final harness
   allows 60 seconds for cold native view loads, and bounded failure screenshots preserve
   the original exception instead of masking it with a font-loading timeout.

The two Primacy application fixes are applied locally, with a private rollback/review patch
retained outside the publication. The separate Primacy application repository was not pushed.
Automatic approval review rejected publishing a patch derived from that private repository
without explicit disclosure authorization. The published kit therefore contains original test
fixtures, skill guidance and sanitized results; it does not contain that private patch or a
copied application tree. Source fixes must be delivered through the authorized private
application repository separately.

## Reproduction and evidence

Use [native testing recipes](../skills/primacy-engineering/references/native-odoo-testing.md).
The original disposable QA addon, guarded seed script, browser harness and trigger regression
are in skills/primacy-engineering/assets/native_odoo. The seed creates a fresh private mode
0600 credential file outside the repository; raw credentials and database dumps are excluded.
Existing external Playwright toolchain locks from 0.3.0 are reused, with no new dependency.

Sanitized results and source/artifact hashes: evaluations/native-odoo-2026-11-16.json.
Reviewed synthetic screenshots: evaluations/native-evidence/.

## Remaining limits

Primacy AI installation/UI on Odoo 20 requires the matching reviewed prierp_core source;
removing that dependency or substituting a 19-series core would conceal the compatibility
problem. It remains BLOCKED, not PASS. No live MCP transport authorization, real provider,
production deployment, customer UAT, concurrency/load, full accessibility audit or Odoo 20
Primacy AI compatibility claim is made. Manufacturing/accounting completion above is native
ORM coverage; their full browser workflows were not exercised. The historical 54 client/model
cases were not rerun. No production or global IDE permissions/configuration were changed.
