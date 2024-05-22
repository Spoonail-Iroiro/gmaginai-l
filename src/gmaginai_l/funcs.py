from pathlib import Path
import os
import shutil
from typing import Optional, List, Tuple, Dict, Callable
import logging
from PySide6.QtWidgets import QMessageBox, QWidget
import traceback

logger = logging.getLogger(__name__)


def formatError(exc: BaseException) -> str:
    return "\n".join(traceback.format_exception_only(exc))


def showConfirm(
    parent: QWidget,
    title: str,
    message: str,
):
    box = QMessageBox()
    box.setIcon(QMessageBox.Icon.Question)
    box.setWindowTitle(title)
    box.setText(message)
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
    box = QMessageBox()
    box.setIcon(icon)
    box.setWindowTitle(title)
    box.setText(message)
    box.addButton("OK", QMessageBox.ButtonRole.AcceptRole)
    box.exec()


def open_directory(dir_: Path):
    raise NotImplementedError()
