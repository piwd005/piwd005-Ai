# security

Review an authorized change or system for security.

## Trigger and boundary

Use for requests such as “Review a public Odoo controller”. Select another route for unrelated work. This route supplies procedures and grants no runtime permissions.

## Required context

Target authorization, threat model, data classes, affected surfaces. Identify the exact version, edition and installed module set when Odoo is involved. Read only authorized files and use installed, approved tools. If a required runtime or service is unavailable, complete safe local preparation and record NOT_RUN or BLOCKED.

## Workflow

Trace auth and effective identity. Review record/company isolation, portal ownership, CSRF, injections, uploads, secrets, dependencies and hooks. Assess scanner matches in context. Use scoped synthetic tests. Prioritize exploitable findings with paths, preconditions and remediation.

## Output and validation

Reproducible findings and verified remediation limits. Use [task and evidence templates](../assets/task-evidence.md). Preserve unresolved questions and distinguish static source evidence from live behavior. Reuse existing test recipes after verifying their scope and current revision.

## Version-specific procedures

Establish [Odoo 19](odoo-19.md) or [Odoo 20](odoo-20.md), then read access and controllers in [the change procedures](odoo-workflows.md). Select relevant upstream metadata through [source selection](sources.md).
