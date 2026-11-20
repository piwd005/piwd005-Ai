# debugging

Reproduce and fix a confirmed bug.

## Trigger and boundary

Use for requests such as “A retry creates duplicate invoices”. Select another route for unrelated work. This route supplies procedures and grants no runtime permissions.

## Required context

Symptoms, logs with secrets removed, expected behavior, revision. Identify the exact version, edition and installed module set when Odoo is involved. Read only authorized files and use installed, approved tools. If a required runtime or service is unavailable, complete safe local preparation and record NOT_RUN or BLOCKED.

## Workflow

Reproduce through the normal caller. Trace every caller of the shared function. Establish an evidence-backed cause. Apply the smallest complete fix and regression test. After three materially similar failed cycles, summarize attempts and missing evidence before changing approach.

For duplicate delivery, establish the actual logical operation key and retry contract.
Do not assume invoice references are unique or introduce constraints from symptoms alone.
Check legitimate repeated references and distinct requests. Verify target-version syntax
and existing APIs before proposing code. Keep unverified fixes conditional.

Even without source or a runtime, return a concrete reproduction plan and proposed regression
cases alongside missing prerequisites. For duplicate retries, cover sequential and concurrent
replay, a committed operation whose response was lost, distinct operations and legitimately
repeated references. State what should be asserted and keep execution NOT_RUN. A diagnostic
question list alone does not satisfy the debugging deliverable.

## Output and validation

Before/after reproduction and regression results. Use [task and evidence templates](../assets/task-evidence.md). Preserve unresolved questions and distinguish static source evidence from live behavior. Reuse existing test recipes after verifying their scope and current revision.
