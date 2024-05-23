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
from .message_form import MessageFormBase
from .maginai_install_worker import MaginaiInstallWorker


logger = logging.getLogger(__name__)


class FormState(Enum):
    CONFIRM = auto()
    INSTALLING = auto()
    FINISHED = auto()


class MaginaiInstallMessageForm(MessageFormBase):
    cancelWorker = Signal()

    def __init__(self, installer, tag_name_to_install: str, parent=None):
        super().__init__(self.tr("Install"), parent)
        self.installer = installer
        self.tag_name_to_install = tag_name_to_install

        self.btn_ok, self.btn_cancel = tuple(
            self.set_buttons(
                [
                    (self.tr("OK"), self.Buttons.AcceptRole),
                    (self.tr("Cancel"), self.Buttons.RejectRole),
                ]
            )
        )
        self.btn_ok.clicked.connect(self.btn_ok_clicked)
        self.btn_cancel.clicked.connect(self.btn_cancel_clicked)

        self.set_message(
            self.tr("Install mod loader 'maginai' {0}?").format(tag_name_to_install)
        )
        self.state = FormState.CONFIRM

        self.install_worker: None | MaginaiInstallWorker = None

    def btn_ok_clicked(self):
        if self.state == FormState.CONFIRM:
            self.state = FormState.INSTALLING
            self.btn_ok.setEnabled(False)
            self._start_install(self.tag_name_to_install)
        elif self.state == FormState.FINISHED:
            self.acceptDialog()

    def btn_cancel_clicked(self):
        if self.state == FormState.CONFIRM:
            self.rejectDialog()
        elif self.state == FormState.INSTALLING:
            self._cancel_install()

    def _start_install(self, tag_name_to_install: str):
        self.install_worker = MaginaiInstallWorker(self.installer, tag_name_to_install)
        self.install_worker.notify.connect(self._install_state_notified)
        self.install_worker.finished.connect(self._on_install_finished)
        self.cancelWorker.connect(self.install_worker.cancel)
        QThreadPool.globalInstance().start(self.install_worker.run)

    def _install_state_notified(self, text: str):
        self.set_message(text)

    def _on_install_finished(self):
        self.state = FormState.FINISHED
        self.btn_ok.setEnabled(True)
        self.btn_cancel.setEnabled(False)

    def _cancel_install(self):
        if self.state == FormState.INSTALLING:
            self.cancelWorker.emit()
        else:
            self.rejectDialog()
