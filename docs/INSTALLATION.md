# Installation, discovery and rollback

Run commands from the kit root with Python 3.10+. Specify an existing project explicitly.
The default is a read-only preview. --apply copies only skills/primacy-engineering.

| Client | Project destination | Local status |
|---|---|---|
| Codex | .agents/skills/primacy-engineering | CLI discovery/planning tested |
| Antigravity | .agents/skills/primacy-engineering | Native skill/playbook reads tested using scoped launcher |
| Claude Code | .claude/skills/primacy-engineering | CLI discovery/planning tested |

Use python3 adapters/install.py --project /absolute/project --client CLIENT for preview,
then repeat with --apply after reviewing the destination. A collision returns a nonzero
exit code, including the second attempt to install the shared Codex/Antigravity view.
The installer refuses symlinked destination components and never overwrites a skill.
It assumes the selected project is trusted and no hostile process is concurrently replacing
its parent directories. A failed copy can leave a partial install for manual review.

Open the target project in each actual client surface. Ask it to list/read primacy-engineering
and select the debugging playbook for a harmless fictional bug. Record client version,
project, files actually read, selected routes and output. Restart/reload using the client's
supported UI if needed. Copy success alone is CREATED. Mark DISCOVERED only after observation.
A real task and evidence are required for FUNCTIONALLY_VERIFIED. Never weaken permissions.

For updates, compare the canonical diff first. Back up the installed folder into a private,
timestamped directory, record hashes and review any local edits. Move the old copy aside
only with authorization, then install the approved replacement. Restore the backup if
validation fails. A manual update preserves the backup until the new workflow is accepted.
For uninstall, inspect the exact installed directory and move only that copy to the backup
location. The shared Codex/Antigravity copy serves both clients. No global edits need rollback.
Generated views are disposable copies. Make changes in the canonical source, then repeat
the reviewed update process. Future adapters must declare discovery path, copy/link support,
metadata, permissions, tool availability and a harmless discovery test before activation.

Official references consulted for the adapter shape on 15 November 2026.

- [Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Antigravity skills](https://antigravity.google/docs/skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills)

For headless Antigravity planning use adapters/antigravity/run.py as described in the
[adapter guide](../adapters/antigravity/README.md). The session-only read_file grant fixes
the earlier command-permission issue without authorizing shell execution.
