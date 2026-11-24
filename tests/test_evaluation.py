import contextlib
import io
import sys
from unittest.mock import patch
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runner = load('evaluation', ROOT / 'evaluations/run.py')
fixture = load('fixture', ROOT / 'evaluations/prepare_fixture.py')


class EvaluationTests(unittest.TestCase):
    def test_fixture_excludes_answers_and_preserves_existing_project(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / 'fixture'
            fixture.prepare(project)
            skill = project / '.agents/skills/primacy-engineering'
            self.assertEqual((skill / 'SKILL.md').read_bytes(),
                             (ROOT / 'skills/primacy-engineering/SKILL.md').read_bytes())
            self.assertFalse((skill / 'tests').exists())
            self.assertFalse((project / 'registry').exists())
            with self.assertRaises(FileExistsError):
                fixture.prepare(project)

    def test_grant_is_session_only_and_skill_scoped(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            skill = project / '.agents/skills/primacy-engineering'
            skill.mkdir(parents=True)
            (skill / 'SKILL.md').write_text('fixture')
            command = runner.agy.command(project, 'fictional request')
            settings = json.loads(command[command.index('--settings')+1])
            self.assertEqual(settings, {'permissions': {'allow': [f'read_file({skill.resolve()})']}})
            self.assertNotIn('--dangerously-skip-permissions', command)
            self.assertEqual(command[command.index('--mode')+1], 'plan')
            self.assertIn('--sandbox', command)
            self.assertEqual(list(project.iterdir()), [project / '.agents'])

    def test_missing_install_is_rejected_before_client_launch(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                runner.agy.command(directory, 'request')

    def test_answer_catalog_fixture_is_rejected_before_launch(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            skill = project / '.agents/skills/primacy-engineering'
            skill.mkdir(parents=True)
            (skill / 'SKILL.md').write_text('fixture')
            (skill / 'tests').mkdir()
            output = project / 'evidence'
            argv = ['evaluate', '--project', str(project), '--output', str(output)]
            with patch.object(sys, 'argv', argv), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as error:
                    runner.main()
            self.assertEqual(error.exception.code, 2)
            self.assertFalse(output.exists())

    def test_empty_success_result_is_a_failure(self):
        denied = {'event': 'result', 'result': {'status': 'SUCCESS', 'response': '',
                                               'denied_actions': [{'action': 'command'}]}}
        with self.assertRaises(ValueError):
            runner.agy.read_result(json.dumps(denied))
        success = {'event': 'result', 'result': {'status': 'SUCCESS', 'response': 'Observed answer'}}
        self.assertEqual(runner.agy.read_result(json.dumps(success))['response'], 'Observed answer')

    def test_json_parser_accepts_fences_and_rejects_prose(self):
        self.assertEqual(runner.parse_response('```json\n{"results": []}\n```'), {'results': []})
        with self.assertRaises(ValueError):
            runner.parse_response('Tests passed without any evidence')


if __name__ == '__main__':
    unittest.main()
