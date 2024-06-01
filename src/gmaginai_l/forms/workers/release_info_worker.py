from pathlib import Path
import tempfile
from typing import Optional, List, Tuple, Dict
import logging
import time
import traceback
from PySide6.QtWidgets import QDialog, QWidget, QDialogButtonBox
from PySide6.QtCore import QThreadPool, Signal, QObject, Slot
from ...core.maginai_installer import MaginaiInstaller
from ... import funcs
import requests.exceptions

logger = logging.getLogger(__name__)


class CancelError(Exception):
    pass


class ReleaseInfoWorker(QObject):
    completed = Signal(list)
    failed = Signal(str)

    def __init__(self, installer: MaginaiInstaller, parent=None):
        super().__init__(parent)

        self.installer = installer

    def run(self):
        try:
            tag_names = self.installer.get_release_tag_names(timeout=10)
            self.completed.emit(tag_names)
        except Exception as ex:
            logger.exception("")
            message = funcs.formatError(ex)
            self.failed.emit(
                self.tr(
                    "An error occured during getting release information. It might be network issue: {0}"
                ).format(message)
            )
