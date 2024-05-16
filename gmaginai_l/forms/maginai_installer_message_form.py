from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
import time
import traceback
from PySide6.QtWidgets import QDialog, QWidget, QDialogButtonBox
from PySide6.QtCore import QThreadPool, Signal, QObject
from enum import Enum, auto
from .message_form_ui import Ui_MessageForm


logger = logging.getLogger(__name__)


class MaginaiInstallWorker(QObject):
    notify = Signal(str)
    finished = Signal()

    def __init__(self, game_dir: Path | str, parent=None):
        super().__init__(parent)
        game_dir = Path(game_dir)

    def run(self):
        try:
            self.notify.emit("started")
            raise ValueError("Test Error")
            time.sleep(3)
            self.notify.emit("3 seconds later...")
            time.sleep(3)
            self.notify.emit("completed")
        except Exception as ex:
            error_message = "\n".join(traceback.format_exception_only(ex))
            message = (
                f"An error occured during install. Please try again.\n{error_message}"
            )
            logger.exception(message)
            self.notify.emit(message)
        finally:
            self.finished.emit()
        pass


class FormState(Enum):
    CONFIRM = auto()
    INSTALLING = auto()
    FINISHED = auto()


class MaginaiInstallerMessageForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MessageForm()
        self.ui.setupUi(self)

        Buttons = QDialogButtonBox.ButtonRole

        self.btn_ok = self.ui.bbx_main.addButton("OK", Buttons.AcceptRole)
        self.btn_ok.clicked.connect(self.btn_ok_clicked)
        self.btn_cancel = self.ui.bbx_main.addButton("Cancel", Buttons.RejectRole)
        self.btn_cancel.clicked.connect(self.btn_cancel_clicked)

        self.state = FormState.CONFIRM
        self.ui.txt_main.setText("Do you want to install mod loader 'maginai'?")

        self.install_worker: None | MaginaiInstallWorker = None

    def btn_ok_clicked(self):
        if self.state == FormState.CONFIRM:
            self.state = FormState.INSTALLING
            self.btn_ok.setEnabled(False)
            self._start_install()
        elif self.state == FormState.FINISHED:
            self.accept()

    def btn_cancel_clicked(self):
        if self.state == FormState.CONFIRM:
            self.reject()
        elif self.state == FormState.INSTALLING:
            self._cancel_install()

    def _start_install(self):
        self.install_worker = MaginaiInstallWorker(Path("~/home/downloads"))
        self.install_worker.notify.connect(self._install_state_notified)
        self.install_worker.finished.connect(self._on_install_finished)
        QThreadPool.globalInstance().start(self.install_worker.run)
        logger.info(f"Max thread: {QThreadPool.globalInstance().maxThreadCount()}")

    def _install_state_notified(self, text: str):
        self.ui.txt_main.setText(text)

    def _on_install_finished(self):
        self.state = FormState.FINISHED
        self.btn_ok.setEnabled(True)
        self.btn_cancel.setEnabled(False)

    def _cancel_install(self):
        raise NotImplementedError()
