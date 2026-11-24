# Actual client checks — 15 November 2026

Latest full-case results and permission remediation are recorded in [FULL_EVALUATION_REPORT.md](FULL_EVALUATION_REPORT.md). This document preserves the earlier baseline.
Skill installed at project scope in the Odoo workspace and a clean checkout of this kit.
Codex and Antigravity share .agents/skills/primacy-engineering. Generated client copies are
excluded from Git. Each new checkout needs the documented installer.

## Codex CLI

Version 0.167.0-alpha.4.1. Executed with exec --ephemeral --ignore-user-config --sandbox
read-only from the clean kit checkout, using the existing login and default model.
Exit 0. Execution trace showed the client reading SKILL.md, references/debugging.md,
references/testing.md and assets/task-evidence.md. A fictional duplicate-invoice retry task
produced the following output. Discovery and this planning workflow passed. This establishes
CLI behavior, with desktop/IDE surfaces and actual ERP execution still NOT_RUN.

Read exact installed skill: `<test-project>/.agents/skills/primacy-engineering/SKILL.md`, plus `references/debugging.md`, `references/testing.md`, and `assets/task-evidence.md` beneath that directory.

**Task contract — PROPOSED:** Investigate the fictional report that retrying invoice creation produces duplicates. Acceptance: one logical request creates exactly one invoice; retries return the same outcome; distinct requests remain independent. Product/version/edition, modules, revision, environment, caller and owner are unspecified. Scope is planning only; accounting duplication is the principal risk. Budget: this response.

**Selected routes:** Primary: `debugging`. Supporting: `testing`. Reuse existing caller handling and test recipes after verifying their scope and revision.

**Reproduction and regression plan:**

- In an isolated environment with synthetic data, invoke the normal caller, simulate a lost response after commit, then retry the same logical request. Record invoice IDs, request correlation and transaction boundaries.
- Trace all callers of shared creation logic. Treat missing idempotency or a concurrency race as hypotheses until evidence establishes the cause.
- Check sequential retries, concurrent retries, failure before commit, lost response after commit, and distinct requests. Verify company isolation and conflicting payload handling.
- Assert one invoice per logical request and independently approved invoice amounts, taxes and accounting results.
- Plan L1 focused checks, L2 native Odoo/security/contract regression before PR, and L3 staging reconciliation and functional sign-off before release.

**Permission boundaries:** Only local guidance was read. No business actions, runtime calls, file edits, installations or deployment occurred. Any later live writes require scoped authorization; the skill itself grants none.

**Completion:** Planning complete; investigation and fix remain **PROPOSED**. Reproduction, tests and functional verification: **NOT_RUN**. No tests claimed passed. No files changed. Next prerequisite: an authorized isolated runtime and the missing version, revision, module and caller evidence. Cost: **UNAVAILABLE**.


## Antigravity CLI

Existing agy login, plan mode and sandbox. Two file-reading attempts returned exit 0
with empty stdout and a command-permission auto-denial. These attempts are BLOCKED,
regardless of the process exit code. A session-only narrow permission retry did not resolve it.
Global settings were preserved.

Native /primacy-engineering invocation with no tool calls returned exit 0 and correctly
listed all six profiles, establishing CLI skill discovery and router loading. Its first
planning answer suggested version-specific constraint syntax and invoice-reference uniqueness
before establishing the version or business key. This failed part of the behavioral review.
The router and three playbooks were tightened, and the debugging-boundary case was updated.
The corrected router was reinstalled. The targeted retest returned the following output.

Based on the loaded router in [primacy-engineering](../skills/primacy-engineering/SKILL.md):

### 1. Prerequisites Before Recommending Odoo API Syntax or Uniqueness Constraints
* **Exact Odoo Series & Existing Patterns:** You must establish the exact Odoo series/version and inspect its existing ORM and architectural patterns before proposing version-specific APIs, constraints, or schema changes.
* **Operation Identity:** You must prove the operation identity (the true logical idempotency key or transaction boundary) rather than assuming symptoms imply a database constraint is needed.

### 2. Can Invoice References Be Assumed Unique?
* **No.** As explicitly stated in the skill guidance: *"Invoice references may legitimately repeat."* (e.g., across companies, journals, vendors, or cancellation/re-issuance workflows).

---

### Route & Test Status
* **Primary Route:** `debugging` (Supporting: `requirements`, `python-api`)
* **Test Status:** `NOT_RUN` *(no tests or actions executed)*


Discovery and the targeted corrected-router response passed. File-reading/tool workflow
remains BLOCKED under the existing headless permissions. Desktop and IDE interaction,
real Odoo/MCP operations and the full 54-case evaluation remain NOT_RUN.

## Scope of result

Local unit suite — five tests passed. Skill validator, JSON parsing and local Markdown
links passed. A narrow private-key/token pattern check passed, with no comprehensive
secret or dependency audit claimed. No global installation, ERP connection or business
transaction was performed. Raw client diagnostics remain outside the published kit.
