# functional

Configure and validate Odoo business workflows.

## Trigger and boundary

Use for requests such as “Verify a purchase return and supplier credit”. Select another route for unrelated work. This route supplies procedures and grants no runtime permissions.

## Required context

Installed apps, company, role, warehouse, localization, currency. Identify the exact version, edition and installed module set when Odoo is involved. Read only authorized files and use installed, approved tools. If a required runtime or service is unavailable, complete safe local preparation and record NOT_RUN or BLOCKED.

## Workflow

Trace the current document lifecycle and configuration. Draft a change preview and synthetic UAT. Obtain approval for configuration writes and transactions. Reconcile resulting stock, balances and taxes using independently approved expected values.

## Output and validation

Preconditions, inputs, expected and actual business result, evidence and functional reviewer. Use [task and evidence templates](../assets/task-evidence.md). Preserve unresolved questions and distinguish static source evidence from live behavior. Reuse existing test recipes after verifying their scope and current revision.

## Version-specific procedures

Establish [Odoo 19](odoo-19.md) or [Odoo 20](odoo-20.md), then read migration and release, native tests and qa in [the change procedures](odoo-workflows.md). Select relevant upstream metadata through [source selection](sources.md).

## Local browser and contract checks

Use [the local test recipes](local-contracts.md) when changing page scope, functional guidance,
AI routing, execution confirmation or MCP contracts. These reuse explicitly selected Primacy
source and synthetic data. Passing fixture checks does not establish native Odoo ACLs,
transaction correctness, live MCP authorization or client discovery.

## Native runtime checks

Use [native Odoo testing](native-odoo-testing.md) for disposable database tests and real UI
workflows, including series-specific schema checks, test discovery and persisted reconciliation.
