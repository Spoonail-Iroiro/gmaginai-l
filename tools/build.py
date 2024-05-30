import PyInstaller.__main__
from pathlib import Path
import logging

logging.basicConfig(level="INFO")

logger = logging.getLogger(__name__)

proj_dir = Path(__file__).parent.parent
dist_dir = proj_dir / "dist" / "gmaginai-l"


def pyinstaller_build():
    # pyinstallerでのビルド
    dist_arg = f"--distpath={dist_dir.parent}"  # for pyinstaller 6 or later
    build_arg = f"--workpath={proj_dir / 'build'}"

    PyInstaller.__main__.run(
        [
            "main_spec.spec",
            dist_arg,
            build_arg,
            "--noconfirm",
        ]
    )


import shutil
import os


def overwritetree_no_gitkeep(src_dir, dst_dir):
    for path in src_dir.glob("*"):
        if path.is_dir():
            shutil.copytree(path, dst_dir / path.name)
        else:
            shutil.copy(path, dst_dir / path.name)


def place_assets():
    overwritetree_no_gitkeep(proj_dir / "asset", dist_dir)
    overwritetree_no_gitkeep(proj_dir / "_internal", dist_dir / "_internal")
    os.remove(dist_dir / "_internal" / "content_translation" / ".gitkeep")
    (dist_dir / "data").mkdir()
    shutil.copytree(proj_dir / "qss", dist_dir / "qss")


if dist_dir.exists():
    print(f"Delete {dist_dir}?(y/n)")
    if input() != "y":
        raise ValueError(f"Cancelled Build")
    shutil.rmtree(dist_dir)
    # send2trash.send2trash(dist_dir)
dist_dir.mkdir(parents=True, exist_ok=True)

pyinstaller_build()
place_assets()
