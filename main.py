import logging
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTranslator, QLibraryInfo, QLocale

# from save_backup.forms.game_select_form import GameSelectForm
from gmaginai_l.forms.profile_form import ProfileForm
from gmaginai_l.core.app_setting_manager import AppSettingManager
from gmaginai_l.dirs import application_dir
from gmaginai_l.core.profile_service import ProfileService
from gmaginai_l.core.db import get_db
from gmaginai_l import config
import sys
import os

import tomli

logger = logging.getLogger(__name__)


logging.basicConfig(level="INFO")
try:
    # os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=2"
    # sys.argv += ['-platform', 'windows:darkmode=1']
    config.load_from_file(application_dir / "config.toml")

    db_path = application_dir / "data" / "db.json"
    db = get_db(db_path)

    qss_path = application_dir / "QSS" / "QtDark.qss"

    app = QApplication(sys.argv)

    app.setStyle("fusion")
    if qss_path.exists():
        app.setStyleSheet(qss_path.read_text(encoding="utf-8"))
    else:
        raise ValueError()

    translation_file_path = (
        application_dir / "_internal" / "content_translation" / "gmaginai-l_ja.qm"
    )
    translator = QTranslator(app)
    translator.load(translation_file_path.name, str(translation_file_path.parent))
    app.installTranslator(translator)

    profile_service = ProfileService(db)
    form = ProfileForm(profile_service)

    form.show()
    code = app.exec()

    sys.exit(code)

except Exception as ex:
    import traceback

    message = traceback.format_exc()
    logger.error(message)
    raise
