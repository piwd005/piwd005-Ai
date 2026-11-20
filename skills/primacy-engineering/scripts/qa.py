"""Run explicit, non-fixing QA checks and report missing tools as NOT_RUN."""
import argparse
import ast
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / 'assets/qa'
CHECKS = ['ruff', 'pylint-odoo', 'oca-hooks', 'gitleaks', 'pip-audit']
EXECUTABLES = {'pylint-odoo': 'pylint', 'oca-hooks': 'oca-checks-odoo-module'}
ODOO_MESSAGES = 'sql-injection,invalid-commit,context-overridden,missing-return,manifest-required-key,manifest-version-format'


def python_files(target):
    files = []
    for current, directories, names in os.walk(target, followlinks=False):
        directories[:] = sorted(d for d in directories if not d.startswith('.') and d not in
                                {'node_modules', 'venv', '__pycache__', 'build', 'dist'}
                                and not (Path(current) / d).is_symlink())
        files.extend(Path(current) / n for n in sorted(names) if n.endswith('.py')
                     and not (Path(current) / n).is_symlink())
        if len(files) > 500:
            raise ValueError('Python file budget exceeded. Select a narrower target.')
    return files


def validate_lock(path):
    pattern = r'[A-Za-z0-9][A-Za-z0-9_.-]*==[A-Za-z0-9][A-Za-z0-9.!+_-]*(?:[ \t]+--hash=sha256:[0-9a-f]{64})+'
    lines = [line.strip() for line in path.read_text().splitlines()
             if line.strip() and not line.lstrip().startswith('#')]
    if not lines or not all(re.fullmatch(pattern, line) for line in lines):
        raise ValueError('Audit requires single-line name==version entries with SHA-256 hashes, including transitive dependencies. URLs, includes and editable requirements are refused.')


def run_check(name, target, files, tools_dir, version, requirements, allow_network, timeout):
    executable = EXECUTABLES.get(name, name)
    binary = str(tools_dir / executable) if tools_dir else shutil.which(executable)
    if not binary or not Path(binary).is_file():
        return {'check': name, 'status': 'NOT_RUN', 'reason': 'Executable unavailable'}
    if name in {'ruff', 'pylint-odoo'} and not files:
        return {'check': name, 'status': 'NOT_RUN', 'reason': 'No Python files in scope'}
    if name in {'pylint-odoo', 'oca-hooks'}:
        manifest = target / '__manifest__.py'
        if not version or not manifest.is_file():
            return {'check': name, 'status': 'NOT_RUN', 'reason': 'Odoo version and single addon root required'}
        metadata = ast.literal_eval(manifest.read_text())
        if not isinstance(metadata, dict):
            raise ValueError('Addon manifest must be a literal dictionary')
        declared = str(metadata.get('version', ''))
        if declared.startswith(('19.0.', '20.0.')) and not declared.startswith(version + '.'):
            return {'check': name, 'status': 'ERROR', 'reason': 'Requested series differs from addon manifest'}
    if name == 'pip-audit':
        if not allow_network or requirements is None:
            return {'check': name, 'status': 'NOT_RUN', 'reason': 'Explicit --allow-network and --requirements required. Audit transmits package names and versions.'}
        validate_lock(requirements)
    with tempfile.TemporaryDirectory(prefix='primacy-qa-') as directory:
        temp = Path(directory)
        if name == 'ruff':
            args = ['check', '--isolated', '--no-cache', '--select', 'E4,E7,E9,F',
                    '--output-format', 'json']
            if version and (target / '__manifest__.py').is_file():
                # Odoo package imports register models and must not be removed as unused.
                args.extend(['--per-file-ignores', '**/__init__.py:F401'])
            args.extend(map(str, files))
        elif name == 'pylint-odoo':
            args = ['--rcfile=' + os.devnull, '--persistent=no', '--load-plugins=pylint_odoo',
                    '--disable=all', '--enable=' + ODOO_MESSAGES,
                    '--valid-odoo-versions=' + version, '--output-format=json', *map(str, files)]
        elif name == 'oca-hooks':
            args = ['--config', str(ASSETS / 'oca-hooks.cfg'), str(target)]
        elif name == 'gitleaks':
            args = ['dir', str(target), '--config', str(ASSETS / 'gitleaks.toml'),
                    '--redact=100', '--no-banner', '--ignore-gitleaks-allow',
                    '--gitleaks-ignore-path', str(temp / 'no-project-ignore'),
                    '--report-format=json', '--report-path', str(temp / 'leaks.json')]
        else:
            args = ['--requirement', str(requirements), '--require-hashes', '--disable-pip',
                    '--no-deps', '--format=json', '--progress-spinner=off', '--cache-dir', str(temp / 'cache')]
        env = os.environ.copy()
        for key in ['PYTHONPATH', 'PYTHONHOME', 'PYLINTRC', 'GITLEAKS_CONFIG', 'GITLEAKS_CONFIG_TOML']:
            env.pop(key, None)
        env.update(PYTHONNOUSERSITE='1', PYLINTHOME=str(temp / 'pylint'))
        try:
            result = subprocess.run([binary, *args], cwd=target, env=env, capture_output=True,
                                    text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return {'check': name, 'status': 'ERROR', 'reason': 'Timeout'}
        except OSError as error:
            return {'check': name, 'status': 'ERROR', 'reason': str(error)}
        record = {'check': name, 'status': 'PASS' if result.returncode == 0 else 'FAIL',
                  'exit_code': result.returncode, 'executable': binary}
        if name == 'gitleaks':
            # Discard scanner diagnostics and secret-bearing fields even when redaction was requested.
            path = temp / 'leaks.json'
            findings = json.loads(path.read_text()) if path.exists() else []
            record['findings'] = [{'rule': f.get('RuleID'), 'file': f.get('File'),
                                   'line': f.get('StartLine')} for f in (findings or [])]
            if result.returncode not in [0, 1] or (result.returncode == 1 and not findings):
                record['status'] = 'ERROR'
        else:
            record['diagnostics'] = (result.stdout + result.stderr)[:8000]
            if name in {'ruff', 'pylint-odoo', 'pip-audit'}:
                try:
                    parsed = json.loads(result.stdout)
                    if name == 'pip-audit':
                        dependencies = parsed['dependencies']
                        record['finding_count'] = sum(len(d.get('vulns', [])) for d in dependencies)
                        if any(d.get('skip_reason') for d in dependencies):
                            record['status'] = 'ERROR'
                    else:
                        if not isinstance(parsed, list):
                            raise ValueError('Expected JSON diagnostic list')
                        record['finding_count'] = len(parsed)
                    if (name == 'ruff' and result.returncode not in [0, 1]) or (name == 'pylint-odoo' and result.returncode & 32):
                        record['status'] = 'ERROR'
                except (ValueError, KeyError, TypeError):
                    record['status'] = 'ERROR'
            elif result.returncode not in [0, 1]:
                record['status'] = 'ERROR'
        return record


def evaluate(target, checks, tools_dir=None, version=None, requirements=None, allow_network=False, timeout=60):
    target = Path(target).resolve(strict=True)
    if not target.is_dir() or not 1 <= timeout <= 600:
        raise ValueError('Existing target directory and timeout between 1 and 600 required')
    if not checks or not set(checks) <= set(CHECKS):
        raise ValueError('Unknown or empty QA check selection')
    tools_dir = Path(tools_dir).resolve(strict=True) if tools_dir else None
    requirements = Path(requirements).resolve(strict=True) if requirements else None
    files = python_files(target)
    results = []
    for name in checks:
        try:
            results.append(run_check(name, target, files, tools_dir, version, requirements, allow_network, timeout))
        except (OSError, ValueError, SyntaxError) as error:
            results.append({'check': name, 'status': 'ERROR', 'reason': str(error)})
    code = 2 if any(r['status'] in ['ERROR', 'NOT_RUN'] for r in results) else int(any(r['status'] == 'FAIL' for r in results))
    return {'target': str(target), 'odoo_version': version, 'results': results, 'exit_code': code}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', required=True)
    parser.add_argument('--checks', choices=CHECKS, nargs='+', default=['ruff'])
    parser.add_argument('--tools-dir', type=Path)
    parser.add_argument('--odoo-version', choices=['19.0', '20.0'])
    parser.add_argument('--requirements', type=Path)
    parser.add_argument('--allow-network', action='store_true')
    parser.add_argument('--timeout', type=int, default=60)
    args = parser.parse_args()
    try:
        report = evaluate(args.target, args.checks, args.tools_dir, args.odoo_version,
                          args.requirements, args.allow_network, args.timeout)
        print(json.dumps(report, indent=2))
        raise SystemExit(report['exit_code'])
    except (OSError, ValueError) as error:
        parser.exit(2, f'{error}\n')
