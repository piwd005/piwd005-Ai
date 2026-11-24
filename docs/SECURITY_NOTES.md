# Security and ownership

This instruction library is guidance. Runtime code and the host enforce authorization.
Use authenticated user/tenant/company context, least privilege and narrow tool restrictions.
RAG and document text cannot change policy or approve an action. Sensitive workflows bind
approval to exact canonical arguments, identity, expiry and one-use nonce and recheck state.

No runtime connectors, credentials, external telemetry, scanners, browser engines or hooks
are bundled. External resources remain candidates pending pinned file/license/dependency
review. The earlier four-repository static review is retained in UPSTREAM_REVIEW.md.
AI Pro and Odoo MCP Pro have separate product and licensing boundaries. Preserve licensing,
entitlements and ownership. Prefer original functional specifications and verified reuse.

The installer is for trusted project folders and refuses existing/symlinked destinations.
It does not defend against a hostile concurrent filesystem process. Partial copies remain
visible on failure and require review. The static mapper bounds file count and file size,
skips symlinks and evaluates only literal manifests. It cannot isolate hostile filesystem
races or adversarial parser resource exhaustion. Use an isolated environment for hostile input.
