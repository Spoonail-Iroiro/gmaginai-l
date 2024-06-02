from pathlib import Path
import os
import shutil
from typing import Optional, List, Tuple, Dict, Callable
import traceback
import logging
from PySide6.QtWidgets import QMessageBox, QWidget
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import Qt
from .core.icon import set_window_icon

logger = logging.getLogger(__name__)


def formatError(exc: BaseException) -> str:
    return "\n".join(traceback.format_exception_only(exc))


def showConfirm(
        parent: QWidget,
        title: str,
        message: str,
):
    box = QMessageBox(parent=parent)
    box.setIcon(QMessageBox.Icon.Question)
    box.setWindowTitle(title)
    box.setText(message)
    box.setWindowFlags(
        Qt.WindowType.Dialog
        | Qt.WindowType.CustomizeWindowHint
        | Qt.WindowType.WindowTitleHint
    )

    ok_button = box.addButton("OK", QMessageBox.ButtonRole.AcceptRole)
    box.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
    box.exec()
    if box.clickedButton() == ok_button:
        return True
    else:
        return False


def showMessageOk(
        parent: QWidget,
        title: str,
        message: str,
        icon: QMessageBox.Icon = QMessageBox.Icon.NoIcon,
):
    box = QMessageBox(parent=parent)
    box.setIcon(icon)
    box.setWindowTitle(title)
    box.setText(message)
    box.setWindowFlags(
        Qt.WindowType.Dialog
        | Qt.WindowType.CustomizeWindowHint
        | Qt.WindowType.WindowTitleHint
    )

    box.addButton("OK", QMessageBox.ButtonRole.AcceptRole)
    box.exec()


def open_directory(dir_: Path):
    dir_uri = dir_.as_uri()
    QDesktopServices.openUrl(dir_uri)
