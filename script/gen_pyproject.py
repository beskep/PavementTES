from __future__ import annotations

import json
import tomllib
from itertools import chain
from pathlib import Path

EXCLUDE = {'dist', 'build'}
EXTS = {'.py', '.qml'}

if __name__ == '__main__':
    root = Path(__file__).parents[1]
    pyproject = Path(__file__).parents[1] / 'pyproject.toml'
    project = tomllib.loads(pyproject.read_text('UTF-8'))['project']['name']

    paths = chain.from_iterable((f for f in root.rglob(f'*{e}')) for e in EXTS)
    texts = sorted(
        f.as_posix() for f in paths if all(p not in EXCLUDE for p in f.parts)
    )

    with (root / f'{project}.pyproject').open('w', encoding='utf-8') as wf:
        json.dump({'files': texts}, wf, indent=4)
