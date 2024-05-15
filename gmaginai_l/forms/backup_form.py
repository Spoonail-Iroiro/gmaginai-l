import shutil
from PySide6.QtWidgets import QDialog, QWidget, QMessageBox
from PySide6.QtCore import Qt
from .backup_form_ui import Ui_BackupForm
from ..core.backup_controllers import BackupControllerBase
from enum import Enum, auto


class SaveMethod(Enum):
    DEFAULT = auto()
    ARK = auto()


class BackupForm(QDialog):
    def __init__(self, controller: BackupControllerBase, parent=None):
        super().__init__(parent)
        self.ui = Ui_BackupForm()
        self.ui.setupUi(self)

        self.controller = controller

        self.ui.lblSpecial.setText(f"")

        self.list_refresh()

        self.ui.txtGameSaveDir.setText(str(self.controller.game_save_dir))
        self.ui.txtSaveBackupRoot.setText(str(self.controller.save_backup_root))

    def btnSave_clicked(self):
        msg = QMessageBox(self)
        save_tag = self.ui.txtSaveTag.text()
        backup_dir_name = self.controller.get_next_backup_dir_name(save_tag)
        msg.setText(f"{backup_dir_name}フォルダとしてセーブをバックアップします。よろしいですか？")
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        msg.setDefaultButton(QMessageBox.StandardButton.No)
        result = msg.exec_()
        if result != QMessageBox.StandardButton.Yes:
            return

        try:
            self.controller.backup(backup_dir_name)
            self.list_refresh()
        except Exception as ex:
            QMessageBox.information(self, "message", "バックアップ中にエラーが発生しました")
            # msg.exec_()
            raise
        else:
            QMessageBox.information(self, "message", "バックアップが完了しました")
            # msg.exec_()

    def btnRestore_clicked(self):
        selected = self.ui.lstMain.selectedItems()
        if len(selected) == 0:
            QMessageBox(text="リストからセーブを選択して下さい")
            return

        dir_name = selected[0].data(Qt.ItemDataRole.DisplayRole)

        msg = QMessageBox(self)
        msg.setText(f"{dir_name}フォルダを復元します。よろしいですか？")
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        msg.setDefaultButton(QMessageBox.StandardButton.No)

        result = msg.exec_()
        if result != QMessageBox.StandardButton.Yes:
            return

        try:
            self.controller.restore(dir_name)
        except Exception as ex:
            QMessageBox.information(self, "message", "復元中にエラーが発生しました")
            raise
        else:
            QMessageBox.information(self, "message", "復元が完了しました")

    def list_refresh(self):
        self.ui.lstMain.clear()

        for name in self.controller.get_existing_backup_dir_names():
            self.ui.lstMain.addItem(name)
