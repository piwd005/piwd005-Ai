# release

Prepare approved PiCloud or existing pipeline releases.

## Trigger and boundary

Use for requests such as “Prepare a PriERP release review”. Select another route for unrelated work. This route supplies procedures and grants no runtime permissions.

## Required context

Verified interface, target, revision, approval, database/filestore backups. Identify the exact version, edition and installed module set when Odoo is involved. Read only authorized files and use installed, approved tools. If a required runtime or service is unavailable, complete safe local preparation and record NOT_RUN or BLOCKED.

## Workflow

Inspect the actual pipeline. Rehearse staging and verify restore of database plus filestore. Record rollback compatibility, migration limits, smoke checks and monitoring thresholds. Obtain production authorization for the concrete release. Verify deployed revision and business smoke outcomes.

## Output and validation

Release evidence, restore result and rollback decision. Use [task and evidence templates](../assets/task-evidence.md). Preserve unresolved questions and distinguish static source evidence from live behavior. Reuse existing test recipes after verifying their scope and current revision.
