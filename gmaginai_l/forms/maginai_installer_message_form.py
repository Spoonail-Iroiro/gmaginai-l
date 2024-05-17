from pathlib import Path
import tempfile
from typing import Optional, List, Tuple, Dict
import logging
import time
import traceback
from PySide6.QtWidgets import QDialog, QWidget, QDialogButtonBox
from PySide6.QtCore import QThreadPool, Signal, QObject, Slot
from enum import Enum, auto
from ..core.maginai_installer import MaginaiInstaller
from .message_form_ui import Ui_MessageForm
from .maginai_install_worker import MaginaiInstallWorker


logger = logging.getLogger(__name__)


class FormState(Enum):
    CONFIRM = auto()
    INSTALLING = auto()
    FINISHED = auto()


class MaginaiInstallerMessageForm(QDialog):
    cancelWorker = Signal()

    def __init__(self, installer, tag_name_to_install: str, parent=None):
        super().__init__(parent)
        self.ui = Ui_MessageForm()
        self.ui.setupUi(self)

        self.installer = installer
        self.tag_name_to_install = tag_name_to_install

        Buttons = QDialogButtonBox.ButtonRole
        self.btn_ok = self.ui.bbx_main.addButton("OK", Buttons.AcceptRole)
        self.btn_ok.clicked.connect(self.btn_ok_clicked)
        self.btn_cancel = self.ui.bbx_main.addButton("Cancel", Buttons.RejectRole)
        self.btn_cancel.clicked.connect(self.btn_cancel_clicked)

        self.ui.txt_main.setText(f"Install mod loader 'maginai' {tag_name_to_install}?")
        self.state = FormState.CONFIRM

        self.install_worker: None | MaginaiInstallWorker = None

    def btn_ok_clicked(self):
        if self.state == FormState.CONFIRM:
            self.state = FormState.INSTALLING
            self.btn_ok.setEnabled(False)
            self._start_install(self.tag_name_to_install)
        elif self.state == FormState.FINISHED:
            self.accept()

    def btn_cancel_clicked(self):
        if self.state == FormState.CONFIRM:
            self.reject()
        elif self.state == FormState.INSTALLING:
            self._cancel_install()

    def _start_install(self, tag_name_to_install: str):
        self.install_worker = MaginaiInstallWorker(self.installer, tag_name_to_install)
        self.install_worker.notify.connect(self._install_state_notified)
        self.install_worker.finished.connect(self._on_install_finished)
        # self.cancelWorker.disconnect()
        self.cancelWorker.connect(self.install_worker.cancel)
        QThreadPool.globalInstance().start(self.install_worker.run)

    def _install_state_notified(self, text: str):
        self.ui.txt_main.setText(text)

    def _on_install_finished(self):
        self.state = FormState.FINISHED
        self.btn_ok.setEnabled(True)
        self.btn_cancel.setEnabled(False)

    def _cancel_install(self):
        if self.state == FormState.INSTALLING:
            self.cancelWorker.emit()
        else:
            self.reject()
