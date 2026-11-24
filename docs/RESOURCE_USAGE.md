# Resource usage

All 62 supplied resources are present in the portable generated source index and mapped to
24 routes. The source selector reads only relevant route/version metadata. Its inclusion
confers no runtime execution permission. The canonical registry remains the source of truth.

The original Primacy core has no third-party Python imports. Five QA tools have external CLI
adapters and were tested in an isolated local environment. No tool wheels/binaries or upstream
skill/application bodies are bundled. QA dependencies are optional and are never auto-installed.
Odoo 19/20 guidance links to inspected, pinned Community source. Native runtime compatibility
still requires tests on the target deployment. Other catalog entries retain their admission
status and need selected-file review before code reuse or execution.

| Resource | Admission | Actual use |
|---|---|---|
| agent-skills | REFERENCE_VERIFIED | Reference metadata, loaded on demand |
| codex-skills | REFERENCE_VERIFIED | Reference metadata, loaded on demand |
| codex-customization | REFERENCE_VERIFIED | Reference metadata, loaded on demand |
| codex-security | REFERENCE_VERIFIED | Reference metadata, loaded on demand |
| openai-plugins | CANDIDATE | Reference metadata, loaded on demand |
| openai-skills-legacy | CANDIDATE | Reference metadata, loaded on demand |
| antigravity-skills | REFERENCE_VERIFIED | Reference metadata, loaded on demand |
| claude-skills | REFERENCE_VERIFIED | Reference metadata, loaded on demand |
| anthropic-skills | CANDIDATE | Reference metadata, loaded on demand |
| odoo-security | CANDIDATE | Reference metadata, loaded on demand |
| odoo-testing | CANDIDATE | Reference metadata, loaded on demand |
| odoo-json2 | CANDIDATE | Reference metadata, loaded on demand |
| odoo20-docs | REVIEWED_REFERENCE | Reference metadata, loaded on demand |
| odoo20-tests | CANDIDATE | Reference metadata, loaded on demand |
| odoo-ai | CANDIDATE | Reference metadata, loaded on demand |
| odoo-ai-agents | CANDIDATE | Reference metadata, loaded on demand |
| odoo-module | REVIEWED_REFERENCE | Reference metadata, loaded on demand |
| odoo-skills | REVIEWED_REFERENCE | Reference metadata, loaded on demand |
| oca-hooks | QA_CLI_ADMITTED | External QA CLI adapter |
| oca-pylint | QA_CLI_ADMITTED | External QA CLI adapter |
| oca-openupgrade | CANDIDATE | Reference metadata, loaded on demand |
| playwright-cli | CANDIDATE | Reference metadata, loaded on demand |
| playwright-mcp | CANDIDATE | Reference metadata, loaded on demand |
| mcp-python | CANDIDATE | Reference metadata, loaded on demand |
| mcp-security | CANDIDATE | Reference metadata, loaded on demand |
| agents-guardrails | CANDIDATE | Reference metadata, loaded on demand |
| owasp-asvs | CANDIDATE | Reference metadata, loaded on demand |
| owasp-agentic | CANDIDATE | Reference metadata, loaded on demand |
| trailofbits | CANDIDATE | Reference metadata, loaded on demand |
| gitleaks | QA_CLI_ADMITTED | External QA CLI adapter |
| pip-audit | QA_CLI_ADMITTED | External QA CLI adapter |
| semgrep | CANDIDATE | Reference metadata, loaded on demand |
| ruff | QA_CLI_ADMITTED | External QA CLI adapter |
| uv | CANDIDATE | Reference metadata, loaded on demand |
| superpowers | CANDIDATE | Reference metadata, loaded on demand |
| spec-kit | CANDIDATE | Reference metadata, loaded on demand |
| context7 | CANDIDATE | Reference metadata, loaded on demand |
| promptfoo | CANDIDATE | Reference metadata, loaded on demand |
| rea | REVIEWED_REFERENCE | Reference metadata, loaded on demand |
| rea-install | CANDIDATE | Reference metadata, loaded on demand |
| reverse-skill | REVIEWED_REFERENCE | Reference metadata, loaded on demand |
| odoo-mcp-pro | REVIEWED_REFERENCE | Reference metadata, loaded on demand |
| ecc | CANDIDATE | Reference metadata, loaded on demand |
| ponytail | CANDIDATE | Reference metadata, loaded on demand |
| pan-ai-pro | CANDIDATE | Reference metadata, loaded on demand |
| pan-ai-pro-license | CANDIDATE | Reference metadata, loaded on demand |
| pan-ai-pro-protocol | CANDIDATE | Reference metadata, loaded on demand |
| pan-ai-pro-architecture | CANDIDATE | Reference metadata, loaded on demand |
| fhidalgo-odoo | CANDIDATE | Reference metadata, loaded on demand |
| atakh-odoo | CANDIDATE | Reference metadata, loaded on demand |
| clawic-odoo | CANDIDATE | Reference metadata, loaded on demand |
| clawic-license | CANDIDATE | Reference metadata, loaded on demand |
| odoo20-house | REVIEWED_REFERENCE | Reference metadata, loaded on demand |
| odoo20-web-house | REVIEWED_REFERENCE | Reference metadata, loaded on demand |
| odoo20-security-skill | CANDIDATE | Reference metadata, loaded on demand |
| odoo20-review-skill | CANDIDATE | Reference metadata, loaded on demand |
| odoo-boost | CANDIDATE | Reference metadata, loaded on demand |
| psae-functional | CANDIDATE | Reference metadata, loaded on demand |
| omas-superpowers | CANDIDATE | Reference metadata, loaded on demand |
| pydantic-skills | CANDIDATE | Reference metadata, loaded on demand |
| pydantic-ai | CANDIDATE | Reference metadata, loaded on demand |
| github-odoo-search | CANDIDATE | Reference metadata, loaded on demand |

## Release 0.3.0 local contract admission

MCP Python SDK 2.3.0 is now verified for an optional synthetic stdio fixture, with artifact
hashes and dependency audit in assets/contracts/provenance.json. Playwright 1.65.1 library
is used as an external local browser test tool; this does not admit playwright-cli or
playwright-mcp servers. See STEPS_4_5_REPORT.md. No catalog entry grants runtime permissions.
