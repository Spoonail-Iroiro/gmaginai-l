import os
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Optional, List, Tuple, Dict
from .maginai_installer import MaginaiInstaller
import logging

logger = logging.getLogger(__name__)


class ModInstaller:
    def __init__(
        self,
        maginai_installer: MaginaiInstaller,
        game_dir: Path,
        work_dir: Path | None = None,
    ):
        self.game_dir = game_dir
        self.maginai_installer = maginai_installer

    def set_work_dir(self, work_dir: Path):
        self._work_dir = work_dir

    @property
    def work_dir(self):
        if self._work_dir is None:
            raise ValueError(f"work_dir required")
        return self._work_dir

    def get_mod_own_dir(self, mod_name: str) -> Path:
        return self.get_mods_dir() / mod_name

    def get_mod_backup_dir(self, mod_name: str) -> Path:
        return self.get_mods_dir() / ("__" + mod_name)

    def get_mods_dir(self) -> Path:
        return self.maginai_installer.get_mod_dir() / "mods"

    def get_mods_load_js_path(self) -> Path:
        return self.get_mods_dir() / "mods_load.js"

    def unzip_to_work_temp(self, zip_path: Path) -> Path:
        temp_dir = Path(tempfile.mkdtemp(dir=self.work_dir))

        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(temp_dir)

        return temp_dir

    def search_mod_main_folder(self, top_dir: Path):
        init_js_paths = list(top_dir.glob("**/init.js"))
        if len(init_js_paths) >= 2:
            raise ValueError(
                "Can't detect mod main folder. It seems there are more than one mod main folder."
            )

        if len(init_js_paths) == 0:
            return None

        return init_js_paths[0].parent

    def install_mod(self, mod_main_folder: Path):
        mod_name = mod_main_folder.name
        mod_own_dir = self.get_mod_own_dir(mod_name)
        if not mod_main_folder.is_dir():
            raise ValueError(
                f"Specify mod main directory. It's not a directory: {mod_main_folder}"
            )

        if mod_own_dir.exists():
            raise ValueError("Mod '{mod_name}' already exists. Please remove it first.")

        shutil.copytree(mod_main_folder, mod_own_dir)

    def backup_existing_install_by_move(self, mod_name):
        """Backup existing mod's directory

        !! If backup already exists, it will be deleted silently.

        """
        mod_own_dir = self.get_mod_own_dir(mod_name)
        mod_backup_dir = self.get_mod_backup_dir(mod_name)

        if mod_backup_dir.exists():
            # shutil.rmtree(mod_backup_dir)
            logger.info(f"rmtree: {mod_backup_dir}")

        os.rename(mod_own_dir, mod_backup_dir)

    def recover_from_backup(self, mod_name):
        """Backup mod's directory

        !! This removes current mod's directory silently.

        """
        mod_own_dir = self.get_mod_own_dir(mod_name)
        mod_backup_dir = self.get_mod_backup_dir(mod_name)

        if mod_own_dir.exists():
            # shutil.rmtree(mod_backup_dir)
            logger.info(f"rmtree: {mod_own_dir}")

        shutil.copytree(mod_backup_dir, mod_own_dir)

    def get_mods_load_list(self):
        mods_load_js_path = self.get_mods_load_js_path()

        pass
