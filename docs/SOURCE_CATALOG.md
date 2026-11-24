# Primacy skill and resource catalog v2

Prepared 15 November 2026. This is a curated reference inventory, not an installation list.
All upstream execution_approved and installed flags remain false. No third-party skill bodies
or application code are bundled. Counts include documentation/license pages as well as tools.

## Role profiles

### developer
Local development and approved isolated tests; live systems require separate authorization.
Routes: requirements, codebase-map, reuse-first, odoo-backend, odoo-ui, python-api, testing, debugging, performance

### functional
Read-only analysis by default; preview every configuration/import change and obtain scoped approval.
Routes: functional, requirements, migration, testing, training-docs

### ai-engineer
Development-only sandbox; never inherit client-wide business permissions.
Routes: ai-rag, mcp, security, agent-product-evaluation, testing, optimization

### sales-support
Drafts and authorized read-only information. No discount, promise, outreach or customer data write without approval.
Routes: sales-presales, customer-support, training-docs, functional

### delivery-security
Evidence/release preparation; deployment authority is separate and transaction-specific.
Routes: project-delivery, release, security, testing, performance

### maintainer
Candidate review and proposed changes only; no automatic trust promotion.
Routes: skill-maintenance, knowledge, optimization

## 24 intent routes

| Route | Purpose | Playbook |
|---|---|---|
| `requirements` | Requirements, fit-gap, planning and task breakdown | `references/requirements.md` |
| `functional` | Odoo configuration and business-process UAT | `references/odoo-functional.md` |
| `odoo-backend` | Odoo models, ORM, controllers and security | `references/odoo-development.md` |
| `odoo-ui` | OWL, XML views, QWeb and portal behavior | `references/odoo-development.md` |
| `migration` | Master data, addon upgrades and reconciliations | `references/migration.md` |
| `python-api` | Python services, APIs, transactions and background work | `references/python-api.md` |
| `ai-rag` | PriERP/PiCloud agents, retrieval and evaluations | `references/ai-rag.md` |
| `mcp` | MCP tools, adapters, identity and authorization | `references/mcp-guardrails.md` |
| `security` | Threat modeling, guardrails and authorized security review | `references/cybersecurity.md` |
| `testing` | Test planning, regression and browser evidence | `references/testing-debugging.md` |
| `debugging` | Reproduction, root cause and minimal fix | `references/testing-debugging.md` |
| `reference-analysis` | Authorized feature discovery and clean-room specifications | `references/reference-analysis.md` |
| `release` | PiCloud staging, backup, restore and release review | `references/delivery-picloud.md` |
| `project-delivery` | Odoo tasks, handoffs, client status and hypercare | `references/delivery-picloud.md` |
| `knowledge` | Product context, evidence, knowledge refresh and reuse | `references/knowledge-cost.md` |
| `optimization` | Measured token, effort and iteration optimization | `references/knowledge-cost.md` |
| `codebase-map` | Understand unfamiliar Odoo code, trace overrides and impact | `references/codebase-understanding.md` |
| `reuse-first` | Select configuration, existing components or the smallest new change | `references/solution-selection.md` |
| `sales-presales` | Discovery, fit-gap, demo, scope and proposal drafts | `references/sales-presales.md` |
| `customer-support` | Triage, approved support actions, communication and regression capture | `references/support-operations.md` |
| `training-docs` | Role-based training, handover, process and user guide drafts | `references/training-docs.md` |
| `performance` | Profile measured latency, query volume and resource use | `references/performance.md` |
| `skill-maintenance` | Research, review, pin, evaluate and update skill candidates | `references/skill-governance.md` |
| `agent-product-evaluation` | Evaluate Odoo AI products and independent PriERP implementation options | `references/agent-product-evaluation.md` |

## Research sources and decisions

Earlier 43 sources are retained from v0.1; not every earlier URL was re-audited in v0.2.
All selected code, hooks, licences and compatibility must be reviewed at a pinned revision.

### agent-skills - Agent Skills specification
Source: https://agentskills.io/specification
Type/provenance: standard. Decision: foundation.
Portable SKILL.md structure and progressive loading.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### codex-skills - OpenAI: Build skills
Source: https://learn.chatgpt.com/docs/build-skills
Type/provenance: official. Decision: foundation.
Codex discovery, metadata and skill distribution.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### codex-customization - OpenAI: Customization
Source: https://learn.chatgpt.com/docs/customization/overview
Type/provenance: official. Decision: foundation.
AGENTS.md, skills and tool integration boundaries.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### codex-security - OpenAI: Agent approvals and security
Source: https://learn.chatgpt.com/docs/agent-approvals-security
Type/provenance: official. Decision: foundation.
Runtime sandbox and approvals; not replaceable by prompts.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### openai-plugins - OpenAI plugin examples
Source: https://github.com/openai/plugins
Type/provenance: official-repository. Decision: selective.
Optional OpenAI-specific distribution packaging.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### openai-skills-legacy - OpenAI legacy skills catalog
Source: https://github.com/openai/skills
Type/provenance: official-repository. Decision: legacy-reference.
README marks repository deprecated and points to openai/plugins.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### antigravity-skills - Google Antigravity: Agent skills
Source: https://antigravity.google/docs/skills
Type/provenance: official. Decision: foundation.
Current .agents/skills discovery; legacy .agent/skills compatibility.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### claude-skills - Claude Code: Skills
Source: https://code.claude.com/docs/en/skills
Type/provenance: official. Decision: foundation.
Claude-specific directory, invocation and runtime extensions.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### anthropic-skills - Anthropic skill examples
Source: https://github.com/anthropics/skills
Type/provenance: official-repository. Decision: selective.
Selected mcp-builder, webapp-testing and skill-creator patterns.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### odoo-security - Odoo 19 security
Source: https://www.odoo.com/documentation/19.0/developer/reference/backend/security.html
Type/provenance: official. Decision: foundation.
Access controls, record rules and unsafe security bypasses.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### odoo-testing - Odoo 19 testing
Source: https://www.odoo.com/documentation/19.0/developer/reference/backend/testing.html
Type/provenance: official. Decision: foundation.
Native ORM, HTTP and version-specific frontend tests.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### odoo-json2 - Odoo 19 External JSON-2 API
Source: https://www.odoo.com/documentation/19.0/developer/reference/external_api.html
Type/provenance: official. Decision: foundation.
Database-specific APIs, ACLs and per-call transaction boundaries.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### odoo20-docs - Odoo 20 documentation
Source: https://www.odoo.com/documentation/20.0/
Type/provenance: official. Decision: version-specific.
Version-specific starting point; do not mix versions.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### odoo20-tests - Odoo 20 testing
Source: https://www.odoo.com/documentation/20.0/developer/reference/backend/testing.html
Type/provenance: official. Decision: version-specific.
Verify against the target Odoo branch and installed build.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### odoo-ai - Odoo 19 AI
Source: https://www.odoo.com/documentation/19.0/applications/productivity/ai.html
Type/provenance: official. Decision: reference.
Documented reference capabilities; not a code-copy license.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### odoo-ai-agents - Odoo 19 AI agents
Source: https://www.odoo.com/documentation/19.0/applications/productivity/ai/agents.html
Type/provenance: official. Decision: reference.
Reference-agent workflows; verify edition and installed modules.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### odoo-module - Odoo 19 module tutorial
Source: https://www.odoo.com/documentation/19.0/developer/tutorials/backend.html
Type/provenance: official. Decision: foundation.
Addon development reference.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### odoo-skills - mart337i/odoo-skills
Source: https://github.com/mart337i/odoo-skills
Type/provenance: community. Decision: SELECTIVE_REFERENCE_PENDING_LICENSE.
Odoo development, tracing, review, testing, OWL and migration playbooks.
Admission note: Not established from inspected README/root listing; confirm applicable package/file license before vendoring. Use original Primacy workflow until cleared.
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### oca-hooks - OCA Odoo pre-commit hooks
Source: https://github.com/OCA/odoo-pre-commit-hooks
Type/provenance: specialist-community. Decision: pilot.
Odoo addon checks complementary to pylint-odoo.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### oca-pylint - OCA pylint-odoo
Source: https://github.com/OCA/pylint-odoo
Type/provenance: specialist-community. Decision: pilot.
Odoo-aware Python static checks.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### oca-openupgrade - OCA OpenUpgrade
Source: https://github.com/OCA/OpenUpgrade
Type/provenance: specialist-community. Decision: migration-only.
Migration tooling; verify branch and per-module coverage.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### playwright-cli - Microsoft Playwright CLI
Source: https://github.com/microsoft/playwright-cli
Type/provenance: official-repository. Decision: pilot.
Compact browser actions and coding-agent workflows.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### playwright-mcp - Microsoft Playwright MCP
Source: https://github.com/microsoft/playwright-mcp
Type/provenance: official-repository. Decision: optional.
Interactive browser investigation; enable only when needed.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### mcp-python - Official MCP Python SDK
Source: https://github.com/modelcontextprotocol/python-sdk
Type/provenance: official-repository. Decision: pilot.
Candidate SDK for a Primacy-owned MCP gateway.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### mcp-security - MCP security best practices (versioned)
Source: https://modelcontextprotocol.io/specification/latest/basic/security_best_practices
Type/provenance: official. Decision: foundation.
Confused deputy, token passthrough, SSRF and session threats; verify negotiated protocol.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### agents-guardrails - OpenAI Agents SDK guardrails
Source: https://openai.github.io/openai-agents-python/guardrails/
Type/provenance: official. Decision: reference.
Input/output/tool boundaries and blocking versus parallel execution.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### owasp-asvs - OWASP ASVS
Source: https://asvs.owasp.org/
Type/provenance: security-standard. Decision: foundation.
Web application security verification requirements.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### owasp-agentic - OWASP Agentic Applications Top 10
Source: https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/
Type/provenance: security-standard. Decision: foundation.
Threat-model baseline for agentic applications.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### trailofbits - Trail of Bits skills
Source: https://github.com/trailofbits/skills
Type/provenance: security-specialist. Decision: license-review-before-reuse.
Selected audit-context-building, differential-review and insecure-defaults workflows; CC-BY-SA-4.0 shown.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### gitleaks - Gitleaks
Source: https://github.com/gitleaks/gitleaks
Type/provenance: maintainer-repository. Decision: pilot.
Secrets scanning; redact findings before model ingestion.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### pip-audit - PyPA pip-audit
Source: https://github.com/pypa/pip-audit
Type/provenance: official-repository. Decision: pilot.
Known Python dependency vulnerability checks; no automatic dependency upgrade.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### semgrep - Semgrep
Source: https://github.com/semgrep/semgrep
Type/provenance: maintainer-repository. Decision: selective.
Static analysis; review selected rules, licenses and telemetry.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### ruff - Astral Ruff
Source: https://github.com/astral-sh/ruff
Type/provenance: maintainer-repository. Decision: pilot.
Fast Python lint and format checks, complementary to Odoo checks.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### uv - Astral uv
Source: https://github.com/astral-sh/uv
Type/provenance: maintainer-repository. Decision: optional.
Reproducible isolated Python environments.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### superpowers - obra/superpowers
Source: https://github.com/obra/superpowers
Type/provenance: community. Decision: selective-not-full-install.
Selected systematic-debugging, TDD and verification-before-completion workflows.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### spec-kit - GitHub Spec Kit
Source: https://github.com/github/spec-kit
Type/provenance: official-repository. Decision: optional.
Specification-led planning for substantial features; not every tiny fix.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### context7 - Upstash Context7
Source: https://github.com/upstash/context7
Type/provenance: maintainer-repository. Decision: optional-privacy-review.
Optional documentation retrieval; official versioned docs remain authoritative.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### promptfoo - Promptfoo
Source: https://github.com/promptfoo/promptfoo
Type/provenance: maintainer-repository. Decision: optional.
Agent and RAG evaluation; review data egress and paid dependencies.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### rea - morluto/rea
Source: https://github.com/morluto/rea
Type/provenance: community. Decision: optional.
Authorized reference-app analysis; do not activate heavyweight toolchains by default.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### rea-install - REA installation documentation
Source: https://github.com/morluto/rea/blob/main/docs/getting-started/installation.md
Type/provenance: maintainer-documentation. Decision: reference.
Lists Codex, Antigravity and Claude Code client setup identifiers.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### reverse-skill - zhaoxuya520/reverse-skill
Source: https://github.com/zhaoxuya520/reverse-skill
Type/provenance: community. Decision: disabled-by-default.
Optional scoped investigation; dependencies have their own licenses.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### odoo-mcp-pro - pantalytics/odoo-mcp-pro
Source: https://github.com/pantalytics/odoo-mcp-pro
Type/provenance: community-commercial. Decision: blocked-for-client-hosting-pending-review.
Mixed MPL-2.0 and Elastic License 2.0; hosted-client use needs licensing review.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### ecc - affaan-m/ECC
Source: https://github.com/affaan-m/ecc
Type/provenance: community. Decision: reference-only.
Optional workflow patterns; do not stack a second competing orchestration system.
Admission note: required before copying, vendoring or production use
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### ponytail - DietrichGebert/ponytail
Source: https://github.com/DietrichGebert/ponytail
Type/provenance: community skill. Decision: SELECTIVE_PILOT.
Minimal complete changes, reuse and focused review.
Admission note: MIT declared in skill and repository; retain notice, audit selected revision and hooks.
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### pan-ai-pro - Pantalytics AI Pro application
Source: https://github.com/pantalytics/pan_ai_pro
Type/provenance: vendor application. Decision: REFERENCE_ONLY.
Reference behaviors for agents inside Odoo; not an IDE skill.
Admission note: Elastic License 2.0; hosted/managed-service restriction requires commercial clearance before PriERP adoption. No bypass of pairing or entitlement.
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### pan-ai-pro-license - AI Pro license
Source: https://raw.githubusercontent.com/pantalytics/pan_ai_pro/main/LICENSE
Type/provenance: vendor license. Decision: LICENSE_GATE.
Authoritative license text, distinct from Odoo MCP Pro licensing.
Admission note: Elastic-2.0; preserve notices and review intended use.
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### pan-ai-pro-protocol - AI Pro platform protocol
Source: https://raw.githubusercontent.com/pantalytics/pan_ai_pro/main/docs/protocol.md
Type/provenance: vendor documentation. Decision: REFERENCE_ONLY.
Pairing, heartbeat and entitlement data flows.
Admission note: Do not remove or bypass licensing; review transmitted metadata and provider traffic separately.
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### pan-ai-pro-architecture - AI Pro architecture
Source: https://raw.githubusercontent.com/pantalytics/pan_ai_pro/main/docs/architecture-20.md
Type/provenance: vendor documentation. Decision: REFERENCE_ONLY.
Documented architecture, not an independent runtime/security audit.
Admission note: No protected code or prompt copying into an independent Primacy implementation.
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### fhidalgo-odoo - fhidalgodev/odoo-development-skill
Source: https://github.com/fhidalgodev/odoo-development-skill
Type/provenance: community skill. Decision: SELECTIVE_PILOT.
Code orientation, pattern lookup and version-aware reuse.
Admission note: MIT shown by repository; preserve attribution and upstream lineage, verify selected files. No Enterprise copying or unbounded exhaustive searches.
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### atakh-odoo - atakhadiviom/odoo-skill
Source: https://github.com/atakhadiviom/odoo-skill
Type/provenance: community skill. Decision: REVIEW_FIRST.
Scaffolding and specification/bug workflow examples.
Admission note: README declares LGPL-3; standalone LICENSE fetch returned 404. Confirm applicable terms and file notices before copying; version/support statements need official verification.
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### clawic-odoo - Clawic Odoo workflow
Source: https://github.com/clawic/skills/tree/main/skills/odoo
Type/provenance: community skill. Decision: SELECTIVE_PILOT.
Functional operations and read-before-write workflows.
Admission note: Root MIT license observed; verify per-file terms. Replace global cross-customer memory with scoped Primacy context.
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### clawic-license - Clawic root license
Source: https://raw.githubusercontent.com/clawic/skills/main/LICENSE
Type/provenance: maintainer license. Decision: LICENSE_REFERENCE.
License evidence for selected Clawic content.
Admission note: MIT; attribution and license inclusion required for covered distribution.
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### odoo20-house - Odoo official addon guidelines skill
Source: https://raw.githubusercontent.com/odoo/odoo/20.0/skills/odoo-guidelines/SKILL.md
Type/provenance: official Odoo source. Decision: PRIORITY_REFERENCE.
Version-specific addon engineering source.
Admission note: Inspect repository and file-level licensing before vendoring; source branch is 20.0, not universal guidance.
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### odoo20-web-house - Odoo official web guidelines skill
Source: https://raw.githubusercontent.com/odoo/odoo/20.0/skills/odoo-web-guidelines/SKILL.md
Type/provenance: official Odoo source. Decision: PRIORITY_REFERENCE.
Version-specific OWL, JavaScript, templates and frontend tests.
Admission note: Inspect file-level terms; do not apply version-specific APIs to 19 without verification.
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### odoo20-security-skill - Odoo official security audit skill
Source: https://raw.githubusercontent.com/odoo/odoo/20.0/skills/odoo-security/SKILL.md
Type/provenance: official Odoo source. Decision: PRIORITY_REFERENCE.
Odoo-specific access, injection and controller review.
Admission note: Inspect file-level terms; static guidance is not a proof of security.
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### odoo20-review-skill - Odoo official review skill
Source: https://raw.githubusercontent.com/odoo/odoo/20.0/skills/odoo-review/SKILL.md
Type/provenance: official Odoo source. Decision: PRIORITY_REFERENCE.
Diff review with required sibling guideline references.
Admission note: Preserve sibling references if admitted; verify version and applicable license.
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### odoo-boost - havmedia/odoo-boost
Source: https://github.com/havmedia/odoo-boost
Type/provenance: MCP and skills package. Decision: STAGING_PILOT_ONLY.
Live model/view/access introspection for a staging developer.
Admission note: README declares MIT; standalone LICENSE fetch returned 404. Verify package terms and credentials/config handling; README advertises Odoo 17-19, not verified 20.
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### psae-functional - odoo-ps/psae-ai-infra
Source: https://github.com/odoo-ps/psae-ai-infra
Type/provenance: public functional workflow repository. Decision: REFERENCE_ONLY.
Functional specifications, small-change boundaries and validation ideas.
Admission note: Redistribution permission not established in review; do not vendor. Do not assume Odoo.sh hooks fit PiCloud or Community.
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### omas-superpowers - omas-odoo/odoo-superpowers
Source: https://github.com/omas-odoo/odoo-superpowers
Type/provenance: community workflow pack. Decision: ALTERNATIVE_NOT_DEFAULT.
Alternative Odoo planning, completion and review procedures.
Admission note: License not established in review; do not vendor. Avoid competing orchestrators and automatic self-refinement.
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### pydantic-skills - Pydantic coding-agent skills
Source: https://pydantic.dev/docs/ai/overview/coding-agent-skills/
Type/provenance: official vendor documentation. Decision: OPTIONAL_STACK_MATCH.
Library-aligned AI development skill; use only if the project selects Pydantic AI.
Admission note: Review pydantic/skills file-level licensing and installed library compatibility before use.
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### pydantic-ai - Pydantic AI documentation
Source: https://pydantic.dev/docs/ai/overview/
Type/provenance: official vendor documentation. Decision: OPTIONAL_STACK_MATCH.
Typed agent/tool development reference; not a mandatory framework replacement.
Admission note: Inspect applicable SDK and dependency terms before adopting a runtime.
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.

### github-odoo-search - GitHub Odoo skill discovery query
Source: https://github.com/search?q=odoo+skill&type=repositories
Type/provenance: discovery only. Decision: DISCOVERY_ONLY.
Candidate discovery; never an installation or trust feed. Direct search page was inaccessible in this review.
Admission note: Search results imply no installation, safety or redistribution permission.
State: NOT_INSTALLED; EXECUTION_NOT_APPROVED; PIN_REQUIRED.
