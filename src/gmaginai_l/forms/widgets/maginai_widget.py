import subprocess
from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
from PySide6.QtWidgets import QDialog, QWidget
from PySide6.QtCore import QThreadPool
from .shown_event_widget import ShownEventWidget
from .maginai_widget_ui import Ui_MaginaiWidget
from ..maginai_install_message_form import MaginaiInstallMessageForm
from ...core.maginai_installer import MaginaiInstaller
from ..maginai_uninstall_message_form import MaginaiUninstallMessageForm
from ... import funcs
from ...core.coaw_launcher import CoAWLauncher
from ..workers.release_info_worker import ReleaseInfoWorker

logger = logging.getLogger(__name__)


class MaginaiWidget(ShownEventWidget):
    def __init__(self, installer: MaginaiInstaller, parent=None):
        super().__init__(parent)
        self.ui = Ui_MaginaiWidget()
        self.ui.setupUi(self)

        self.installer = installer
        self.release_info_worker = ReleaseInfoWorker(self.installer, self)
        self.release_info_requested = False
        self.tag_names: List[str] | None = None

        self.ui.btn_install.clicked.connect(self.btn_install_clicked)
        self.ui.btn_open_mod_folder.clicked.connect(self.btn_open_mod_folder_clicked)
        self.ui.btn_uninstall_only_tags.clicked.connect(
            self.btn_uninstall_only_tags_clicked
        )
        self.ui.btn_uninstall_all.clicked.connect(self.btn_uninstall_all_clicked)
        self.ui.btn_start_game.clicked.connect(self.btn_start_game_clicked)
        self.ui.btn_start_game_with_console.clicked.connect(
            self.btn_start_game_with_console_clicked
        )

        self.refresh_install_state()
        # self.ui.btn_install

    def btn_install_clicked(self):
        tag_name = self.ui.cmb_tag.currentText()
        # Install latest
        form = MaginaiInstallMessageForm(
            self.installer,
            tag_name,
            parent=self,
        )
        form.exec()
        self.refresh_install_state()

    def btn_open_mod_folder_clicked(self):
        funcs.open_directory(self.installer.get_mod_dir())

    def btn_uninstall_only_tags_clicked(self):
        form = MaginaiUninstallMessageForm(self.installer, False)
        form.exec()
        self.refresh_install_state()

    def btn_uninstall_all_clicked(self):
        form = MaginaiUninstallMessageForm(self.installer, True)
        form.exec()
        self.refresh_install_state()

    def _get_version_text(self):
        try:
            version = self.installer.get_version()
            version = version if version is not None else "<unknown version>"
        except Exception:
            version = "<unknown version>"

        return version

    def refresh_install_state(self):
        try:
            tags_exist = self.installer.maginai_tags_exist()
            mod_exists = self.installer.get_mod_dir().exists()
            version = self._get_version_text()
            self._set_all_maginai_buttons_enabled()
            # disable install (online) when can't access release
            self.ui.btn_install.setEnabled(self.tag_names is not None)

            if tags_exist and mod_exists:
                message = self.tr("'maginai' v{0} is installed.").format(version)
            elif mod_exists:
                message = self.tr("'maginai' is not installed. (mods are present)")
                self.ui.btn_uninstall_only_tags.setEnabled(False)
            elif tags_exist:
                message = self.tr(
                    "Invalid 'maginai' installation. ('mod' folder is missing)"
                )
                self.ui.btn_open_mod_folder.setEnabled(False)
            else:
                message = self.tr("'maginai' is not installed.")
                self.ui.btn_uninstall_only_tags.setEnabled(False)
                self.ui.btn_uninstall_all.setEnabled(False)
                self.ui.btn_open_mod_folder.setEnabled(False)
            self._clear_error()
        except Exception as ex:
            logger.exception("")
            self._display_error(funcs.formatError(ex))
            message = self.tr("Unknown installation state. Try install to clean up.")

        self._set_install_state(message)

    def _set_all_maginai_buttons_enabled(self):
        self.ui.btn_install.setEnabled(True)
        self.ui.btn_open_mod_folder.setEnabled(True)
        self.ui.btn_uninstall_only_tags.setEnabled(True)
        self.ui.btn_uninstall_all.setEnabled(True)
        self.ui.btn_start_game.setEnabled(True)
        self.ui.btn_start_game_with_console.setEnabled(True)

    def _set_install_state(self, message):
        self.ui.txt_main.setText(message)

    def btn_start_game_clicked(self):
        CoAWLauncher().launch(self.installer.game_dir)

    def btn_start_game_with_console_clicked(self):
        CoAWLauncher().launch_with_dev_console(self.installer.game_dir)

    def _display_error(self, message):
        self.ui.txt_error.setVisible(True)
        self.ui.txt_error.setText(message)

    def _clear_error(self):
        self.ui.txt_error.setVisible(False)
        self.ui.txt_error.setText("")

    def shownEvent(self):
        pass

    def showEvent(self, event):
        super().showEvent(event)
        # request only once
        if not self.release_info_requested:
            self.release_info_worker.completed.connect(
                self.release_info_worker_completed
            )
            self.release_info_worker.failed.connect(self._display_error)
            QThreadPool.globalInstance().start(self.release_info_worker.run)
            self.release_info_requested = True

    def release_info_worker_completed(self, tag_names: List[str]):
        logger.info(f"tag name received: {tag_names}")
        self.tag_names = tag_names
        self.ui.btn_install.setEnabled(True)
        self.ui.cmb_tag.clear()
        for tag_name in tag_names:
            self.ui.cmb_tag.addItem(tag_name)
        self.ui.cmb_tag.setCurrentIndex(0)
