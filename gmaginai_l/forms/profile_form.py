from PySide6.QtWidgets import QDialog, QWidget, QListWidgetItem
from PySide6.QtCore import Qt
from .profile_form_ui import Ui_ProfileForm
import logging

logger = logging.getLogger(__name__)


class ProfileForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ProfileForm()
        self.ui.setupUi(self)

        items = [
            {"name": "default", "path": r"C:\hoge"},
            {"name": "2", "path": r"C:\fuga"},
        ]

        if len(items) > 0:
            self.ui.lstMain.setCurrentRow(0)

        for rec in items:
            item = QListWidgetItem(rec["name"])
            # set record as UserRole data
            item.setData(Qt.ItemDataRole.UserRole, rec)
            self.ui.lstMain.addItem(item)

        # for name in self.controller.get_profile_names():
        #     self.ui.lstMain.addItem(name)
        #

    def btnSelect_clicked(self):
        pass
        items = self.ui.lstMain.selectedItems()
        if len(items) != 0:
            profile_name = items[0].data(Qt.ItemDataRole.UserRole)
            logger.info(profile_name)

            # self.controller.set_profile(profile_name)
            # form = BackupForm(
            #     self.controller,
            #     parent=self,
            # )
            # form.exec_()
