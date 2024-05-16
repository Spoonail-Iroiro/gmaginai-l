from PySide6.QtWidgets import QDialog, QWidget
from .maginai_widget_ui import Ui_MaginaiWidget


class MaginaiWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MaginaiWidget()
        self.ui.setupUi(self)
