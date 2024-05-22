from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
from PySide6.QtWidgets import QDialog, QWidget, QListWidgetItem
from PySide6.QtCore import Qt
logger = logging.getLogger(__name__)

class ShownEventWidget(QWidget):
    def shownEvent(self):
        pass
