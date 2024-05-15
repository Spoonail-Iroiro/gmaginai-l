import logging
from PySide6.QtWidgets import QApplication

# from save_backup.forms.game_select_form import GameSelectForm
from gmaginai_l.forms.profile_form import ProfileForm
from gmaginai_l.core.app_setting_manager import AppSettingManager
from gmaginai_l.dirs import application_dir
from gmaginai_l.core.profile_service import ProfileService
from gmaginai_l.core.db import get_db
import sys
import tomli

logger = logging.getLogger(__name__)


logging.basicConfig(level="INFO")
try:
    config_path = application_dir / "config.toml"
    config_dict = tomli.loads(config_path.read_text(encoding="utf-8"))

    db_path = application_dir / "data" / "db.json"
    db = get_db(db_path)

    qss_path = application_dir / "data" / "QSS" / "QtDark.qss"

    app_setting_manager = AppSettingManager(db_path)
    app_setting_manager.init_on_start()

    app = QApplication(sys.argv)

    if qss_path.exists():
        app.setStyleSheet(qss_path.read_text(encoding="utf-8"))
    else:
        raise ValueError()

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
