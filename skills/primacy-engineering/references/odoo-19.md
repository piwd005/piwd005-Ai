# Odoo 19 engineering reference

Use for an explicitly established 19.0 target. The source baseline is Community commit
a157617c921669c5c036509b341be6a07ad1069d, inspected 15 November 2026. A customer's patch level, Enterprise modules and Primacy
extensions still require inspection. These procedures are original Primacy guidance with
immutable source references. No upstream skill body or implementation is bundled.

## Establish the target

Record the server version/build, edition, addon manifest, installed dependencies and source
revision. Follow imported addon entrypoints and inherited methods. Compare current database
fields and XML IDs with the intended change. A manifest prefix alone cannot prove runtime version.
Use [shared workflows](odoo-workflows.md) for the affected area.

## Backend and transactions

Use recordset-aware ORM calls and preserve caller signatures and batch create/write behavior.
The inspected 19.0 source supports models.Constraint and models.Index as class attributes.
Choose the invariant and repair existing incompatible data before adding a database object.
Do not infer uniqueness from a repeated invoice reference or event payload.

Python constraints run when their declared simple fields occur in create/write values.
They do not establish that an omitted value was checked. When absence is part of the business
rule, inspect required/default/create semantics and test an input that omits the field.
Review computed-field dependencies, inverses, stored values, company consistency and field
access restrictions before changing a field on existing records.

Keep ORM-managed transaction ownership. Use the existing savepoint/retry pattern for a
recoverable operation. A manual commit inside normal model logic can separate business
changes that callers expect to succeed or fail together. Test retries around committed
side effects and concurrent workers using an established logical operation key.

[Constraint and index definitions](https://github.com/odoo/odoo/blob/a157617c921669c5c036509b341be6a07ad1069d/odoo/orm/table_objects.py) · [Constraint decorator behavior](https://github.com/odoo/odoo/blob/a157617c921669c5c036509b341be6a07ad1069d/odoo/orm/decorators.py)

## Controllers and views

The inspected HTTP implementation uses jsonrpc as a request type and retains json as a
deprecated alias. Inspect the route's actual auth, CSRF and method behavior before changing
it. Re-decorate route overrides explicitly and test through the HTTP entrypoint with the
correct user. A successful backend model test does not prove controller access is safe.

Resolve inherited view/XML IDs in the installed module set. Validate server-side action
permissions independently of hidden fields/buttons. For reports, verify both rendered HTML
and PDF with long descriptions, pagination, localized values and the intended user/company.

[HTTP implementation](https://github.com/odoo/odoo/blob/a157617c921669c5c036509b341be6a07ad1069d/odoo/http.py)

## Frontend and tests

The inspected bundled Owl source identifies version 2.8.4. Follow the existing 19.0 component
and service patterns. Do not apply 20.0 Owl 3 hook signatures to it. Confirm asset bundles,
template names, event cleanup, asynchronous request ordering and access errors in the target app.
Native TransactionCase and HttpCase are available in the inspected test source. Put ORM
checks in native Odoo tests, import tests through the module's test entrypoint, and use the
target branch's frontend test helpers. An ordinary Python syntax check cannot load an Odoo registry.

[Bundled Owl source](https://github.com/odoo/odoo/blob/a157617c921669c5c036509b341be6a07ad1069d/addons/web/static/lib/owl/owl.js) · [Native test classes](https://github.com/odoo/odoo/blob/a157617c921669c5c036509b341be6a07ad1069d/odoo/tests/common.py)

## Native runtime checks

Use [native Odoo testing](native-odoo-testing.md) for disposable database tests and real UI
workflows, including series-specific schema checks, test discovery and persisted reconciliation.
