# Odoo change procedures

Read the relevant section after establishing [19.0](odoo-19.md) or [20.0](odoo-20.md).
Use the source selector for matching documentation and candidate tools. Every procedure
finishes with changed behavior, actual commands/results, unresolved prerequisites and reviewer.

## Addon and ORM

1. Trace manifest dependencies, Python imports, inherited classes, method callers, views/actions,
   external IDs and access rules. Reuse configuration, existing fields/helpers or an approved addon.
2. Define the business invariant with valid, invalid, omitted and boundary examples. Determine
   company ownership, field security, defaults, historical records and import/API behavior.
3. Change the shared implementation once. Preserve multi-record calls, compute dependencies,
   inverse behavior and caller error contracts. Avoid per-record queries when a batch query works.
4. For database constraints/indexes, inspect existing data, name and target-version definitions.
   Rehearse duplicate cleanup and upgrades. Keep legitimate repeated business references valid.
5. Test normal create/write/read and denied users/records/companies in native Odoo. Include
   omitted input, old records, batch operations and a fresh install plus existing-data upgrade.

## Access and controllers

Trace authenticated identity from HTTP/RPC entrypoint to model method. Check model ACLs,
record rules, field restrictions, company boundaries and ownership using the actual effective
user. UI visibility never authorizes a backend operation. Review public method parameters,
sudo/elevation, unsafe domains, direct SQL, upload paths and exposed binary fields.

For a button/action, assert both authorized state transition and denial of a direct call by
an unauthorized user without loading the view. For controllers, test route auth and HTTP
methods, CSRF where applicable, malformed inputs and identifiers of another company/owner.
Keep untrusted external data outside policy and approval decisions.

## OWL, views and reports

Resolve the inherited template/component and the target-version asset bundle. Prefer existing
registries, services and extension points. Verify markup inheritance against real parent views.
For asynchronous UI state, exercise overlapping calls, errors, cancellation and unmount cleanup.
Test keyboard navigation, focus, labels, translations and small screens with the intended role.

Escape untrusted QWeb text and review any explicit raw/HTML output. Validate portal ownership
and download routes independently of template filtering. For PDF output, render long tables,
page breaks, repeated headers, currency/rounding and mixed-language descriptions. Keep screenshots
or rendered pages tied to the source revision. Syntax or XML parsing alone does not verify layout.

## Native tests and QA

Obtain the actual project's Odoo executable, configuration and isolated database recipe.
Do not invent production endpoints or use a live database for install/upgrade checks. Native
ORM tests load the registry and validate transactions/access. HTTP tests exercise controller
entrypoints. Use the branch's frontend runner for component behavior and browser/tour checks
for workflows. Standalone Python tests cover the kit and external Python services.

Run the packaged QA helper for scoped static checks. Ruff covers selected Python correctness
rules. The Odoo pylint baseline checks selected ORM/manifest hazards. OCA hooks inspect addon
XML/CSV structure. Gitleaks detects configured secret patterns. pip-audit checks a complete
pinned dependency lock against advisory data. Each reports its own scope and outcome.
None establishes business reconciliation, installation success or complete security.

## Migration and release

Map source and target series, modules, stable external IDs, field/relation transformations,
companies, rounding, expected counts and independent business totals. Design repeatable batches,
failed-row isolation, rejection reporting and safe restart after interruption. Define the
boundary between transaction rollback and database-plus-filestore restoration, including
new transactions that could be lost after a backup.

Rehearse a fresh install and existing-data upgrade on approved staging data. Reconcile counts,
references, stock and accounting outcomes against approved expectations. Verify denied access
and affected reports/UI. Record restore evidence, cutover, smoke checks, monitoring and rollback
limits. Obtain scoped authorization for migrations and production actions. Preserve unrun checks
as NOT_RUN and attach actual evidence before functional acceptance.
