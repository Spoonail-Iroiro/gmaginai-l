from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
from PySide6.QtWidgets import QDialog, QWidget
from .maginai_widget_ui import Ui_MaginaiWidget
from ..maginai_installer_message_form import MaginaiInstallerMessageForm
from ...core.maginai_installer import MaginaiInstaller
from ... import config
from ... import funcs

logger = logging.getLogger(__name__)


class MaginaiWidget(QWidget):
    def __init__(self, installer: MaginaiInstaller, parent=None):
        super().__init__(parent)
        self.ui = Ui_MaginaiWidget()
        self.ui.setupUi(self)
        self.installer = installer

        self.ui.btn_install.clicked.connect(self.btn_install_clicked)

        self.refresh_install_state()
        # self.ui.btn_install

    def btn_install_clicked(self):
        try:
            tag_names = self.installer.get_release_tag_names()
        except Exception as ex:
            message = funcs.formatError(ex)
            self._display_error(
                f"An error occured during getting release information. It might be network issue: {message}"
            )
            raise
        else:
            # Install latest
            form = MaginaiInstallerMessageForm(
                self.installer,
                tag_names[0],
                parent=self,
            )
            form.exec()
            self.refresh_install_state()

    def refresh_install_state(self):
        try:
            tags_exist = self.installer.maginai_tags_exist()
            mod_exists = self.installer.get_mod_dir().exists()

            if tags_exist and mod_exists:
                message = "'maginai' installed."
            elif mod_exists:
                message = "'maginai' is not installed. ('mod' folder remains)"
            elif tags_exist:
                message = "Invalid 'maginai' installation. ('mod' folder is missing)"
            else:
                message = "'maginai' is not installed."
        except Exception as ex:
            logger.exception("")
            self._display_error(funcs.formatError(ex))
            message = "Unknown installation state. Try install to clean up."

        self._set_install_state(message)

    def _set_install_state(self, message):
        self.ui.txt_main.setText(message)

    def _display_error(self, message):
        self.ui.txt_error.setText(message)
