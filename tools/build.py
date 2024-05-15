import PyInstaller.__main__
from pathlib import Path
import send2trash

proj_dir = Path(__file__).parent.parent
dist_dir = proj_dir / "dist" / "SaveBackup"


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


def place_assets():
    shutil.copy(proj_dir / "config_default.toml", dist_dir / "config.toml")
    shutil.copy(proj_dir / "assets" / "run.bat", dist_dir / "run.bat")
    shutil.copytree(proj_dir / "data", dist_dir / "data")


if dist_dir.exists():
    print(f"Delete {dist_dir}?(y/n)")
    if input() != "y":
        raise ValueError(f"Cancelled Build")
    send2trash.send2trash(dist_dir)
dist_dir.mkdir(parents=True, exist_ok=True)

pyinstaller_build()
place_assets()
