from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
from PySide6.QtWidgets import QDialog, QWidget, QFileDialog, QMessageBox
from .profile_edit_form_ui import Ui_ProfileEditForm
from .. import funcs
from PySide6.QtCore import Qt

logger = logging.getLogger(__name__)


class ProfileEditForm(QDialog):
    def __init__(
            self,
            name: str = "",
            game_dir: str | Path = "",
            parent=None,
    ):
        super().__init__(parent)
        self.ui = Ui_ProfileEditForm()
        self.ui.setupUi(self)

        self.name = name
        self.game_dir = game_dir
        self.ui.txt_name.setText(name)
        self.ui.txt_game_dir.setText(str(game_dir))

        self.ui.btn_ok.clicked.connect(self.btn_ok_clicked)
        self.ui.btn_cancel.clicked.connect(self.reject)
        self.ui.btn_open.clicked.connect(self.btn_open_clicked)

        self.ui.btn_detect_steam_version.clicked.connect(self.btn_detect_steam_version)

        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.WindowTitleHint
        )

    def btn_ok_clicked(self):
        game_dir = Path(self.ui.txt_game_dir.text())

        if self.ui.txt_name.text().strip() == "":
            funcs.showMessageOk(
                self, self.tr("Warning"), self.tr("Name must not be empty"), QMessageBox.Icon.Warning
            )
            return

        if not (game_dir / "Game.exe").exists():
            isOk = funcs.showConfirm(
                self,
                self.tr("Confirm"),
                self.tr(
                    "Game.exe does not exist in {0}. "
                    "You may have specified wrong directory. Proceed anyway?"
                ).format(game_dir),
            )
            if not isOk:
                return

        self.name = self.ui.txt_name.text()
        self.game_dir = game_dir

        self.accept()

    def btn_open_clicked(self):
        # game_dir = QFileDialog.getExistingDirectory(
        #     self,
        #     "Select ",
        #     options=QFileDialog.Option.DontResolveSymlinks
        #     | QFileDialog.Option.ShowDirsOnly,
        # )
        fdialog = QFileDialog(self)
        fdialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        fdialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        fdialog.setNameFilter("Game.exe (*.*)")
        rtn = fdialog.exec()

        filepaths = fdialog.selectedFiles()
        if rtn == QDialog.DialogCode.Accepted and len(filepaths) > 0:
            game_exe_path = Path(filepaths[0])
            game_dir = game_exe_path.parent

            self.ui.txt_game_dir.setText(str(game_dir))

    # def btn_steam
    def btn_detect_steam_version(self):
        PATH = Path(r"C:\Program Files (x86)\Steam\steamapps\common\isekainosouzousha")
        if PATH.exists():
            self.ui.txt_game_dir.setText(str(PATH))
            self.ui.txt_name.setText("steam")
