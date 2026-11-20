# Native Odoo UI and functional verification

Use a fresh disposable database and the exact target series/addon revision. Never clone a
customer database for public test evidence. The optional original addon in
[assets/native_odoo](../assets/native_odoo/primacy_native_qa/tests/test_business.py) verifies
real receipt/backorder quantities, manufacturing consumed/finished stock, and posted bill/
credit balances. It depends on business apps, independently of the Primacy AI addon.

Check addon tests/__init__.py imports before selecting tests. Odoo can finish successfully
with no selected tests; require its final test count and zero failures/errors/skips. Module
updates/installations determine which post-install suites run: use -u on already installed
modules when selecting their tests again. Statistics include setup/teardown; report the
actual tests.result count. The addon root must not import its tests in normal server mode.

Use the matching Odoo checkout and already approved Python environment. Include core addons,
the Primacy addon directory and assets/native_odoo in --addons-path. On Odoo 20, copy the QA
addon into a temporary directory and change only its manifest version to 20.0.1.0.0. Keep
unavailable Primacy dependencies explicit; do not remove dependencies to claim compatibility.

Example arguments for a **fresh** Odoo 19 test database (substitute local paths):

```sh
"$ODOO_PYTHON" "$ODOO_BIN" -c "$EMPTY_QA_CONFIG" \
  --addons-path "$CORE_ADDONS,$PRIMACY_ADDONS,$NATIVE_FIXTURES" \
  --data-dir "$QA_DATA" --db_host 127.0.0.1 --db_user "$QA_DB_USER" \
  -d primacy_native19_qa --without-demo=all -i primacy_native_qa,pi_erp_agentic_ai \
  --test-enable --test-tags /primacy_native_qa,/pi_erp_agentic_ai:TestAiAssistantFunctionalEngine,/pi_erp_agentic_ai:TestAiAssistantExecution,/pi_erp_agentic_ai:TestAiAssistantSecurity,/pi_erp_agentic_ai:TestAiAssistantWorkflows \
  --stop-after-init --no-http --max-cron-threads 0
```

Install CRM, sales, purchase, stock, manufacturing and accounting before claiming their
coverage. Tests requiring absent apps may skip or fail. Do not enable live providers,
shipping/payment integrations, cron jobs or outgoing email. The receipt fixture expects 5
demanded, 3 received, 2 backordered and a stock increase of 3. Manufacturing starts with
10 components, consumes 2 and produces 1 finished item; expect 8 and 1 in stock. The supplier
bill and credit are 100 each; expect balanced entries and zero residual after native posting.
These are independent expected quantities for synthetic workflows, not customer acceptance.

For native browser checks, run seed.py through Odoo shell in the disposable database. Set
PRIMACY_NATIVE_FIXTURE to a **new private file outside the repository**. The seed refuses
existing output, requires a primacy_native database prefix, rotates only the disposable admin
password, creates fresh synthetic records and commits them. It writes mode 0600 credentials;
never publish that file. Existing user/company databases must not be targets.

Serve only that database on 127.0.0.1, with --db-filter matching it exactly,
--no-database-list and --max-cron-threads 0. Set PRIMACY_NATIVE_ORIGIN to its loopback HTTP
origin, PRIMACY_NATIVE_EVIDENCE to a private existing output directory, and
PRIMACY_PLAYWRIGHT_MODULE to the external pinned Playwright index.mjs described in
[local contracts](local-contracts.md). Then run assets/native_odoo/browser.mjs.

The browser uses a fresh context, blocks external browser requests and closes on failure.
It clicks native Validate/Create Backorder, independently reads persisted stock/remaining
demand, edits/saves a contact and reopens it at mobile width. On an installed Primacy addon,
it opens manual inventory guidance and checks that stock/credit record counts do not change.
A live AI prompt is never sent. Backend network isolation still requires disabled integrations;
browser routing alone does not restrict the Odoo process. Use a new seed file/records per run.

Await the actual web_save response before reading the saved record. Use DOM readiness plus
specific controls instead of waiting for every page resource. Collect browser errors and
assert no unexpected error remains. For the async direct-chat restore regression, run
PRIMACY_SOURCE_ROOT=/path/to/primacy node assets/native_odoo/test_trigger.mjs. It exercises
the actual trigger class with service/lifecycle fakes; the native browser confirms the fix.

Observed series differences at the revisions in the native report: stock.move uses
product_uom on 19 and uom_id on 20; the 19 BOM consumption field is absent on inspected 20.
Re-inspect live metadata before extending these fixtures. Do not infer identical schemas.
Report UI, ORM, AI-addon, provider and transport coverage separately. A completed receipt
screen does not establish accounting localization, concurrency or a live integration.

## Resolve project dependencies at a pinned revision

A local branch can differ from its cached origin ref. Inspect both trees before concluding a
module is missing. Read the target manifest and dependency closure; establish its actual
series from source and installation. For the local 20-series qualification, prierp_core
20.0.1.0.19 was available at prierp-acc ref origin/20.0, revision
dd055e7d1a7097f7cea877823ac912c0a590b679, tree 7332166abfc0a1501765bd17d72fd4da033ac5ef.
The local branch named 20.0 lacked that module. This is a tested project pin, not a claim
that the cached ref is the latest remote release or generally approved for all projects.

Export only the authorized module from that revision to a private addon directory, verify
its bytes against the archive, and add the directory to the disposable runtime's addons
path. Install the unmodified dependency; do not change a 19 manifest to claim a 20 port,
remove required dependencies, fabricate license state or bundle private code into the skill.
Check installed module versions and normal licensing status as well as process exit status.

This core contains optional PiCloud calls. For local qualification on macOS, launch **every
Odoo install, shell and server process** through sandbox-exec with
assets/native_odoo/local-only-macos.sb. Verify the profile on the machine first: PostgreSQL
on loopback must connect and an external TCP target must fail with EPERM. The profile denies
external outbound network access while permitting localhost. Other platforms require an
equivalent independently verified network restriction. Browser route blocking alone does
not constrain backend requests. Leave cron disabled and do not register/connect licenses or
providers. Normal local trial behavior was sufficient for the recorded test; it can expire.

## Manufacturing and accounting through actual UI

Use assets/native_odoo/seed_business_ui.py through the same confined Odoo shell with a new
PRIMACY_NATIVE_FIXTURE file. It seeds a draft manufacturing order, 10 component units and a
draft supplier bill (2 x 50), never completing production or posting accounting entries.
The guards reject non-QA databases and existing output before mutation. It requires a normal
unlocked core status where that module exists and writes credentials with mode 0600.

Run assets/native_odoo/business_ui.mjs with the same explicit fixture/origin/evidence and
external pinned Playwright module variables used above. Business writes must come from
native UI buttons: Confirm, Produce, bill Confirm, Credit Note, Reverse and credit Confirm.
The verification RPC helper permits read/search_read/search_count only. Independently
reconcile actual component/finished stock, balanced move lines, linked reversal and both
residuals. Assert the rendered native statusbar reaches Done or Posted before screenshots;
a committed database response can precede the visual refresh. Capture errors and close the
fresh context on failure. The fixture is full-quantity, untracked production and no-tax
accounting; partial production, tracked lots, taxes and localization need separate cases.

The 20-series fixture uses purchase.order.line.uom_id, not product_uom_id. Its Owl trigger
uses useProps; the tiny trigger regression supplies lifecycle/props fakes for both Owl
variants. An async action.restore rejection needs an awaited catch; a synchronous try/catch
around an unawaited promise does not handle it. Keep private application fixes local unless
disclosure through that application's repository is explicitly authorized. Publish only
original test recipes, sanitized evidence and the test report.

For India localization and currency reconciliation, use the separate
[GST and multicurrency test recipe](gst-multicurrency-testing.md).
