from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
from logging.handlers import RotatingFileHandler
from .. import dirs

logger = logging.getLogger(__name__)


def get_formatter():
    formatter = logging.Formatter("%(asctime)s:%(levelname)-5s:%(name)s:%(message)s")
    return formatter


def get_format_str():
    rtn = "%(asctime)s:%(levelname)-5s:%(name)s:%(message)s"
    return rtn


def setup_log(log_level: str):
    log_path = dirs.application_dir / "log.log"
    sh = logging.StreamHandler()
    fh = RotatingFileHandler(
        log_path,
        maxBytes=5 * 1024 * 1024,
        backupCount=1,
        encoding="utf-8",
    )
    logging.basicConfig(level=log_level, handlers=[sh, fh], format=get_format_str())
    pass
