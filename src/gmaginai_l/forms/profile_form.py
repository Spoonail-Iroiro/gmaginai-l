from pathlib import Path
from typing import Optional, List, Tuple, Dict
from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QListWidgetItem,
    QMessageBox,
    QApplication,
)
from PySide6.QtCore import Qt
from .profile_form_ui import Ui_ProfileForm
from .profile_edit_form import ProfileEditForm
from .manager_form import ManagerForm
from ..core.profile_service import ProfileService
from .. import funcs
from ..core.config_enum import Language
from ..core.config_service import ConfigService
from ..core.translation import set_translation
import logging

logger = logging.getLogger(__name__)


class ProfileForm(QDialog):
    def __init__(self, profile_service: ProfileService, parent=None):
        super().__init__(parent)
        self.ui = Ui_ProfileForm()
        self.ui.setupUi(self)

        self.profile_service = profile_service

        self.refresh_list()

        if self.ui.lstMain.count() > 0:
            self.ui.lstMain.setCurrentRow(0)

        self.ui.btnSelect.clicked.connect(self.btn_select_clicked)
        self.ui.btn_add.clicked.connect(self.btn_add_clicked)
        self.ui.btn_edit.clicked.connect(self.btn_edit_clicked)
        self.ui.btn_delete.clicked.connect(self.btn_delete_clicked)

        config = ConfigService().get_config()
        i = 0
        current_index = -1
        for ln in Language:
            self.ui.cmb_language.addItem(ln.value, ln)
            if config.appearance.language == ln:
                current_index = i
            i += 1

        self.ui.cmb_language.setCurrentIndex(current_index)

        self.ui.cmb_language.currentIndexChanged.connect(
            self.cmb_language_current_index_changed
        )

        # for name in self.controller.get_profile_names():
        #     self.ui.lstMain.addItem(name)
        #

    def refresh_list(self):
        selected_index = self.ui.lstMain.currentRow()
        self.ui.lstMain.clear()
        items = self.profile_service.get_all_profile()

        for rec in items:
            item = QListWidgetItem(rec["name"])
            # set record as UserRole data
            item.setData(Qt.ItemDataRole.UserRole, rec)
            self.ui.lstMain.addItem(item)

        if selected_index >= 0:
            selected_index = max(0, min(selected_index, self.ui.lstMain.count() - 1))
            self.ui.lstMain.setCurrentRow(selected_index)

    def _get_selected_item(self) -> Optional[dict]:
        items = self.ui.lstMain.selectedItems()
        if len(items) != 0:
            profile = items[0].data(Qt.ItemDataRole.UserRole)
            return profile
        else:
            return None

    def btn_select_clicked(self):
        items = self.ui.lstMain.selectedItems()
        if len(items) != 0:
            profile = items[0].data(Qt.ItemDataRole.UserRole)
            form = ManagerForm(profile, self)
            form.exec()

            # self.controller.set_profile(profile_name)
            # form = BackupForm(
            #     self.controller,
            #     parent=self,
            # )
            # form.exec_()

    def btn_add_clicked(self):
        form = ProfileEditForm(parent=self)
        rtn = form.exec()
        if rtn == QDialog.DialogCode.Accepted:
            self.profile_service.add_profile(form.name, str(form.game_dir))
            self.refresh_list()

    def btn_edit_clicked(self):
        profile = self._get_selected_item()
        if profile is not None:
            form = ProfileEditForm(profile["name"], profile["game_dir"], parent=self)
            rtn = form.exec()
            if rtn == QDialog.DialogCode.Accepted:
                self.profile_service.update_profile(
                    profile["id"], form.name, str(form.game_dir)
                )
                self.refresh_list()

    def btn_delete_clicked(self):
        profile = self._get_selected_item()
        if profile is not None:
            profile_name = profile["name"]
            isOk = funcs.showConfirm(
                self,
                self.tr("Confirm"),
                self.tr("Do you really want to delete the profile '{0}'?").format(
                    profile_name
                ),
            )
            if isOk:
                self.profile_service.remove_profile(profile["id"])
                self.refresh_list()

    def cmb_language_current_index_changed(self, index):
        service = ConfigService()
        config = service.get_config()
        language = self.ui.cmb_language.itemData(index)
        config.appearance.language = language
        service.save_config(config)
        set_translation(QApplication.instance(), language)
        self.ui.retranslateUi(self)
        # logger.info(language)
