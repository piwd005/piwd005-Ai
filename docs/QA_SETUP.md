# Local QA setup

The portable core requires no third-party imports. Optional QA tools run as external CLIs.
Use an existing approved tool environment or prepare a separate virtual environment.
The included wheel hash lock was tested on macOS arm64 CPython 3.12 only.

```sh
python3 -m venv /absolute/qa-venv
/absolute/qa-venv/bin/python -m pip install --only-binary=:all: --require-hashes -r skills/primacy-engineering/assets/qa/requirements-macos-arm64-py312.lock
```

The tested build downloaded wheels first and installed offline. The command above would
fetch those pinned artifacts from the configured package registry. Review/authorize that
network installation for the target environment. No upstream source installer, project
setup.py or global client settings need to run. Inspect the lock/provenance before use.
For another platform, review a matching wheel graph instead of bypassing hashes.

Gitleaks is supplied separately through its official pinned release. The reviewed Darwin
arm64 download URL and archive SHA-256 are recorded in gitleaks-provenance.json inside
assets/qa. Verify the checksum before extracting the executable to the chosen tools directory.
This kit does not include an executable or automatically download one.

For an addon, select only the relevant directory and its known version.

```sh
python3 skills/primacy-engineering/scripts/qa.py --target /absolute/addon --checks ruff pylint-odoo oca-hooks --odoo-version 20.0 --tools-dir /absolute/qa-venv/bin
```

Ruff's Odoo baseline preserves package registration imports. OCA scans declared module data.
Gitleaks and OCA use their own discovery rules, so select a bounded trusted source directory
and review coverage. Reports can contain private paths and identifiers. Retain raw results
locally. Only synthetic reviewed test evidence is included in this repository.

pip-audit requires explicit --allow-network and a complete, exact-version SHA-256 lock.
The helper disables pip resolution/builds, rejects URL/editable/include requirements and
reports skipped dependencies or unavailable results as errors. Package names and versions
are sent to advisory services. The tested audit covers the QA toolchain, not application
requirements or every dependency in an Odoo deployment.

Exit 0 means all selected checks passed. Exit 1 means findings. Exit 2 means an error or
incomplete check. Missing tools and absent runtime prerequisites never count as PASS.
Read the portable references/qa.md for the exact baseline scope and reviewed exception.
