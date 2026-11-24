import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/primacy-engineering'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


builder = load('catalog_builder', ROOT / 'scripts/build_catalog.py')
selector = load('source_selector', SKILL / 'scripts/sources.py')
qa = load('quality_checks', SKILL / 'scripts/qa.py')
installer = load('project_installer', ROOT / 'adapters/install.py')


def addon(path, version='19.0'):
    path.mkdir()
    (path / '__init__.py').write_text('from . import models\n')
    manifest = {'name': 'Quality Fixture', 'summary': 'Synthetic local QA fixture',
                'version': version + '.1.0.0', 'author': 'Primacy Infotech',
                'license': 'LGPL-3', 'depends': ['base'], 'data': [], 'installable': True}
    (path / '__manifest__.py').write_text(repr(manifest)+'\n')
    (path / 'models.py').write_text('from odoo import fields, models\n\n\nclass QualityFixture(models.Model):\n    _name = "primacy.quality.fixture"\n    _description = "Quality fixture"\n\n    name = fields.Char(required=True)\n')


class CatalogTests(unittest.TestCase):
    def test_generated_catalog_and_all_routes_are_current(self):
        self.assertEqual(builder.OUTPUT.read_text(), builder.render())
        data = json.loads(builder.render())
        self.assertEqual(len(data['sources']), 62)
        self.assertEqual(len(data['routes']), 24)

    def test_installed_copy_contains_catalog_and_resolves_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            result = installer.install(directory, 'codex', True)
            installed = Path(result['destination'])
            data = selector.select_sources('odoo-backend', '19.0', installed / 'references/source-index.json')
            self.assertIn('odoo-module', {r['id'] for r in data})
            self.assertNotIn('odoo20-house', {r['id'] for r in data})
            data20 = selector.select_sources('odoo-backend', '20.0', installed / 'references/source-index.json')
            self.assertIn('odoo20-house', {r['id'] for r in data20})
            self.assertNotIn('odoo-module', {r['id'] for r in data20})
            with self.assertRaises(ValueError):
                selector.select_sources('unknown', index=installed / 'references/source-index.json')


class QATests(unittest.TestCase):
    def test_missing_tool_is_not_a_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / 'sample.py').write_text('x = 1\n')
            report = qa.evaluate(target, ['ruff'], target)
            self.assertEqual(report['exit_code'], 2)
            self.assertEqual(report['results'][0]['status'], 'NOT_RUN')

    def test_audit_lock_rejects_resolution_and_url_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'requirements.lock'
            for text in ['requests>=2', '-r other.txt', '-e .', 'package @ https://example.org/p.whl']:
                path.write_text(text)
                with self.assertRaises(ValueError):
                    qa.validate_lock(path)
            path.write_text('example==1.0 --hash=sha256:'+'a'*64+'\n')
            qa.validate_lock(path)

    def test_timeout_and_invalid_tool_output_are_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'x.py').write_text('x = 1\n')
            (root / 'ruff').write_text('placeholder')
            with patch.object(qa.subprocess, 'run', side_effect=qa.subprocess.TimeoutExpired('ruff', 1)):
                self.assertEqual(qa.evaluate(root, ['ruff'], root)['results'][0]['status'], 'ERROR')
            completed = qa.subprocess.CompletedProcess([], 0, 'not diagnostics', '')
            with patch.object(qa.subprocess, 'run', return_value=completed):
                self.assertEqual(qa.evaluate(root, ['ruff'], root)['results'][0]['status'], 'ERROR')

    def test_version_mismatch_and_network_opt_in(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / 'addon'
            addon(target)
            (root / 'pylint').write_text('placeholder')
            (root / 'pip-audit').write_text('placeholder')
            report = qa.evaluate(target, ['pylint-odoo', 'pip-audit'], root, '20.0')
            self.assertEqual(report['exit_code'], 2)
            self.assertEqual([r['status'] for r in report['results']], ['ERROR', 'NOT_RUN'])


@unittest.skipUnless(os.environ.get('PRIMACY_QA_TOOLS_DIR'), 'Real QA tool environment not selected')
class RealQATests(unittest.TestCase):
    def setUp(self):
        self.tools = Path(os.environ['PRIMACY_QA_TOOLS_DIR'])

    def test_clean_addons_both_versions_and_static_mutants(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for version in ['19.0', '20.0']:
                target = root / ('fixture'+version[:2])
                addon(target, version)
                report = qa.evaluate(target, ['ruff', 'pylint-odoo', 'oca-hooks'], self.tools, version)
                self.assertEqual(report['exit_code'], 0, report)
                with (target / 'models.py').open('a') as stream:
                    stream.write('\n    def action_bad(self):\n        self.env.cr.commit()\n        return missing_name\n')
                report = qa.evaluate(target, ['ruff', 'pylint-odoo'], self.tools, version)
                self.assertEqual([r['status'] for r in report['results']], ['FAIL', 'FAIL'], report)
                self.assertIn('F821', report['results'][0]['diagnostics'])
                self.assertIn('invalid-commit', report['results'][1]['diagnostics'])

    def test_generic_package_imports_remain_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / '__init__.py').write_text('import unused_module\n')
            report = qa.evaluate(target, ['ruff'], self.tools)
            self.assertEqual(report['results'][0]['status'], 'FAIL', report)
            self.assertIn('F401', report['results'][0]['diagnostics'])

    def test_oca_duplicate_xml_id_and_redacted_canary(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'addon'
            addon(target)
            manifest = target / '__manifest__.py'
            metadata = qa.ast.literal_eval(manifest.read_text())
            metadata['data'] = ['views.xml']
            manifest.write_text(repr(metadata))
            (target / 'views.xml').write_text('<odoo><record id="x" model="res.partner"/><record id="x" model="res.partner"/></odoo>')
            report = qa.evaluate(target, ['oca-hooks'], self.tools, '19.0')
            self.assertEqual(report['results'][0]['status'], 'FAIL', report)
            self.assertIn('xml-duplicate-record-id', report['results'][0]['diagnostics'])
            token = ''.join(['gh', 'p_', 'A7b8C9d0E1f2G3h4I5j6K7l8M9n0P1q2R3s4'])
            (target / 'synthetic.env').write_text('GITHUB_TOKEN='+token+'\n')
            report = qa.evaluate(target, ['gitleaks'], self.tools)
            self.assertEqual(report['results'][0]['status'], 'FAIL', report)
            self.assertTrue(any(f['file'].endswith('synthetic.env') for f in report['results'][0]['findings']))
            self.assertNotIn(token, json.dumps(report))
            self.assertNotIn('Secret', json.dumps(report))


if __name__ == '__main__':
    unittest.main()
