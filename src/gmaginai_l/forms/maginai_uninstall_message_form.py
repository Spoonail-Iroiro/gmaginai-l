from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
from enum import Enum, auto
from PySide6.QtWidgets import QDialog, QWidget, QDialogButtonBox
from PySide6.QtCore import QThreadPool, Signal, QObject, Slot
from .message_form_ui import Ui_MessageForm
from .message_form import MessageFormBase
from ..core.maginai_installer import MaginaiInstaller
from .. import funcs

logger = logging.getLogger(__name__)


class FormState(Enum):
    CONFIRM = auto()
    FINISHED = auto()


class MaginaiUninstallMessageForm(MessageFormBase):
    def __init__(self, installer: MaginaiInstaller, is_all: bool, parent=None):
        uninstall_type = "(all)" if is_all else "(only tags)"
        title = f"Uninstall {uninstall_type}"
        super().__init__(self.tr(title), parent)

        self.is_all = is_all
        self.installer = installer

        self.btn_ok, self.btn_cancel = tuple(
            self.set_buttons(
                [
                    (self.tr("OK"), self.Buttons.AcceptRole),
                    (self.tr("Cancel"), self.Buttons.RejectRole),
                ]
            )
        )
        self.btn_ok.clicked.connect(self.btn_ok_clicked)
        self.btn_cancel.clicked.connect(self.rejectDialog)

        if self.is_all:
            mod_dir_message = "'mod' folder will be removed. This can't be reverted."
        else:
            mod_dir_message = "'mod' folder will remain."

        self.ui.txt_main.setText(f"Uninstall 'maginai'? {mod_dir_message}")
        self.state = FormState.CONFIRM

    def btn_ok_clicked(self):
        if self.state == FormState.CONFIRM:
            self._uninstall()
            self.state = FormState.FINISHED
            self.btn_cancel.setEnabled(False)
        elif self.state == FormState.FINISHED:
            self.acceptDialog()

    def _uninstall(self):
        try:
            self.installer.uninstall_all() if self.is_all else self.installer.uninstall_only_tags()
            self.ui.txt_main.setText("Uninstalled 'maginai' successfully.")
        except Exception as ex:
            self.ui.txt_main.setText(
                f"An error occured during uninstall.\n{funcs.formatError(ex)}"
            )
            logger.exception("")
