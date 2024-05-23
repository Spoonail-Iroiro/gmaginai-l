from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
from PySide6.QtWidgets import QDialog, QWidget, QListWidgetItem
from PySide6.QtCore import Qt
from .mods_widget_ui import Ui_ModsWidget
from .shown_event_widget import ShownEventWidget
from ...core.mod_installer import ModInstaller
from ..mod_install_message_form import ModInstallMessageForm

logger = logging.getLogger(__name__)


class ModsWidget(ShownEventWidget):
    def __init__(self, mod_installer: ModInstaller, parent=None):
        super().__init__(parent)
        self.ui = Ui_ModsWidget()
        self.ui.setupUi(self)

        self.mod_installer = mod_installer
        self.current_index_memo = 0

        self.ui.lstMain.currentRowChanged.connect(self.lstMain_currentRowChanged)
        self.ui.btn_enable.clicked.connect(self.btn_enable_clicked)
        self.ui.btn_up.clicked.connect(self.btn_up_clicked)
        self.ui.btn_down.clicked.connect(self.btn_down_clicked)
        self.ui.btn_add.clicked.connect(self.btn_add_clicked)

    def refresh_mod_list(self):
        self.ui.lstMain.setCurrentRow(-1)
        self.ui.lstMain.clear()
        enabled_mods = self.mod_installer.get_enabled_mods()
        disabled_mods = self.mod_installer.get_disabled_mods()

        enabled_mods_installed = [
            mod for mod in enabled_mods if self.mod_installer.has_mod_own_folder(mod)
        ]
        if enabled_mods != enabled_mods_installed:
            # don't allow inconsistent mod installation
            self.mod_installer.set_enabled_mods(enabled_mods_installed)
            enabled_mods = self.mod_installer.get_enabled_mods()

        for mod in enabled_mods:
            mod_info = {"name": mod, "display": mod, "enabled": True}
            item = QListWidgetItem(mod_info["display"])  # type:ignore[call-overload]
            item.setData(Qt.ItemDataRole.UserRole, mod_info)
            self.ui.lstMain.addItem(item)

        for mod in disabled_mods:
            mod_info = {
                "name": mod,
                "display": mod + self.tr(" (disabled)"),
                "enabled": False,
            }
            item = QListWidgetItem(mod_info["display"])  # type: ignore[call-overload]
            item.setData(Qt.ItemDataRole.UserRole, mod_info)
            self.ui.lstMain.addItem(item)

        self.ui.lstMain.setCurrentRow(self.current_index_memo)

    def lstMain_currentRowChanged(self, index):
        if index >= 0:
            selected_item = self.ui.lstMain.item(index)
            mod_info = selected_item.data(Qt.ItemDataRole.UserRole)
            if mod_info["enabled"]:
                self.ui.btn_enable.setText(self.tr("Disable"))
                self.ui.btn_up.setEnabled(True)
                self.ui.btn_down.setEnabled(True)
            else:
                self.ui.btn_enable.setText(self.tr("Enable"))
                self.ui.btn_up.setEnabled(False)
                self.ui.btn_down.setEnabled(False)

            self.current_index_memo = index

    def btn_enable_clicked(self):
        selected_items = self.ui.lstMain.selectedItems()
        if len(selected_items) >= 1:
            selected_item = selected_items[0]
            mod_info = selected_item.data(Qt.ItemDataRole.UserRole)
            mod_name = mod_info["name"]
            if mod_info["enabled"]:
                self.mod_installer.disable_mod(mod_name)
            else:
                self.mod_installer.enable_mod(mod_name)

            self.refresh_mod_list()

            # set selected row to moved mod
            self._set_current_row_to_mod(mod_name)

        pass

    def btn_up_clicked(self):
        self.move_row(-1)

    def btn_down_clicked(self):
        self.move_row(+1)

    def move_row(self, delta):
        current_index = self.ui.lstMain.currentRow()
        if not (0 <= current_index + delta < self.ui.lstMain.count()):
            return

        items = [self.ui.lstMain.item(idx) for idx in range(self.ui.lstMain.count())]
        current_mod_name = items[current_index].data(Qt.ItemDataRole.UserRole)["name"]
        items.insert(current_index + delta, items.pop(current_index))
        enabled_mods = [
            item.data(Qt.ItemDataRole.UserRole)["name"]
            for item in items
            if item.data(Qt.ItemDataRole.UserRole)["enabled"]
        ]
        self.mod_installer.set_enabled_mods(enabled_mods)

        self.refresh_mod_list()
        # self.ui.lstMain.setCurrentRow(current_index + delta)
        self._set_current_row_to_mod(current_mod_name)

    def _set_current_row_to_mod(self, mod_name: str):
        items = [self.ui.lstMain.item(idx) for idx in range(self.ui.lstMain.count())]
        mod_names = [item.data(Qt.ItemDataRole.UserRole)["name"] for item in items]
        moved_index = mod_names.index(mod_name)
        self.ui.lstMain.setCurrentRow(moved_index)
        pass

    def btn_add_clicked(self):
        form = ModInstallMessageForm(self.mod_installer, parent=self)
        form.exec()
        self.refresh_mod_list()

    def shownEvent(self):
        self.refresh_mod_list()
