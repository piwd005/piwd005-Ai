"""Project-only installer. Dry-run by default and refuses existing destinations."""
import argparse
import json
import shutil
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
PATHS = {'codex': '.agents/skills', 'antigravity': '.agents/skills', 'claude-code': '.claude/skills'}


def install(project, client, apply=False):
    project = Path(project).resolve(strict=True)
    if not project.is_dir():
        raise ValueError('Project must be an existing directory')
    relative = Path(PATHS[client]) / 'primacy-engineering'
    destination = project / relative
    current = project
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f'Symlink destination refused: {current}')
    if destination.exists():
        raise FileExistsError(f'Existing installation preserved: {destination}')
    result = {'client': client, 'destination': str(destination), 'status': 'PROPOSED', 'apply': apply}
    if apply:
        # copytree claims the leaf exclusively. Partial failures remain for manual review.
        shutil.copytree(KIT / 'skills/primacy-engineering', destination,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        result['status'] = 'CREATED'
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True)
    parser.add_argument('--client', choices=PATHS, required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    try:
        print(json.dumps(install(args.project, args.client, args.apply), indent=2))
    except (OSError, ValueError) as error:
        parser.exit(1, f'{error}\n')
