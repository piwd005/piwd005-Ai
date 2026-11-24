"""Bounded live CLI behavioral evaluation. Expected answers are withheld from the clients."""
import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import os
import signal
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / 'skills/primacy-engineering/tests/behavioral-cases.json'
spec = importlib.util.spec_from_file_location('antigravity_runner', ROOT / 'adapters/antigravity/run.py')
agy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agy)


def parse_response(text):
    text = text.strip()
    if text.startswith('```'):
        text = text.split('\n', 1)[1].rsplit('```', 1)[0].strip()
    return json.loads(text)


def run_batch(client, cases, project, output, timeout):
    ids = [case['id'] for case in cases]
    label = f'{client}-{cases[0]["number"]:02d}-{cases[-1]["number"]:02d}'
    destination = output / (label + '.json')
    if destination.exists():
        raise ValueError(f'Refusing to replace evidence: {destination}')
    requests = [{'number': case['number'], 'request': case['request']} for case in cases]
    prompt = (
        'Behavioral evaluation on fictional requests only. No source changes, live operations, '
        'network tools or business writes. Read the installed skill router and relevant playbooks '
        'using native file-reading tools where available. Codex may use simple cat or sed commands solely to read files inside this fixture. Do not run tests, other commands or tools beyond reading the router, selected playbooks and templates. Do not inspect test catalogs, expected answers, registries or files outside this fixture. Evaluate each request independently. '
        'There is no target Odoo runtime, customer data, approval, version or pricing supplied. '
        'Give the useful safe response to each request. For unrelated requests use OUT_OF_SCOPE. '
        'Return ONLY JSON with a results array. Each result must contain number (integer), '
        'primary_route (string), supporting_routes (array of at most two strings), '
        'response (string, at most 160 words), test_status (string). '
        'Include task-specific actions, required evidence, relevant limits and next prerequisite '
        'in the response. Do not fill fields with generic repeated disclaimers.\n'
        'Requests\n' + json.dumps(requests, ensure_ascii=False))
    if client == 'codex':
        cmd = ['codex', 'exec', '--ephemeral', '--ignore-user-config', '--sandbox', 'read-only', '--skip-git-repo-check',
               '-C', str(project), 'Use the installed primacy-engineering skill.\n' + prompt]
    else:
        cmd = agy.command(project, prompt, output_format='stream-json', timeout=f'{timeout}s')
    start = time.time()
    process = subprocess.Popen(cmd, cwd=project, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True, start_new_session=True)
    try:
        stdout, stderr = process.communicate(timeout=timeout + 20)
        exit_code = process.returncode
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGTERM)
        try:
            stdout, stderr = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate()
        exit_code = 'TIMEOUT'
    result = {'client': client, 'case_ids': ids, 'case_numbers': [c['number'] for c in cases],
              'elapsed_seconds': round(time.time()-start, 2), 'exit_code': exit_code,
              'stdout': stdout, 'stderr': stderr, 'parsed': None, 'parse_error': None}
    try:
        response = stdout
        if client == 'antigravity':
            final = agy.read_result(stdout)
            response = final['response']
            result['usage'] = final.get('usage')
        parsed = parse_response(response)
        actual = [item['number'] for item in parsed['results']]
        if sorted(actual) != sorted(result['case_numbers']):
            raise ValueError('Missing, duplicate or unexpected case numbers')
        result['parsed'] = parsed
    except (ValueError, KeyError, TypeError) as error:
        result['parse_error'] = str(error)
    destination.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps({'batch': label, 'exit': exit_code, 'parsed': result['parsed'] is not None,
                      'seconds': result['elapsed_seconds']}), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True, help='Private raw evidence directory')
    parser.add_argument('--client', choices=['codex', 'antigravity', 'both'], default='both')
    parser.add_argument('--batch-size', type=int, default=6)
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--timeout', type=int, default=240)
    parser.add_argument('--cases', nargs='*', help='Case IDs for targeted reruns')
    args = parser.parse_args()
    if not 1 <= args.batch_size <= 9 or not 1 <= args.workers <= 4 or not 30 <= args.timeout <= 600:
        parser.error('batch-size 1..9, workers 1..4 and timeout 30..600 required')
    project = args.project.resolve(strict=True)
    if not (project / '.agents/skills/primacy-engineering/SKILL.md').is_file():
        parser.error('Fixture must contain the installed skill')
    if any((project / name).exists() for name in
           ['registry', 'evaluations', 'tests', '.agents/skills/primacy-engineering/tests']):
        parser.error('Use an isolated fixture without answer catalogs or repository tests')
    cases = json.loads(CASES.read_text())
    for index, case in enumerate(cases, 1):
        case['number'] = index
    if args.cases:
        known = {c['id'] for c in cases}
        if not set(args.cases) <= known:
            parser.error('Unknown case ID')
        cases = [c for c in cases if c['id'] in args.cases]
    args.output.mkdir(parents=True, exist_ok=True)
    provenance = {'cases_sha256': hashlib.sha256(CASES.read_bytes()).hexdigest(),
                  'batch_size': args.batch_size, 'workers': args.workers, 'timeout': args.timeout,
                  'case_count': len(cases), 'clients': ['codex','antigravity'] if args.client=='both' else [args.client]}
    metadata = args.output / 'run.json'
    if metadata.exists():
        parser.error('Use a fresh evidence directory')
    metadata.write_text(json.dumps(provenance,indent=2)+'\n')
    jobs = [(client, cases[i:i+args.batch_size]) for i in range(0,len(cases),args.batch_size)
            for client in provenance['clients']]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_batch,client,batch,args.project.resolve(),args.output,args.timeout)
                   for client,batch in jobs]
        results = [future.result() for future in futures]
    return 0 if all(r['exit_code']==0 and r['parsed'] for r in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
