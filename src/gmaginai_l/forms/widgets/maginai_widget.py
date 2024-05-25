import subprocess
from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
from PySide6.QtWidgets import QDialog, QWidget
from .shown_event_widget import ShownEventWidget
from .maginai_widget_ui import Ui_MaginaiWidget
from ..maginai_install_message_form import MaginaiInstallMessageForm
from ...core.maginai_installer import MaginaiInstaller
from ..maginai_uninstall_message_form import MaginaiUninstallMessageForm
from ... import funcs
from ...core.coaw_launcher import CoAWLauncher

logger = logging.getLogger(__name__)


class MaginaiWidget(ShownEventWidget):
    def __init__(self, installer: MaginaiInstaller, parent=None):
        super().__init__(parent)
        self.ui = Ui_MaginaiWidget()
        self.ui.setupUi(self)
        self.installer = installer

        self.ui.btn_install.clicked.connect(self.btn_install_clicked)
        self.ui.btn_uninstall_only_tags.clicked.connect(
            self.btn_uninstall_only_tags_clicked
        )
        self.ui.btn_uninstall_all.clicked.connect(self.btn_uninstall_all_clicked)
        self.ui.btn_start_game.clicked.connect(self.btn_start_game_clicked)
        self.ui.btn_start_game_with_console.clicked.connect(self.btn_start_game_with_console_clicked)

        self.refresh_install_state()
        # self.ui.btn_install

    def btn_install_clicked(self):
        try:
            tag_names = self.installer.get_release_tag_names()
        except Exception as ex:
            message = funcs.formatError(ex)
            self._display_error(
                self.tr(
                    "An error occured during getting release information. It might be network issue: {0}"
                ).format(message)
            )
            raise
        else:
            # Install latest
            form = MaginaiInstallMessageForm(
                self.installer,
                tag_names[0],
                parent=self,
            )
            form.exec()
            self.refresh_install_state()

    def btn_uninstall_only_tags_clicked(self):
        form = MaginaiUninstallMessageForm(self.installer, False)
        form.exec()
        self.refresh_install_state()

    def btn_uninstall_all_clicked(self):
        form = MaginaiUninstallMessageForm(self.installer, True)
        form.exec()
        self.refresh_install_state()

    def refresh_install_state(self):
        try:
            tags_exist = self.installer.maginai_tags_exist()
            mod_exists = self.installer.get_mod_dir().exists()
            self._set_all_maginai_buttons_enabled()

            if tags_exist and mod_exists:
                message = self.tr("'maginai' installed.")
            elif mod_exists:
                message = self.tr("'maginai' is not installed. ('mod' folder remains)")
                self.ui.btn_uninstall_only_tags.setEnabled(False)
            elif tags_exist:
                message = self.tr(
                    "Invalid 'maginai' installation. ('mod' folder is missing)"
                )
            else:
                message = self.tr("'maginai' is not installed.")
                self.ui.btn_uninstall_only_tags.setEnabled(False)
                self.ui.btn_uninstall_all.setEnabled(False)
        except Exception as ex:
            logger.exception("")
            self._display_error(funcs.formatError(ex))
            message = self.tr("Unknown installation state. Try install to clean up.")

        self._set_install_state(message)

    def _set_all_maginai_buttons_enabled(self):
        self.ui.btn_install.setEnabled(True)
        self.ui.btn_uninstall_only_tags.setEnabled(True)
        self.ui.btn_uninstall_all.setEnabled(True)

    def _set_install_state(self, message):
        self.ui.txt_main.setText(message)

    def btn_start_game_clicked(self):
        CoAWLauncher().launch(self.installer.game_dir)

    def btn_start_game_with_console_clicked(self):
        CoAWLauncher().launch_with_dev_console(self.installer.game_dir)

    def _display_error(self, message):
        self.ui.txt_error.setText(message)

    def shownEvent(self):
        pass
