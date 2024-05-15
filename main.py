import logging
from PySide6.QtWidgets import QApplication

# from save_backup.forms.game_select_form import GameSelectForm
from save_backup.forms.profile_form import ProfileForm
from save_backup.core.app_setting_manager import AppSettingManager
from save_backup.dirs import application_dir
import sys
import tomli

logger = logging.getLogger(__name__)


logging.basicConfig(level="INFO")
try:
    config_path = application_dir / "config.toml"
    config_dict = tomli.loads(config_path.read_text(encoding="utf-8"))

    db_path = application_dir / "data" / "db.json"

    qss_path = application_dir / "data" / "QSS" / "QtDark.qss"

    app_setting_manager = AppSettingManager(db_path)
    app_setting_manager.init_on_start()

    app = QApplication(sys.argv)

    if qss_path.exists():
        app.setStyleSheet(qss_path.read_text(encoding="utf-8"))
    else:
        raise ValueError()

    form = ProfileForm()

    form.show()
    code = app.exec_()

    sys.exit(code)

except Exception as ex:
    import traceback

    message = traceback.format_exc()
    logger.error(message)
    raise
