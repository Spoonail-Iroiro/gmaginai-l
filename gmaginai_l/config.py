from pathlib import Path
from typing import Optional, List, Tuple, Dict
from dataclasses import dataclass
import logging
import tomli

logger = logging.getLogger(__name__)


@dataclass
class _Config:
    list_release_endpoint: str


_config: _Config | None = None


def set_config(config: _Config):
    global _config
    _config = config


def unset_config():
    _config = None


def get_config() -> _Config:
    if _config is None:
        raise ValueError("No config")
    return _config


def load_from_file(path: Path):
    config_dict = tomli.loads(path.read_text(encoding="utf-8"))

    config = _Config(
        list_release_endpoint=config_dict["system"]["list_release_end_point"]
    )

    set_config(config)
