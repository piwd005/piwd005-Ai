"""Run Antigravity with a session-only read grant to this project's installed skill."""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def command(project, prompt, executable='agy', output_format='text', timeout='180s'):
    project = Path(project).resolve(strict=True)
    skill = project / '.agents/skills/primacy-engineering'
    if not (skill / 'SKILL.md').is_file():
        raise ValueError('Install primacy-engineering into the project first')
    settings = {'permissions': {'allow': [f'read_file({skill})']}}
    instruction = (f'Use the installed primacy-engineering skill at {skill}. Read its router and only '
                   'relevant playbooks using file-reading tools. Do not use terminal commands to read '
                   'the skill. Other actions retain the client permission rules.\n\n' + prompt)
    return [executable, '--mode', 'plan', '--sandbox', '--settings', json.dumps(settings),
            '--output-format', output_format, '--print-timeout', timeout, '--print', instruction]


def read_result(stdout):
    events = [json.loads(line) for line in stdout.splitlines() if line.strip().startswith('{')]
    results = [event['result'] for event in events if event.get('event') == 'result']
    if not results or results[-1].get('status') != 'SUCCESS':
        raise ValueError('Antigravity did not return a successful result')
    if not isinstance(results[-1].get('response'), str) or not results[-1]['response'].strip():
        raise ValueError('Antigravity returned no answer; inspect permission denials in diagnostics')
    return results[-1]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True)
    parser.add_argument('prompt')
    args = parser.parse_args()
    try:
        executable = shutil.which('agy')
        if not executable:
            raise ValueError('agy is not on PATH')
        result = subprocess.run(command(args.project, args.prompt, executable, output_format='stream-json'),
                                cwd=args.project, capture_output=True, text=True)
        if result.stderr:
            sys.stderr.write(result.stderr)
        if result.returncode:
            raise SystemExit(result.returncode)
        print(read_result(result.stdout)['response'])
    except (OSError, ValueError) as error:
        parser.exit(1, f'{error}\n')
