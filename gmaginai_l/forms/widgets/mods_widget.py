from PySide6.QtWidgets import QDialog, QWidget
from .mods_widget_ui import Ui_ModsWidget


class ModsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ModsWidget()
        self.ui.setupUi(self)
