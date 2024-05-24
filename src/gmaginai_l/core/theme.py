from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
from .config_enum import Theme
from .. import dirs

logger = logging.getLogger(__name__)


def set_theme(app, theme: Theme):
    if theme == Theme.QT_DARK:
        app.setStyle("fusion")
        qss_path = dirs.application_dir / "QSS" / "QtDark.qss"
        app.setStyleSheet(qss_path.read_text(encoding="utf-8"))
    else:
        raise NotImplementedError()
    pass
