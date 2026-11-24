# Antigravity adapter

Install the canonical project skill using the shared installer described in
[installation and rollback](../../docs/INSTALLATION.md). Codex and Antigravity share one
.agents/skills/primacy-engineering entry.

For read-only planning through headless Antigravity, use this scoped launcher from the kit root.

```sh
python3 adapters/antigravity/run.py --project /absolute/project "Review our fictional workflow"
```

The launcher uses plan mode, sandboxing and a session-only read_file permission for the exact
installed skill directory. It asks the client to use file-reading tools. Shell commands,
MCP tools, browser access and business writes receive no new permission. Existing deny/ask
rules retain precedence. No global settings are changed and no backup is needed for a
session-only setting. The installed skill itself follows the normal installer backup rules.

If another operation requires approval, use the interactive client or authorize that exact
operation separately. The launcher captures stream events and returns nonzero for a missing/empty answer, even
if the client exits zero. Permission diagnostics are retained on stderr. See [behavioral evaluation](../../evaluations/README.md) for the test scope.

[Official permission rules](https://antigravity.google/docs/permissions?tab=cli)
