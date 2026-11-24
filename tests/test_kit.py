import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/primacy-engineering'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


installer = load('installer', ROOT / 'adapters/install.py')
mapper = load('mapper', SKILL / 'scripts/map_addon.py')


class KitTests(unittest.TestCase):
    def test_routes_profiles_and_specs(self):
        routes = json.loads((ROOT / 'registry/routes.json').read_text())
        ids = {r['id'] for r in routes}
        self.assertEqual(len(ids), 24)
        for route in routes:
            self.assertTrue((SKILL / route['playbook']).is_file())
        for profile in json.loads((ROOT / 'registry/profiles.json').read_text()).values():
            self.assertTrue(set(profile) <= ids)
        cases = json.loads((SKILL / 'tests/behavioral-cases.json').read_text())
        self.assertEqual(len(cases), 54)
        self.assertEqual(len({c['id'] for c in cases}), 54)
        for case in cases:
            self.assertIn(case['primary_route'], ids | {'OUT_OF_SCOPE'})
            self.assertEqual(case['status'], 'NOT_RUN')

    def test_dry_run_copy_and_collision(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            installer.install(root, 'codex')
            self.assertEqual(list(root.iterdir()), [])
            result = installer.install(root, 'codex', True)
            self.assertEqual((Path(result['destination']) / 'SKILL.md').read_bytes(), (SKILL / 'SKILL.md').read_bytes())
            with self.assertRaises(FileExistsError):
                installer.install(root, 'antigravity', True)
            result = installer.install(root, 'claude-code', True)
            self.assertTrue((Path(result['destination']) / 'references/mcp.md').exists())

    def test_symlink_destination_is_refused(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            (Path(directory) / '.agents').symlink_to(outside)
            with self.assertRaises(ValueError):
                installer.install(directory, 'codex', True)
            self.assertEqual(list(Path(outside).iterdir()), [])

    def test_map_never_executes_source_and_enforces_budget(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / '__manifest__.py').write_text("{'depends': ['base']}")
            (root / 'models.py').write_text("raise RuntimeError('must not execute')\nclass Demo: pass\n")
            result = mapper.map_addon(root)
            self.assertEqual(result['manifest']['depends'], ['base'])
            self.assertEqual(result['files'][1]['classes'], ['Demo'])
            with self.assertRaises(ValueError):
                mapper.map_addon(root, 1)
            (root / 'alias.py').symlink_to(root / 'models.py')
            self.assertEqual(len(mapper.map_addon(root)['files']), 2)

    def test_manifest_expression_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / '__manifest__.py').write_text("dict(name='expression')")
            with self.assertRaises(ValueError):
                mapper.map_addon(directory)


if __name__ == '__main__':
    unittest.main()
