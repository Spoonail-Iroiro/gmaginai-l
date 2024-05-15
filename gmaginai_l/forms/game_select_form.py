from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
from PySide6.QtWidgets import QDialog, QWidget, QListWidgetItem
from PySide6.QtCore import Qt
from .game_select_form_ui import Ui_GameSelectForm
from ..core.app_setting_manager import AppSettingManager

logger = logging.getLogger(__name__)


class GameSelectForm(QDialog):
    def __init__(self, app_setting_manager: AppSettingManager, parent=None):
        super().__init__(parent)
        self.ui = Ui_GameSelectForm()
        self.ui.setupUi(self)

        self.app_setting_manager = app_setting_manager

        apps = self.app_setting_manager.get_all_apps()

        for app in apps:
            item = QListWidgetItem(app["name"])
            # set record as UserRole data
            item.setData(Qt.ItemDataRole.UserRole, app)
            self.ui.lstMain.addItem(item)

        self.ui.btn_select.clicked.connect(self.btn_select_clicked)

    def btn_select_clicked(self):
        items = self.ui.lstMain.selectedIndexes()
        if len(items) != 0:
            # get data as UserRole to get record
            app = items[0].data(Qt.ItemDataRole.UserRole)
            logger.info(app)
        pass
