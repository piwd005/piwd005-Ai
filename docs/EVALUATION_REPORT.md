# Initial build evaluation, 15 November 2026

Latest full-case results and permission remediation are recorded in [FULL_EVALUATION_REPORT.md](FULL_EVALUATION_REPORT.md). This document preserves the earlier baseline.
Subsequent actual client results and the behavioral correction are in [CLIENT_TEST_RESULTS.md](CLIENT_TEST_RESULTS.md). The table below is the initial build baseline.

| Component | Actual status | Evidence |
|---|---|---|
| Router, 24 playbooks, six profiles | STRUCTURE_VALIDATED | Skill creator validator exit 0; registry tests exit 0 |
| Project installer | FUNCTIONALLY_VERIFIED for temporary local copies | Dry-run purity, copy equality, shared-path collision and symlink denial tests |
| Static mapper | FUNCTIONALLY_VERIFIED for static metadata | Literal parsing, no source execution, file budget and symlink tests; 95 actual addon files mapped |
| Source registry and schema | CREATED | Supplied catalog parsed; no admission or runtime installation |
| 54 behavioral cases | NOT_RUN | Newly authored English/Hindi/Bengali specifications; structural coverage checked only |
| Codex, Antigravity, Claude discovery | NOT_RUN | Adapter paths documented; no client integration activated |
| Odoo runtime, functional UAT, MCP and release pilots | NOT_RUN | No isolated Odoo runtime/staging identity authorized for this build |
| Delivery/token savings | NOT_RUN | No accepted-task baseline; AI cost UNAVAILABLE |

Commands executed with Python 3.12.7 on macOS arm64 from the owning workspace.

- python3 -m unittest discover -s primacy-ai-engineering-kit/tests -v — exit 0, five tests.
- python3 <skill-creator>/scripts/quick_validate.py primacy-ai-engineering-kit/skills/primacy-engineering — exit 0, valid.
- python3 primacy-ai-engineering-kit/skills/primacy-engineering/scripts/map_addon.py <authorized-addon> --max-files 300 — exit 0, 95 files, STATIC_ONLY.

Internal source inspection artifacts and environment reports are excluded from public distribution.
The static map test result establishes source inspection only, without deployment verification.
The initial generated documentation script had a syntax error and was corrected before
delivery. An initial helper-write attempt encountered missing directories and was rerun
after creating them. All reported passing checks were run after the corresponding fixes.

The supplied v2 brief superseded v1. No starter bundle or original 54-case dataset was
provided. This implementation creates 54 new cases and one canonical original skill.
No third-party source was vendored. An all-rights-reserved initial notice avoids granting
an open-source license on Primacy's behalf. Select the intended license before public reuse.

Next acceptance step is discovery in one selected actual client, followed by a harmless
workflow. Run the behavioral cases as real prompts and score routes, boundaries and evidence
against the expected contracts. Retain failed responses and rerun only after meaningful fixes.
Then obtain an isolated Odoo environment for a real change/regression/UAT/MCP pilot.
