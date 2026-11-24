"""Generate the portable catalog from canonical source records and route mappings."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'skills/primacy-engineering/references/source-index.json'


def render(root=ROOT):
    sources = json.loads((root / 'registry/sources.json').read_text())
    routes = json.loads((root / 'registry/route-sources.json').read_text())
    keys = ['id', 'title', 'url', 'artifact_type', 'admission_status', 'revision',
            'reviewed_version', 'source_revision', 'license_review', 'versions', 'verification_scope']
    entries = {item['id']: {key: item[key] for key in keys if key in item} for item in sources}
    if len(entries) != len(sources):
        raise ValueError('Duplicate source IDs')
    known_routes = {r['id'] for r in json.loads((root / 'registry/routes.json').read_text())}
    if set(routes) != known_routes:
        raise ValueError('Source mappings must cover every route exactly')
    linked = {identifier for ids in routes.values() for identifier in ids}
    if linked != set(entries):
        raise ValueError('Missing or unknown mapped source IDs')
    payload = {'format': 1, 'generated': True, 'routes': routes, 'sources': entries,
               'usage': 'Load only selected route entries. Catalog presence grants no execution, copying or runtime permissions.'}
    return json.dumps(payload, indent=2, ensure_ascii=False) + '\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        text = render()
        if args.check:
            if not OUTPUT.exists() or OUTPUT.read_text() != text:
                parser.exit(1, 'Portable catalog is stale. Run scripts/build_catalog.py\n')
        else:
            OUTPUT.write_text(text)
    except (OSError, ValueError) as error:
        parser.exit(1, f'{error}\n')
