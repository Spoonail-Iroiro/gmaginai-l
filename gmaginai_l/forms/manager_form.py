from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
from PySide6.QtWidgets import QDialog, QWidget
from .manager_form_ui import Ui_ManagerForm
from .widgets.mods_widget import ModsWidget
from .widgets.maginai_widget import MaginaiWidget

logger = logging.getLogger(__name__)


class ManagerForm(QDialog):
    def __init__(self, profile: dict, parent=None):
        super().__init__(parent)
        self.ui = Ui_ManagerForm()
        self.ui.setupUi(self)

        self.profile = profile

        self.maginai_widget = MaginaiWidget(profile["game_dir"], self)
        self.mods_widget = ModsWidget(self)

        self.ui.stwMain.addWidget(self.maginai_widget)
        self.ui.stwMain.addWidget(self.mods_widget)
        self.ui.stwMain.setCurrentIndex(0)

        self.ui.lstMain.addItem("Mod Loader")
        self.ui.lstMain.addItem("Mods")
        self.ui.lstMain.setCurrentRow(0)
        self.ui.lstMain.currentRowChanged.connect(self.ui.stwMain.setCurrentIndex)

        self.ui.lstMain.setFixedWidth(
            self.ui.lstMain.sizeHintForColumn(0) + self.ui.lstMain.frameWidth() * 2
        )
