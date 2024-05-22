from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
from enum import Enum, auto
from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QDialogButtonBox,
    QPushButton,
    QMessageBox,
    QFileDialog,
)
from PySide6.QtCore import QThreadPool, Signal, QObject, Slot
from .message_form_ui import Ui_MessageForm
from .message_form import MessageFormBase
from ..core.maginai_installer import MaginaiInstaller
from ..core.mod_installer import ModInstaller
from .. import funcs

logger = logging.getLogger(__name__)


class FormState(Enum):
    SELECT_MOD = auto()
    FINISHED = auto()


class CancelError(Exception):
    pass


class ModInstallMessageForm(MessageFormBase):
    def __init__(self, installer: ModInstaller, parent=None):
        title = f"Install Mod"
        super().__init__(self.tr(title), parent)

        self.installer = installer

        (
            self.btn_ok,
            self.btn_cancel,
            self.btn_yes_show_extracted,
            self.btn_no_show_extracted,
        ) = tuple(
            self.set_buttons(
                [
                    (self.tr("OK"), self.Buttons.AcceptRole),
                    (self.tr("Cancel"), self.Buttons.RejectRole),
                    (
                        self.tr("Yes, I want to see what's inside the zip"),
                        self.Buttons.AcceptRole,
                    ),
                    (self.tr("No, just discard it"), self.Buttons.RejectRole),
                ]
            )
        )
        self.btn_ok.clicked.connect(self.btn_ok_clicked)
        self.btn_cancel.clicked.connect(self.rejectDialog)
        self.btn_yes_show_extracted.setVisible(False)
        self.btn_no_show_extracted.setVisible(False)

        self.ui.txt_main.setText(
            f"Select init.js in mod's main folder or distribution zip."
            "\n(If the selected mod is already installed, it will be updated)"
        )
        self.state = FormState.SELECT_MOD

    def btn_ok_clicked(self):
        if self.state == FormState.SELECT_MOD:
            selected_path = self._select_file()
            if selected_path is None:
                return
            self._install_new(selected_path)
            self.state = FormState.FINISHED
            self.btn_cancel.setEnabled(False)
        elif self.state == FormState.FINISHED:
            self.acceptDialog()

    def _select_file(self) -> Path | None:
        fdialog = QFileDialog(self)
        fdialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        fdialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        fdialog.setNameFilter("zip file (*.zip);init.js (init.js)")
        rtn = fdialog.exec()

        filepaths = fdialog.selectedFiles()
        if rtn == QDialog.DialogCode.Accepted and len(filepaths) > 0:
            return Path(filepaths[0])

    def _install_new(self, path: Path):
        # TODO: more suitable file classification
        if path.suffix == ".zip":
            try:
                extracted = self.installer.unzip_to_work_temp(path)
                mod_dir = self.installer.search_mod_main_folder(extracted)
                if mod_dir is None:
                    raise ValueError(f"No mod's main folder found")
            except Exception as ex:
                error_message = (
                    "Unabled to extract mod from the distribution zip. "
                    "Please unzip it manually and specify init.js.\n"
                    f"{funcs.formatError(ex)}"
                )
                self.ui.txt_main.setText(self.tr(error_message))
                logger.exception(error_message)
                self.move_to_finish()
                pass
        else:
            if path.name != "init.js":
                isOk = funcs.showConfirm(
                    self,
                    self.tr("Confirm"),
                    "The selected file is not init.js, so you might selected wrong mod's main folder. Proceed anyway?",
                )
                if not isOk:
                    self.rejectDialog()
                    return

            mod_dir = path.parent

        mod_name = mod_dir.name
        isOk = funcs.showConfirm(
            self, self.tr("Confirm"), f"Mod '{mod_name}' will be installed. OK?"
        )
        if not isOk:
            self.rejectDialog()
            return

        self.installer.install_mod(mod_dir)

        self.move_to_successfully_installed(mod_name)

    def _uninstall(self):
        try:
            self.installer.uninstall_all() if self.is_all else self.installer.uninstall_only_tags()
            self.ui.txt_main.setText("Uninstalled 'maginai' successfully.")
        except Exception as ex:
            self.ui.txt_main.setText(
                f"An error occured during uninstall.\n{funcs.formatError(ex)}"
            )
            logger.exception("")

    def move_to_finish(self):
        self.state = FormState.FINISHED
        self.btn_ok.setVisible(True)
        self.btn_ok.setEnabled(True)
        self.btn_cancel.setVisible(True)
        self.btn_cancel.setEnabled(False)

    def move_to_successfully_installed(self, mod_name):
        self.ui.txt_main.setText(f"Installed '{mod_name}' successfully.")
