from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
from PySide6.QtWidgets import QDialog, QWidget
from PySide6.QtCore import QTimer
from .manager_form_ui import Ui_ManagerForm
from .widgets.mods_widget import ModsWidget
from .widgets.maginai_widget import MaginaiWidget
from ..core.maginai_installer import MaginaiInstaller
from ..core.mod_installer import ModInstaller
from .widgets.shown_event_widget import ShownEventWidget
from ..core.config_service import ConfigService

logger = logging.getLogger(__name__)


class ManagerForm(QDialog):
    def __init__(self, profile: dict, parent=None):
        super().__init__(parent)
        self.ui = Ui_ManagerForm()
        self.ui.setupUi(self)

        self.profile = profile

        maginai_installer = self._get_installer()

        self.maginai_widget = MaginaiWidget(maginai_installer, parent=self)
        mod_installer = ModInstaller(maginai_installer)

        self.mods_widget = ModsWidget(mod_installer, parent=self)

        self.widgets: List[ShownEventWidget] = [self.maginai_widget, self.mods_widget]

        # To invoke stwMain.currentRowChanged
        self.ui.stwMain.setCurrentIndex(-1)
        self.ui.stwMain.addWidget(self.maginai_widget)
        self.ui.stwMain.addWidget(self.mods_widget)
        self.ui.stwMain.setCurrentIndex(0)

        self.ui.lstMain.addItem(self.tr("Mod Loader"))
        self.ui.lstMain.addItem(self.tr("Mods"))
        self.ui.lstMain.setCurrentRow(0)
        self.ui.lstMain.currentRowChanged.connect(self.ui.stwMain.setCurrentIndex)
        self.ui.stwMain.currentChanged.connect(self.stwMain_currentChanged)

        self.ui.lstMain.setFixedWidth(
            self.ui.lstMain.sizeHintForColumn(0) + self.ui.lstMain.frameWidth() * 2
        )

        self.ui.txt_header.setText(profile["name"])

        self.ui.txt_game_dir.setText(profile["game_dir"])

        self.stwMain_currentChanged(0)

    def _get_installer(self):
        config = ConfigService().get_config()
        installer = MaginaiInstaller(
            Path(self.profile["game_dir"]), config.external_source.list_release_endpoint
        )

        return installer

    def stwMain_currentChanged(self, index):
        logger.info("Shown")
        if index >= 0:
            self.widgets[index].shownEvent()

        QTimer.singleShot(0, lambda: self.adjustSize())
