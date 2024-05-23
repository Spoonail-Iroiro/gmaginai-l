from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
from PySide6.QtWidgets import QDialog, QWidget, QDialogButtonBox, QPushButton
from PySide6.QtCore import Qt, Slot, QTimer
from .message_form_ui import Ui_MessageForm


logger = logging.getLogger(__name__)


class MessageFormBase(QDialog):
    """Extended no close button custom message form

    Call acceptDialog or rejectDialog to close window, otherwise you can't.

    """

    Buttons = QDialogButtonBox.ButtonRole

    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.ui = Ui_MessageForm()
        self.ui.setupUi(self)

        self.setWindowTitle(title)

        # TODO: Ubuntu環境では変化なし
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.CustomizeWindowHint
            # Qt.WindowType.FramelessWindowHint
            # self.windowFlags()
            # | Qt.WindowType.CustomizeWindowHint
            # & ~Qt.WindowType.WindowCloseButtonHint
            # & ~Qt.WindowType.WindowTitleHint
        )

        # block closing other than accept/reject
        self._closeOk = False

    def set_buttons(
        self, button_info_list: List[Tuple[str, QDialogButtonBox.ButtonRole]]
    ) -> List[QPushButton]:
        rtn = []
        for name, role in button_info_list:
            button = self.ui.bbx_main.addButton(name, role)
            rtn.append(button)

        return rtn

    def acceptDialog(self):
        self._closeOk = True
        self.accept()

    def rejectDialog(self):
        self._closeOk = True
        self.reject()

    def accept(self):
        if self._closeOk:
            super().accept()

    def reject(self):
        if self._closeOk:
            super().reject()

    def closeEvent(self, ev):
        if self._closeOk:
            ev.accept()

        ev.ignore()

    def set_message(self, message: str):
        self.ui.txt_main.setText(message)
        QTimer.singleShot(0, lambda: self.adjustSize())
