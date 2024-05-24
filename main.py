import logging
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTranslator, QLibraryInfo, QLocale

# from save_backup.forms.game_select_form import GameSelectForm
from gmaginai_l.forms.profile_form import ProfileForm
from gmaginai_l.dirs import application_dir
from gmaginai_l.core.profile_service import ProfileService
from gmaginai_l.core.db import get_db, set_current_db
from gmaginai_l.core.config_service import ConfigService
from gmaginai_l.core.config_enum import Language, Theme
from gmaginai_l.core.translation import set_translation
from gmaginai_l.core.theme import set_theme
import sys
import os

import tomli

logger = logging.getLogger(__name__)


logging.basicConfig(level="INFO")
try:
    # os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=2"
    # sys.argv += ['-platform', 'windows:darkmode=1']

    db_path = application_dir / "data" / "db.json"
    db = get_db(db_path)
    # set application db
    set_current_db(db)

    config = ConfigService().get_config()

    app = QApplication(sys.argv)

    set_translation(app, config.appearance.language)

    set_theme(app, config.appearance.theme)

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
