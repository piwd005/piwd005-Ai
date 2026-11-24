# claude-code adapter

Run `python3 adapters/install.py --project /absolute/project --client claude-code` from the
kit root for preview. Add --apply after reviewing it. Read [installation and rollback](../../docs/INSTALLATION.md)
for the shared-directory conflict rule and actual-client discovery protocol.
The adapter copies the canonical source. It registers no MCP tools and grants no permissions.
Status is CREATED for copied files. Live discovery and functional verification remain NOT_RUN.
