# Odoo 20 engineering reference

Use for an explicitly established 20.0 target. The Community source baseline is commit
d032c6dc504a24de4084783d8abb1b95896f1eda, inspected 15 November 2026. Check the installed build, edition and customization set
before using a source API. The official 20.0 addon and web guidelines exist at this pin.
Their corresponding 19.0 paths were unavailable during review, so no shared-path assumption
is made. This file contains original Primacy guidance and links to the reviewed sources.

## Backend and version boundaries

Use the source-matched models.Constraint, models.Index and, where genuinely required,
models.UniqueIndex definitions. Check current data and the exact database invariant first.
Preserve recordset/batch behavior, inheritance and transaction ownership. Omitted-field,
import/API, company access and upgrade tests remain necessary for field validation changes.
The inspected upstream guideline warns against relying on legacy _sql_constraints in its
newer code. Verify the actual target source and installed migration behavior before converting
legacy declarations. Treat a grep match as a migration candidate, not permission to drop a constraint.

[Database objects](https://github.com/odoo/odoo/blob/d032c6dc504a24de4084783d8abb1b95896f1eda/odoo/orm/table_objects.py) · [ORM guidance](https://github.com/odoo/odoo/blob/d032c6dc504a24de4084783d8abb1b95896f1eda/skills/odoo-guidelines/guidelines/orm.md)

## HTTP differences

At this pin, odoo.http is a package. Its public exports come from package modules, including
routing_map. Avoid depending on private implementation paths copied from 19.0. The official
controller guidance includes http, jsonrpc and json2 route types and requires bearer_scope
for bearer authentication. Inspect the actual routing module and current endpoint contract
before defining one. Do not mechanically change auth, request type, read-only flags or CSRF
behavior on an inherited route. Verify anonymous, authenticated and denied-record requests.

[Public HTTP exports](https://github.com/odoo/odoo/blob/d032c6dc504a24de4084783d8abb1b95896f1eda/odoo/http/__init__.py) · [Controller guidance](https://github.com/odoo/odoo/blob/d032c6dc504a24de4084783d8abb1b95896f1eda/skills/odoo-guidelines/guidelines/controllers.md)

## Owl 3 boundary

The official 20.0 web guidance targets Owl 3. New code should follow that branch's reactive
primitives and hook semantics. The guide documents useEffect as dependency-tracked and
useOnChange for an explicitly tracked dependency function. It identifies useState, useRef
and static props as removed Owl 2 APIs and lists other compatibility hooks to avoid in new
code. Inspect the exact installed component/library before migrating an existing extension.
Do not convert nearby unaffected code simply because it uses an older compatibility layer.

Trace registry/service extension points before patching framework code. Exercise unmount and
cancellation, stale requests, keyboard/focus behavior, labels, escaped text and responsive
layout. Resolve assets and test helpers from the target branch, including Hoot patterns where
that branch uses them. Native TransactionCase and HttpCase exist at the reviewed pin.

[Version-matched web rules](https://github.com/odoo/odoo/blob/d032c6dc504a24de4084783d8abb1b95896f1eda/skills/odoo-web-guidelines/SKILL.md) · [Hook semantics](https://github.com/odoo/odoo/blob/d032c6dc504a24de4084783d8abb1b95896f1eda/skills/odoo-web-guidelines/guidelines/javascript.md) · [Native tests](https://github.com/odoo/odoo/blob/d032c6dc504a24de4084783d8abb1b95896f1eda/odoo/tests/common.py)

## Upgrade acceptance

Use the [shared migration procedure](odoo-workflows.md#migration-and-release). A source map
and static linters cannot establish that a 19.0 addon installs, upgrades or behaves correctly
on 20.0. Require a source-matched registry test, affected UI and access checks, and independently
approved business reconciliation in staging before calling that migration verified.

## Native runtime checks

Use [native Odoo testing](native-odoo-testing.md) for disposable database tests and real UI
workflows, including series-specific schema checks, test discovery and persisted reconciliation.
