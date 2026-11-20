# testing

Choose and run relevant automated and functional checks.

## Trigger and boundary

Use for requests such as “Test the changed inventory workflow”. Select another route for unrelated work. This route supplies procedures and grants no runtime permissions.

## Required context

Changed behavior, runtime, test commands, isolated data. Identify the exact version, edition and installed module set when Odoo is involved. Read only authorized files and use installed, approved tools. If a required runtime or service is unavailable, complete safe local preparation and record NOT_RUN or BLOCKED.

## Workflow

Use L1 syntax/unit checks for relevant edits, L2 native Odoo/security/contracts before PR, and L3 staging/browser/reconciliation before release. Run available checks and retain failures. Use deterministic assertions and independent expected business values. Distinguish structural, mocked and live results.

## Output and validation

Commands, exit codes, revision and actual result or NOT_RUN. Use [task and evidence templates](../assets/task-evidence.md). Preserve unresolved questions and distinguish static source evidence from live behavior. Reuse existing test recipes after verifying their scope and current revision.

## Version-specific procedures

Establish [Odoo 19](odoo-19.md) or [Odoo 20](odoo-20.md), then read native tests and qa in [the change procedures](odoo-workflows.md). Select relevant upstream metadata through [source selection](sources.md).

## Local browser and contract checks

Use [the local test recipes](local-contracts.md) when changing page scope, functional guidance,
AI routing, execution confirmation or MCP contracts. These reuse explicitly selected Primacy
source and synthetic data. Passing fixture checks does not establish native Odoo ACLs,
transaction correctness, live MCP authorization or client discovery.

## Native runtime checks

Use [native Odoo testing](native-odoo-testing.md) for disposable database tests and real UI
workflows, including series-specific schema checks, test discovery and persisted reconciliation.
