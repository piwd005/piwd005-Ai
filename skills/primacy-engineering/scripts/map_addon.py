"""Bounded static addon map, without importing source."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path


def map_addon(root, max_files=200):
    root = Path(root).resolve(strict=True)
    manifest = root / '__manifest__.py'
    if not root.is_dir() or not 1 <= max_files <= 10000:
        raise ValueError('Expected an addon directory and file budget from 1 to 10000')
    if manifest.is_symlink() or not manifest.is_file():
        raise ValueError('Expected regular __manifest__.py')
    files = []
    for current, directories, names in os.walk(root, followlinks=False):
        directories[:] = sorted(d for d in directories if not d.startswith('.') and d not in {'node_modules', '__pycache__', 'venv', 'build', 'dist'} and not (Path(current) / d).is_symlink())
        for name in sorted(names):
            path = Path(current) / name
            if path.suffix not in {'.py', '.xml', '.csv', '.js'} or path.is_symlink():
                continue
            if len(files) >= max_files:
                raise ValueError('File budget exceeded; narrow the scope or explicitly increase budget')
            if path.stat().st_size > 1_000_000:
                raise ValueError('File size exceeds 1 MB')
            body = path.read_bytes()
            item = {'path': str(path.relative_to(root)), 'sha256': hashlib.sha256(body).hexdigest()}
            if path.suffix == '.py':
                tree = ast.parse(body, filename=item['path'])
                item['classes'] = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
            files.append(item)
    metadata = ast.literal_eval(manifest.read_text())
    if not isinstance(metadata, dict):
        raise ValueError('Manifest must be a literal dictionary')
    return {'scope': root.name, 'kind': 'STATIC_ONLY', 'manifest': metadata, 'files': files,
            'limitations': ['No live registry resolution', 'No complete dependency graph']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('addon')
    parser.add_argument('--max-files', type=int, default=200)
    args = parser.parse_args()
    try:
        print(json.dumps(map_addon(args.addon, args.max_files), indent=2))
    except (OSError, ValueError, SyntaxError) as error:
        parser.exit(1, f'{error}\n')
