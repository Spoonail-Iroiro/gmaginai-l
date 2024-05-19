import os
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
from .maginai_installer import MaginaiInstaller
from .mods_load_js_service import ModsLoadJsService


logger = logging.getLogger(__name__)


class AmbiguousModMainFolderError(Exception):
    pass


class ModInstaller:
    def __init__(
        self,
        maginai_installer: MaginaiInstaller,
        work_dir: Path | None = None,
    ):
        self.maginai_installer = maginai_installer
        self.mods_load_js_service = ModsLoadJsService()

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

    def search_mod_main_folder(self, top_dir: Path) -> Path | None:
        init_js_paths = list(top_dir.glob("**/init.js"))
        if len(init_js_paths) >= 2:
            raise AmbiguousModMainFolderError(
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
            raise ValueError(
                f"Mod '{mod_name}' already exists. Please remove it first."
            )

        shutil.copytree(mod_main_folder, mod_own_dir)

        self.enable_mod(mod_name)

    def uninstall_mod(self, mod_name: str):
        self.disable_mod(mod_name)

        mod_own_dir = self.get_mod_own_dir(mod_name)
        shutil.rmtree(mod_own_dir)

    def backup_existing_install_by_move(self, mod_name):
        """Backup existing mod's directory

        !! If backup already exists, it will be deleted silently.

        """
        mod_own_dir = self.get_mod_own_dir(mod_name)
        mod_backup_dir = self.get_mod_backup_dir(mod_name)

        if mod_backup_dir.exists():
            shutil.rmtree(mod_backup_dir)

        os.rename(mod_own_dir, mod_backup_dir)

    def recover_from_backup(self, mod_name):
        """Backup mod's directory

        !! This removes current mod's directory silently.

        """
        mod_own_dir = self.get_mod_own_dir(mod_name)
        mod_backup_dir = self.get_mod_backup_dir(mod_name)

        if mod_own_dir.exists():
            shutil.rmtree(mod_own_dir)

        shutil.copytree(mod_backup_dir, mod_own_dir)

    def get_disabled_mods(self) -> List[str]:
        """Get names of disabled mods

        The order is sorted by name.

        """
        mods_dir = self.get_mods_dir()
        enabled_mod_names = self.get_enabled_mods()
        all_mods_names = []
        for path in mods_dir.glob("*"):
            if path.is_dir() and not path.name.startswith("__"):
                all_mods_names.append(path.name)

        disabled_mod_names = list(set(all_mods_names) - set(enabled_mod_names))
        disabled_mod_names.sort()

        return disabled_mod_names

    def get_enabled_mods(self) -> List[str]:
        """Get names of enabled mods

        The order is defined one (= load order).

        """
        mods_load_js_path = self.get_mods_load_js_path()
        mods_load_js_dict = self.mods_load_js_service.to_dict(
            mods_load_js_path.read_text(encoding="utf-8")
        )

        return mods_load_js_dict["mods"]

    def set_enabled_mods(self, mods_load_list: List[str]):
        mods_load_js_path = self.get_mods_load_js_path()
        js = self.mods_load_js_service.from_dict({"mods": mods_load_list})
        mods_load_js_path.write_text(js, encoding="utf-8")

    def disable_mod(self, mod_name: str):
        enabled_mods = self.get_enabled_mods()
        new_enabled = [mo for mo in enabled_mods if mo != mod_name]
        self.set_enabled_mods(new_enabled)

    def enable_mod(self, mod_name: str, error_on_no_mod=False):
        if error_on_no_mod:
            disabled_mods = self.get_disabled_mods()
            if mod_name not in disabled_mods:
                raise ValueError(f"Mod '{mod_name}' is not installed")

        enabled_mods = self.get_enabled_mods()
        if mod_name not in enabled_mods:
            enabled_mods.append(mod_name)
        self.set_enabled_mods(enabled_mods)
