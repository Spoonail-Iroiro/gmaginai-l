from pathlib import Path
from typing import Optional, List, Tuple, Dict
import json
from gmaginai_l.dirs import application_dir
import logging

logging.basicConfig(level="INFO")

logger = logging.getLogger(__name__)

proj_file_path = application_dir / ".trlist"

module_dir = application_dir / "src" / "gmaginai_l"

# Get *.py/*.ui paths under module dir except for generated files (*_ui.py)
paths = list(module_dir.glob("**/*.py"))
paths.extend(list(module_dir.glob("**/*.ui")))
paths_set = set(paths)
generated_paths_set = set(module_dir.glob("**/*_ui.py"))
paths_set = paths_set - generated_paths_set
paths = sorted(list(paths_set))

content_str = "\n".join(
    [path.relative_to(application_dir).as_posix() for path in paths]
)

proj_file_path.write_text(content_str, encoding="utf-8")

# proj_json_dict = {"files": [str(path.relative_to(application_dir)) for path in paths]}
# proj_file_path.write_text(
#     json.dumps(proj_json_dict, indent=2, ensure_ascii=False), encoding="utf-8"
# )
