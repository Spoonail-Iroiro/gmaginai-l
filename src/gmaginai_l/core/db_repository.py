from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
from tinydb import TinyDB

logger = logging.getLogger(__name__)


_current_db: None | TinyDB = None


def set_current_db(db: TinyDB):
    global _current_db
    if _current_db is not None:
        raise ValueError(f"Current DB is already set")
    _current_db = db


def unset_current_db():
    global _current_db
    _current_db = None


def get_current_db():
    if _current_db is None:
        raise ValueError(f"No DB set")
    return _current_db
