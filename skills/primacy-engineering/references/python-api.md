# python-api

Implement services, API contracts and background work.

## Trigger and boundary

Use for requests such as “Fix duplicate webhook delivery”. Select another route for unrelated work. This route supplies procedures and grants no runtime permissions.

## Required context

Existing entrypoints, authentication, request/response contracts. Identify the exact version, edition and installed module set when Odoo is involved. Read only authorized files and use installed, approved tools. If a required runtime or service is unavailable, complete safe local preparation and record NOT_RUN or BLOCKED.

## Workflow

Reuse existing clients and representations. Validate boundary inputs. Preserve timeout, cancellation and errors. Design idempotency for retries and consistency for partial writes and concurrent workers. Test both normal calls and failures at side-effect boundaries.

For duplicate delivery, establish the actual logical operation key and retry contract.
Do not assume invoice references are unique or introduce constraints from symptoms alone.
Check legitimate repeated references and distinct requests. Verify target-version syntax
and existing APIs before proposing code. Keep unverified fixes conditional.

## Output and validation

Contract tests, retry/concurrency evidence and backward compatibility. Use [task and evidence templates](../assets/task-evidence.md). Preserve unresolved questions and distinguish static source evidence from live behavior. Reuse existing test recipes after verifying their scope and current revision.
