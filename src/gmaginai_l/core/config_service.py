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


class ConfigRecordNotFoundError(Exception):
    pass


def _get_config_record(_config_table: Table):
    all = _config_table.all()
    if len(all) == 0:
        raise ConfigRecordNotFoundError()
    config_record = all[0]
    return config_record


@serde()
@dataclass
class AppearanceConfig:
    theme: Theme = Theme.QT_DARK
    language: Language = Language.EN


@serde()
@dataclass
class ExternalSourceConfig:
    list_release_endpoint: str = (
        "https://api.github.com/repos/Spoonail-Iroiro/maginai/releases"
    )


@serde()
@dataclass
class Config:
    appearance: AppearanceConfig = field(default_factory=AppearanceConfig)
    external_source: ExternalSourceConfig = field(default_factory=ExternalSourceConfig)


class ConfigService:
    """Config service
    Should instanciate every use

    ```python
    config = ConfigService().get_config()
    ```

    In test, just mock it entirely or return ConfigService(temp_db)

    """

    def __init__(self, db: TinyDB | None = None):
        self.db = db if db is not None else get_current_db()
        self.config_table = self.db.table("config")

    def init_config(self, force=False):
        if not force:
            try:
                _get_config_record(self.config_table)
                return
            except ConfigRecordNotFoundError:
                pass
        else:
            self.config_table.remove()

        config_default = Config()
        self.config_table.insert(to_dict(config_default))

    def get_config(self) -> Config:
        # make sure a config record exists
        self.init_config()
        config_record = _get_config_record(self.config_table)
        config = from_dict(Config, config_record)
        return config

    def save_config(self, config: Config):
        config_record = to_dict(config)
        self.config_table.update(config_record)
