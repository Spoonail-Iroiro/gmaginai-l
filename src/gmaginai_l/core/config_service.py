"""
How to add config items

(1) (If you add new section) Define *Config, which represents a section in
the config and is property interface to the config. See `AppearanceConfig`.
(2) (If you add new section) Add a member, which type is *Config, to `Config`
(3) Define self._{key_name_snake_case}_keys = [{section_keys}, ...{item_keys}]
in the *Config `__init__`. See `AppearanceConfig`.
(4) Define setter/getter of the item.
(5) Define initial value in `_init_config_value` in `ConfigService`.
(6) Test.
"""


from pathlib import Path
from typing import Optional, List, Tuple, Dict, Any
import logging
from tinydb import TinyDB, Query
from tinydb.table import Table
from dataclasses import dataclass
from .config_enum import Theme, Language
from .db import get_db, get_current_db

logger = logging.getLogger(__name__)


class ConfigRecordNotFoundError(Exception):
    pass


def _get_config_record(_config_table: Table):
    all = _config_table.all()
    if len(all) == 0:
        raise ConfigRecordNotFoundError()
    config_record = all[0]
    return config_record


def _tinydb_upsert_by_keys(keys: List[str], value: Any):
    def opearation(doc):
        target = doc
        for i in range(len(keys) - 1):
            try:
                target = target[keys[i]]
            except KeyError:
                target[keys[i]] = {}
                target = target[keys[i]]

        target[keys[-1]] = value

    return opearation


def _enum_deserialize(value: Any, EnumClass, default_value):
    try:
        rtn = EnumClass(value)
    except ValueError:
        rtn = default_value

    return rtn


class ConfigSectionBase:
    def __init__(self, config_table: Table):
        self._config_table = config_table

    def _get_item_simple_keys(self, keys: List[str]):
        rtn = _get_config_record(self._config_table)
        for key in keys:
            rtn = rtn[key]
        return rtn

    def _set_item_simple_keys(self, keys: List[str], value: Any):
        # self._config_table.update({"appearance": {"theme": value}})
        self._config_table.update(_tinydb_upsert_by_keys(keys, value))


class AppearanceConfig(ConfigSectionBase):
    def __init__(self, config_table: Table):
        super().__init__(config_table)
        self._section_key = "appearance"

        self._theme_keys = [self._section_key, "theme"]
        self._language_keys = [self._section_key, "language"]

    @property
    def theme(self) -> Theme:
        # config_record = _get_config_record(self._config_table)
        # return config_record["appearance"]["theme"]
        rtn = Theme.safe_deserialize(self._get_item_simple_keys(self._theme_keys))
        return rtn

    @theme.setter
    def theme(self, value: Theme):
        # self._config_table.update({"appearance": {"theme": value}})
        # pass
        self._set_item_simple_keys(self._theme_keys, value.value)

    @property
    def language(self) -> Language:
        # config_record = _get_config_record(self._config_table)
        # return config_record["appearance"]["language"]
        rtn = Language.safe_deserialize(self._get_item_simple_keys(self._language_keys))
        return rtn

    @language.setter
    def language(self, value: Language):
        # self._config_table.update({"appearance": {"language": value}})
        # pass
        self._set_item_simple_keys(self._language_keys, value.value)


class ExternalSourceConfig(ConfigSectionBase):
    def __init__(self, config_table: Table):
        super().__init__(config_table)
        self._section_key = "externalSource"

        self._list_release_endpoint_keys = [self._section_key, "listReleaseEndpoint"]

    @property
    def list_release_endpoint(self) -> str:
        # config_record = _get_config_record(self._config_table)
        # return config_record["appearance"]["theme"]
        return self._get_item_simple_keys(self._list_release_endpoint_keys)

    @list_release_endpoint.setter
    def list_release_endpoint(self, value: str):
        # self._config_table.update({"appearance": {"theme": value}})
        # pass
        self._set_item_simple_keys(self._list_release_endpoint_keys, value)


@dataclass
class Config:
    appearance: AppearanceConfig
    externalSource: ExternalSourceConfig


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

        self.config_table.insert({})
        config = self.get_config()
        self._init_config_value(config)

    def _init_config_value(self, config: Config):
        config.appearance.theme = Theme.default_value()
        config.externalSource.list_release_endpoint = (
            "https://api.github.com/repos/Spoonail-Iroiro/maginai/releases"
        )
        config.appearance.language = Language.default_value()

    def get_config(self):
        # make sure a config record exists
        self.init_config()
        config = Config(
            AppearanceConfig(self.config_table),
            ExternalSourceConfig(self.config_table),
        )
        return config
