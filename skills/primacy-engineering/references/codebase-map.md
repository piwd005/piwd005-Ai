# codebase-map

Orient an unfamiliar Odoo addon and trace impact.

## Trigger and boundary

Use for requests such as “Map the sales addon before editing”. Select another route for unrelated work. This route supplies procedures and grants no runtime permissions.

## Required context

Authorized source root, relevant addon and revision. Identify the exact version, edition and installed module set when Odoo is involved. Read only authorized files and use installed, approved tools. If a required runtime or service is unavailable, complete safe local preparation and record NOT_RUN or BLOCKED.

## Workflow

Run the bounded static helper when useful. Inspect manifest, imports, entrypoints, models, inheritance, views, actions, ACLs and tests. Trace runtime registrations manually. Record file hashes and verified run recipes. Refresh affected entries after edits.

## Output and validation

Scoped map with unresolved dynamic relationships. Use [task and evidence templates](../assets/task-evidence.md). Preserve unresolved questions and distinguish static source evidence from live behavior. Reuse existing test recipes after verifying their scope and current revision.

## Version-specific procedures

Establish [Odoo 19](odoo-19.md) or [Odoo 20](odoo-20.md), then read addon and orm in [the change procedures](odoo-workflows.md). Select relevant upstream metadata through [source selection](sources.md).
