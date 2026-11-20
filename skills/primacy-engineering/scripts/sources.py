"""Select version-relevant source metadata without fetching or executing it."""
import argparse
import json
from pathlib import Path

INDEX = Path(__file__).resolve().parents[1] / 'references/source-index.json'


def select_sources(route, version=None, index=INDEX):
    catalog = json.loads(index.read_text())
    if route not in catalog['routes']:
        raise ValueError(f'Unknown route: {route}')
    records = [catalog['sources'][key] for key in catalog['routes'][route]]
    return [r for r in records if not version or not r['versions'] or version in r['versions']]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('route')
    parser.add_argument('--version', choices=['19.0', '20.0'])
    args = parser.parse_args()
    try:
        print(json.dumps(select_sources(args.route, args.version), indent=2, ensure_ascii=False))
    except (OSError, ValueError) as error:
        parser.exit(1, f'{error}\n')
