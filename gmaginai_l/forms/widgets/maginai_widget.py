from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
from PySide6.QtWidgets import QDialog, QWidget
from .maginai_widget_ui import Ui_MaginaiWidget
from ..maginai_installer_message_form import MaginaiInstallerMessageForm

logger = logging.getLogger(__name__)


class MaginaiWidget(QWidget):
    def __init__(self, game_dir: Path | str, parent=None):
        super().__init__(parent)
        self.ui = Ui_MaginaiWidget()
        self.ui.setupUi(self)
        self.game_dir = Path(game_dir)

        self.ui.btn_install.clicked.connect(self.btn_install_clicked)
        # self.ui.btn_install

    def btn_install_clicked(self):
        form = MaginaiInstallerMessageForm()
        rtn = form.exec()
        if rtn == QDialog.DialogCode.Accepted:
            self.refresh_install_state()

    def refresh_install_state(self):
        # TODO: Refresh
        logger.info("Refresh")
