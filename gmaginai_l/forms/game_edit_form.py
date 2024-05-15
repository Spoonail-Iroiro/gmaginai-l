from PySide6.QtWidgets import QDialog, QWidget
from .game_edit_form_ui import Ui_GameEditForm


class GameEditForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_GameEditForm()
        self.ui.setupUi(self)
