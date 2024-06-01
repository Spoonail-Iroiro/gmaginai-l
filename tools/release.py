from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
import shutil
from gmaginai_l import __version__


logger = logging.getLogger(__name__)

logging.basicConfig(level="INFO")

logger = logging.getLogger(__name__)

proj_dir = Path(__file__).parent.parent
dist_dir = proj_dir / "dist" / "gmaginai-l"
dist_root = dist_dir.parent

archive_name = dist_root / f"gmaginai-l-v{__version__}"
shutil.make_archive(str(archive_name), "zip", root_dir=dist_root, base_dir="gmaginai-l")
