from pathlib import Path
import json
from typing import Optional, List, Tuple, Dict
import logging
import uuid

logger = logging.getLogger(__name__)


class AppSettingManager:
    def __init__(self, path: Path):
        self.db_path = path
        pass

    def init_on_start(self):
        if not self.db_path.exists():
            self._save({"apps": []})

    def _load(self):
        return json.loads(self.db_path.read_text(encoding="utf-8"))

    def _save(self, db_obj: dict):
        self.db_path.write_text(
            json.dumps(db_obj, ensure_ascii=False, indent=4), encoding="utf-8"
        )

    def add_app(self, name):
        id_ = str(uuid.uuid4())
        db_obj = self._load()
        db_obj["apps"].append(
            {
                "id": id_,
                "name": name,
                "save_bak_root": None,
                "restore_bak_root": None,
                "game_save_dir": None,
                "spec": None,
                "mode": "DIR",
                "order": None,
            }
        )
        self._save(db_obj)

    def get_all_apps(self):
        db_obj = self._load()
        return db_obj["apps"]

    def get_app_setting(self, id_: str):
        db_obj = self._load()
        return self._get_app_setting(db_obj, id_)

    def _get_app_setting(self, db_obj: dict, id_: str):
        cand = [app for app in db_obj["apps"] if app["id"] == id_]
        if len(cand) == 0:
            raise ValueError(f"No such a app with id {id_}")

        return cand[0]

    def update_paths(
        self,
        id_: str,
        save_bak_root: Optional[Path] = None,
        restore_bak_root: Optional[Path] = None,
        game_save_dir: Optional[Path] = None,
    ):
        db_obj = self._load()
        update_dict = {
            "save_bak_root": str(save_bak_root),
            "restore_bak_root": str(restore_bak_root),
            "game_save_dir": str(game_save_dir),
        }
        app = self._get_app_setting(db_obj, id_)
        app.update(update_dict)

        self._save(db_obj)

    def set_mode_as_selected_files(self, id_: str, spec: str):
        db_obj = self._load()
        update_dict = {
            "mode": "SELECTED_FILES",
            "spec": spec,
        }
        app = self._get_app_setting(db_obj, id_)
        app.update(update_dict)

        self._save(db_obj)

    def set_mode_as_dir(self, id_: str):
        db_obj = self._load()
        update_dict = {"mode": "DIR", "spec": None}
        app = self._get_app_setting(db_obj, id_)
        app.update(update_dict)

        self._save(db_obj)
