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
from .. import config


logger = logging.getLogger(__name__)


class CancelError(Exception):
    pass


class MaginaiInstallWorker(QObject):
    notify = Signal(str)
    finished = Signal()

    def __init__(
        self, installer: MaginaiInstaller, tag_name_to_install: str, parent=None
    ):
        super().__init__(parent)

        self.installer = installer
        self.tag_name_to_install = tag_name_to_install

        self.isCanceled = False

    def run(self):
        additional_error_info = ""
        try:
            self._set_message("Starting...")

            with tempfile.TemporaryDirectory(
                ignore_cleanup_errors=True
            ) as temp_dir_str:
                temp_dir = Path(temp_dir_str)

                mod_dir = self.installer.get_mod_dir()
                backup_dir = self.installer.get_backup_dir()
                mod_dir_exists = mod_dir.exists()
                if mod_dir_exists:
                    self._set_message("Making backup of existing mod folder...")
                    self.installer.backup_existing_install_by_move()

                try:
                    self._check_cancel()
                    self._set_message("Downloading...")
                    self.installer.set_work_dir(temp_dir)
                    zip_path = self.installer.download_by_tag_name(
                        self.tag_name_to_install
                    )
                    self._check_cancel()
                    self._set_message("Extracting...")
                    extracted = self.installer.unzip_to_work_temp(zip_path)

                    self._check_cancel()
                    self._set_message("Installing...")
                    self.installer.install_to_game(extracted)

                    self._check_cancel()
                    self._set_message("Migrating mods from old...")
                    if mod_dir_exists:
                        self.installer.migrate_mods(self.installer.get_backup_dir())
                except Exception:
                    try:
                        if mod_dir_exists:
                            self.installer.recover_from_backup()
                    except Exception:
                        logger.exception(f"Failed to recovery from {backup_dir.name}")
                        additional_error_info += (
                            f"Failed to recovery old mod folder from {backup_dir}."
                            " Please recover it manually\n"
                        )

                    raise

                self._set_message("Mod loader 'maginai' successfully installed.")

        except CancelError as ce:
            self._set_message("Installation is cancelled by user.")
        except Exception as ex:
            error_message = "\n".join(traceback.format_exception_only(ex))
            message = (
                f"An error occured during install. Please try again.\n{error_message}"
            )
            logger.exception(message)
            self.notify.emit(message)
        finally:
            self.finished.emit()

    def _check_cancel(self):
        if self.isCanceled:
            raise CancelError()

    def _set_message(self, message: str):
        self.notify.emit(message)

    @Slot()
    def cancel(self):
        self.isCanceled = True


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
