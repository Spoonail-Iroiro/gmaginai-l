from pathlib import Path
from typing import Optional, List, Tuple, Dict, Callable
from PySide6.QtCore import QRunnable, Slot, QThreadPool
import logging

logger = logging.getLogger(__name__)


class Runner(QRunnable):
    def __init__(self, fn: Callable[[], None]):
        self.fn = fn

    @Slot()
    def run(self):
        self.fn()


def qtconcurrent_run(fn: Callable[[], None]):
    runner = Runner(fn)
    QThreadPool.globalInstance().start

    pass
