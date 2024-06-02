from PySide6.QtGui import QIcon
from .. import dirs


def set_window_icon(window):
    window.setWindowIcon(QIcon(str(dirs.application_dir / "image" / "icon.png")))
    pass
