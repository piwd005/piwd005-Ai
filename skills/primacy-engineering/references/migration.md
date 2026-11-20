# migration

Plan and execute approved data or addon migration.

## Trigger and boundary

Use for requests such as “Plan an Odoo 19 addon upgrade”. Select another route for unrelated work. This route supplies procedures and grants no runtime permissions.

## Required context

Source/target versions, mapping, volume, backup, staging approval. Identify the exact version, edition and installed module set when Odoo is involved. Read only authorized files and use installed, approved tools. If a required runtime or service is unavailable, complete safe local preparation and record NOT_RUN or BLOCKED.

## Workflow

Map identifiers, relational dependencies, companies and rounding. Rehearse on synthetic or approved staged data. Design idempotent batches and failed-row recovery. Compare counts, totals and references before/after. Require scoped approval before writes and a tested rollback.

An upgrade plan must name failed-row isolation/recovery, repeatable batches, rollback and
restore limits alongside rehearsal and reconciliation. Identify what can be rolled back
without losing new transactions, and what requires restoration of database plus filestore.
Do not imply the static mapper proves version/API compatibility. It supplies source metadata;
compatibility requires target-version source review and native install/upgrade checks.

## Output and validation

Rehearsal, reconciliation, rejected rows and restore limits. Use [task and evidence templates](../assets/task-evidence.md). Preserve unresolved questions and distinguish static source evidence from live behavior. Reuse existing test recipes after verifying their scope and current revision.

## Version-specific procedures

Establish [Odoo 19](odoo-19.md) or [Odoo 20](odoo-20.md), then read migration and release in [the change procedures](odoo-workflows.md). Select relevant upstream metadata through [source selection](sources.md).
