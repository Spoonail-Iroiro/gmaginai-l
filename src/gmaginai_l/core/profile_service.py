from pathlib import Path
import uuid
from tinydb import TinyDB, Query
from typing import Optional, List, Tuple, Dict, Union
import logging

logger = logging.getLogger(__name__)


class ProfileService:
    def __init__(self, db: TinyDB):
        self.db = db
        self.profile_table = self.db.table("profile")

    def add_profile(self, name: str, game_dir: Union[Path, str]):
        id_ = str(uuid.uuid4())
        self.profile_table.insert({"id": id_, "name": name, "game_dir": str(game_dir)})
        return id_

    def get_all_profile(self):
        return self.profile_table.all()

    def update_profile(self, id_: str, name: str, game_dir: Union[Path, str]):
        profile = Query()
        self.profile_table.update(
            {"name": name, "game_dir": game_dir}, profile.id == id_
        )
        pass

    def remove_profile(self, id_: str):
        profile = Query()
        self.profile_table.remove(profile.id == id_)
