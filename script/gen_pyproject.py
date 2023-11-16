import json
from itertools import chain
from pathlib import Path

import tomli

EXCLUDE = {'dist', 'build'}
EXTS = {'.py', '.qml'}

if __name__ == '__main__':
    root = Path(__file__).parents[1]
    with (root / 'pyproject.toml').open('rb') as rf:
        pyproject = tomli.load(rf)

    project = pyproject['project']['name']

    paths = chain.from_iterable((f for f in root.rglob(f'*{e}')) for e in EXTS)
    texts = sorted(
        f.as_posix() for f in paths if all(p not in EXCLUDE for p in f.parts)
    )

    with (root / f'{project}.pyproject').open('w', encoding='utf-8') as wf:
        json.dump({'files': texts}, wf, indent=4)
