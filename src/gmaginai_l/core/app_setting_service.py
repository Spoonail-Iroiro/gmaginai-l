from pathlib import Path
from typing import Optional, List, Tuple, Dict, Any
import logging
from tinydb import TinyDB, Query
from tinydb.table import Table
from dataclasses import dataclass, field
from .config_enum import Theme, Language
from .db import get_db, get_current_db
from serde import serde, to_dict, from_dict

logger = logging.getLogger(__name__)


class RecordNotFoundError(Exception):
    pass


def _get_app_setting_record(table: Table):
    all = table.all()
    if len(all) == 0:
        raise RecordNotFoundError()
    record = all[0]
    return record


class AppSettingService:
    """App Setting service
    Provides persistent application settings.

    Should be instanciated every use

    In test, just mock it entirely or return AppSettingService(temp_db)

    """

    def __init__(self, db: TinyDB | None = None):
        self.db = db if db is not None else get_current_db()
        self.app_setting_table = self.db.table("app_setting")

    def init_app_setting(self, force=False):
        if not force:
            try:
                _get_app_setting_record(self.app_setting_table)
                return
            except RecordNotFoundError:
                pass
        else:
            self.app_setting_table.remove()

        self.app_setting_table.insert({})

    def get(self, key: str, default_: Any):
        self.init_app_setting()
        record = _get_app_setting_record(self.app_setting_table)
        try:
            return record[key]
        except KeyError:
            return default_

    def set(self, key: str, value: Any):
        self.init_app_setting()
        self.app_setting_table.update({key: value})
