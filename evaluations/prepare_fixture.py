"""Create a fresh evaluation project without the answer catalog or repository tests."""
import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def prepare(destination):
    destination = Path(destination).absolute()
    destination.mkdir(parents=True, exist_ok=False)
    source = ROOT / 'skills/primacy-engineering'
    skill = destination / '.agents/skills/primacy-engineering'
    skill.mkdir(parents=True)
    for name in ['SKILL.md', 'references', 'assets', 'agents']:
        if (source / name).is_dir():
            shutil.copytree(source / name, skill / name)
        else:
            shutil.copy2(source / name, skill / name)
    shutil.copy2(ROOT / 'evaluations/FIXTURE_AGENTS.md', destination / 'AGENTS.md')
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    try:
        print(prepare(args.destination))
    except OSError as error:
        parser.exit(1, f'{error}\n')
