import os
import sys
from pathlib import Path

from loguru import logger
from PySide6 import QtQml, QtWidgets
from rich.logging import RichHandler

from ptes.controller import Controller

if __name__ == '__main__':
    logger.remove()
    logger.add(RichHandler(log_time_format='[%X]'), level=10, format='{message}')

    root = Path(__file__).parent
    qtdir = root / 'qt'
    qml = qtdir / 'main.qml'
    os.environ['QT_QUICK_CONTROLS_CONF'] = str(qtdir / 'qtquickcontrols2.conf')

    app = QtWidgets.QApplication(sys.argv)

    engine = QtQml.QQmlApplicationEngine()
    engine.quit.connect(app.quit)
    engine.load(qml)

    try:
        window = engine.rootObjects()[0]
    except IndexError:
        msg = f'Failed to load QML "{qml}"'
        raise RuntimeError(msg) from None

    controller = Controller(window)  # type: ignore[arg-type]
    context = engine.rootContext()
    context.setContextProperty('controller', controller)

    sys.exit(app.exec())
