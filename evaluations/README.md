# Behavioral evaluation

These are fictional response-quality cases. They test routing, task-specific next actions,
permission boundaries and truthful evidence status. They do not execute ERP transactions,
load tests, releases or live tenant isolation checks.

Use a separate temporary project containing only the installed router, references, assets
and client metadata. Do not place the answer catalog, source registry, previous responses,
application data or tests in that project. Keep expected answers in the runner repository.

From the kit root, create a fresh fixture, then run the authorized live clients against it.

```sh
python3 evaluations/prepare_fixture.py /absolute/fixture
python3 evaluations/run.py --project /absolute/fixture --output /private/evidence/run-1 --workers 4
```

The defaults evaluate all 54 cases in both clients, six cases per fresh session. The prompt
contains opaque numeric case labels and requests, without expected routes or answers.
Batched responses are context-shared within a six-case session and therefore do not establish
fully independent single-case performance. Codex may use simple cat/sed reads because its native local file entrypoint is its
read-only shell tool; Antigravity uses native file-reading tools. No application commands
or ERP actions are permitted. The process limit is four and each invocation
has a fixed timeout. The runner never silently retries or overwrites evidence. Use a new
output directory and --cases CASE_ID for targeted reruns. Each case consumes real client
usage. Obtain authorization before running paid services or sending sensitive data.

Raw stdout/stderr may include local paths, account diagnostics and tool traces. Store them
outside Git. Publish only reviewed final responses, structural evidence, usage where exposed,
case IDs and reviewer decisions. Retain failures. A parsed response is not automatically PASS.
Review against route intent, task-specific output, safety and truthful status. Accept a
relevant supporting route or an overlapping primary only with a recorded reason. Record
missing output, permission denials, answer-key access and timeouts as failed or invalid.

Antigravity uses adapters/antigravity/run.py, which grants read_file only to the installed
skill directory for that session. It does not grant shell commands or change saved settings.
