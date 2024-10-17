from __future__ import annotations

import json
from typing import Literal

from loguru import logger
from PySide6 import QtCore, QtGui

from ptes import xlsx
from ptes.calculate import Capacity, CapacityCases, PavementTES


class _Window:
    def __init__(self, window: QtGui.QWindow) -> None:
        self._window = window

    @property
    def window(self):
        return self._window

    def page(self, p: Literal['basic', 'design', 'analysis'], /):
        return self._window.page(p)  # type: ignore[attr-defined]


class Controller(QtCore.QObject):
    MATERIALS = ('물', '모래', '물+모래')

    def __init__(self, window: QtGui.QWindow) -> None:
        super().__init__()

        self._winow = _Window(window)
        self._pt = PavementTES()
        self._cases: tuple[Capacity, ...]

    @QtCore.Slot(str)
    def log(self, message: str):
        if (find := message.find('|')) == -1:
            level = 'DEBUG'
        else:
            level = message[:find].upper()
            message = message[(find + 1) :]

        logger.log(level, message)

    @QtCore.Slot(str, str)
    def set_basic_variable(self, variable: str, data: str):
        match variable:
            case 'water':
                self._pt.water = data
                logger.info('water={!r}', self._pt.water)
            case 'sand':
                self._pt.sand = data
                logger.info('sand={!r}', self._pt.sand)
            case 'environment':
                self._pt.env = data
                logger.info('environment={!r}', self._pt.env)
            case _:
                raise ValueError(variable)

    def update_analysis(self):
        page = self._winow.page('analysis')
        page.set_chart_bars(json.dumps([f'{x.capacity:.4g}' for x in self._cases]))
        page.set_table(CapacityCases.dump_json(list(self._cases)).decode())
        logger.info('capacity={}', [round(x.capacity, 3) for x in self._cases])

    @QtCore.Slot(str)
    def set_design_variables(self, text: str):
        self._cases = self._pt.calculate_cases(text)

        for idx, case in enumerate(self._cases):
            logger.info('case[{}]={!r}', idx, case)

        self.update_analysis()

    @QtCore.Slot(str)
    def write_table(self, path: str):
        path = path.removeprefix('file:///')
        xlsx.write_table(path=path, cases=self._cases)
        logger.info('saved to "{}"', path)
