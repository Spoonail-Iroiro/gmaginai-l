from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class Theme(Enum):
    QT_DARK = "QtDark"

    @classmethod
    def default_value(cls):
        return cls.QT_DARK

    @classmethod
    def safe_deserialize(cls, value: str):
        try:
            rtn = cls(value)
        except ValueError:
            rtn = cls.default_value()

        return rtn


class Language(Enum):
    EN = "en"
    JA = "ja"

    @classmethod
    def default_value(self):
        return Language.EN

    @classmethod
    def safe_deserialize(cls, value: str):
        try:
            rtn = cls(value)
        except ValueError:
            rtn = cls.default_value()

        return rtn
