from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
from .config_enum import Language
from PySide6.QtCore import QTranslator
from .. import dirs

logger = logging.getLogger(__name__)


def set_translation(app, language: Language):
    if language == Language.JA:
        translation_file_path = (
            dirs.application_dir
            / "_internal"
            / "content_translation"
            / "gmaginai-l_ja.qm"
        )
        translator = QTranslator(app)
        translator.load(translation_file_path.name, str(translation_file_path.parent))
        app.installTranslator(translator)
    elif language == Language.EN:
        pass
    else:
        raise NotImplementedError()
