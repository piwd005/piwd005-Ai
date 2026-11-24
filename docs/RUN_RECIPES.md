# Verified helper recipes

From the kit root, Python 3.12.7 on macOS arm64 was used for these commands.

```sh
python3 -m unittest discover -s tests -v
python3 skills/primacy-engineering/scripts/map_addon.py /absolute/addon --max-files 200
python3 adapters/install.py --project /absolute/project --client codex
```

Unit tests exercise the mapper and installer in temporary projects. A real addon map is
static metadata only. The mapper can fail on nonliteral manifests, malformed Python,
files over 1 MB or file-budget exhaustion. Narrow the task before increasing limits.

Native Odoo test commands must be obtained from the target project's actual runtime and
configuration. No Odoo runtime or database is included, and no native ERP test recipe is
claimed verified by this kit. Verify the current checkout and applicable policies first.
