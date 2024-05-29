from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class Theme(Enum):
    QT_DARK = "QtDark"


class Language(Enum):
    EN = "en"
    JA = "ja"
