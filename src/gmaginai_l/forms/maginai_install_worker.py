from pathlib import Path
import tempfile
from typing import Optional, List, Tuple, Dict
import logging
import time
import traceback
from PySide6.QtWidgets import QDialog, QWidget, QDialogButtonBox
from PySide6.QtCore import QThreadPool, Signal, QObject, Slot
from ..core.maginai_installer import MaginaiInstaller
from .message_form_ui import Ui_MessageForm


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
            self._set_message(self.tr("Starting..."))

            with tempfile.TemporaryDirectory(
                ignore_cleanup_errors=True
            ) as temp_dir_str:
                temp_dir = Path(temp_dir_str)

                mod_dir = self.installer.get_mod_dir()
                backup_dir = self.installer.get_backup_dir()
                mod_dir_exists = mod_dir.exists()
                if mod_dir_exists:
                    self._set_message(
                        self.tr("Making backup of existing mod folder...")
                    )
                    self.installer.backup_existing_install_by_move()

                try:
                    self._check_cancel()
                    self._set_message(self.tr("Downloading..."))
                    self.installer.set_work_dir(temp_dir)
                    zip_path = self.installer.download_by_tag_name(
                        self.tag_name_to_install
                    )
                    self._check_cancel()
                    self._set_message(self.tr("Extracting..."))
                    extracted = self.installer.unzip_to_work_temp(zip_path)

                    self._check_cancel()
                    self._set_message(self.tr("Installing..."))
                    self.installer.install_to_game(extracted)

                    self._check_cancel()
                    self._set_message(self.tr("Migrating mods from old..."))
                    if mod_dir_exists:
                        self.installer.migrate_mods(self.installer.get_backup_dir())
                except Exception:
                    try:
                        if mod_dir_exists:
                            self.installer.recover_from_backup()
                    except Exception:
                        logger.exception(f"Failed to recovery from {backup_dir}")
                        additional_error_info += self.tr(
                            "Failed to recovery old mod folder from {0}. "
                            "Please recover it manually.\n"
                        ).format(backup_dir)

                    raise

                self._set_message(
                    self.tr("Mod loader 'maginai' successfully installed.")
                )

        except CancelError as ce:
            self._set_message(self.tr("Installation is cancelled by user."))
        except Exception as ex:
            error_message = "\n".join(traceback.format_exception_only(ex))
            message = self.tr(
                "An error occured during install. Please try again.\n{0}{1}"
            ).format(additional_error_info, error_message)
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
