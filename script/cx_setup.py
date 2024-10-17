from __future__ import annotations

import sysconfig
import tomllib
from pathlib import Path

from cx_Freeze import Executable, setup

if __name__ == '__main__':
    root = Path(__file__).parents[1]

    si = (sysconfig.get_platform(), sysconfig.get_python_version())
    pyprj = tomllib.loads((root / 'pyproject.toml').read_text('UTF-8'))
    name = pyprj['project']['name']
    version = pyprj['project']['version']

    options = {
        'build_exe': {
            'build_exe': f'build/{name}-{version}-exe.{si[0]}-{si[1]}',
            'excludes': ['attr', 'test', 'unittest'],
            'include_files': ['assets', 'qt'],
        }
    }
    executables = [
        Executable(script='app.py'),
    ]

    setup(executables=executables, options=options)
