# performance

Profile and improve measured latency or resource use.

## Trigger and boundary

Use for requests such as “Reduce a slow stock report query”. Select another route for unrelated work. This route supplies procedures and grants no runtime permissions.

## Required context

Reproducible workload, authorized target, latency/query baseline. Identify the exact version, edition and installed module set when Odoo is involved. Read only authorized files and use installed, approved tools. If a required runtime or service is unavailable, complete safe local preparation and record NOT_RUN or BLOCKED.

## Workflow

Measure the actual bottleneck before edits. Inspect ORM batching, query counts, indexes, cache scope, locks and payload sizes. Use existing profilers. Change one measured cause. Compare representative load and concurrent behavior while preserving security and business totals.

## Output and validation

Before/after timing/query counts and correctness checks. Use [task and evidence templates](../assets/task-evidence.md). Preserve unresolved questions and distinguish static source evidence from live behavior. Reuse existing test recipes after verifying their scope and current revision.

## Version-specific procedures

Establish [Odoo 19](odoo-19.md) or [Odoo 20](odoo-20.md), then read addon and orm in [the change procedures](odoo-workflows.md). Select relevant upstream metadata through [source selection](sources.md).
