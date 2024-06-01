from pathlib import Path
import shutil
from typing import Optional, List, Tuple, Dict
from ..funcs import cyclic_save, cyclic_mkdir, file_select, selective_file_copy
import logging

logger = logging.getLogger(__name__)


class BackupControllerBase:
    def __init__(
        self,
        save_backup_root: Path,
        restore_bak_root: Path,
        game_save_dir: Path,
    ):
        self.save_backup_root = save_backup_root
        self.restore_bak_root = restore_bak_root
        self.game_save_dir = game_save_dir
        self.profile_name: Optional[str] = None

    def set_profile(self, profile_name: str):
        self.profile_name = profile_name

    @property
    def profile_dir(self) -> Path:
        if self.profile_name is None:
            raise ValueError("Profile name not set")
        return self.save_backup_root / self.profile_name

    def get_profile_names(self):
        profile_dirs = list(self.save_backup_root.glob("*"))
        return [path.name for path in profile_dirs]

    def get_existing_backup_dir_names(self) -> List[str]:
        names = [path.name for path in sorted(list(self.profile_dir.glob("*")))]
        return names

    def get_next_backup_dir_name(self, save_tag: str) -> str:
        profile_dir = self.profile_dir
        game_save_dir = self.game_save_dir

        save_dirs = profile_dir.glob("*")
        save_dir_names = [d.name for d in save_dirs]

        if len(save_dir_names) == 0:
            new_index = 0
        else:
            save_dir_infos = [dn.split("__") for dn in save_dir_names]
            save_dir_infos.sort(key=lambda info: int(info[1]), reverse=True)
            max_index = int(save_dir_infos[0][1])
            new_index = max_index + 1

        save_base_name = game_save_dir.name
        names = [save_base_name, str(new_index).zfill(4)]
        if save_tag != "":
            names.append(save_tag)
        new_save_dir_name = "__".join(names)

        return new_save_dir_name

    def backup(self, backup_dir_name: str):
        raise NotImplementedError()

    def restore(self, backup_dir_name: str):
        raise NotImplementedError()

    def show_target_files(self):
        raise NotImplementedError()


class DirectoryBackupController(BackupControllerBase):
    def __init__(
        self,
        save_backup_root: Path,
        restore_bak_root: Path,
        game_save_dir: Path,
    ):
        super().__init__(save_backup_root, restore_bak_root, game_save_dir)

    def backup(self, backup_dir_name: str):
        backup_dir = self.profile_dir / backup_dir_name
        shutil.copytree(self.game_save_dir, backup_dir)

    def restore(self, backup_dir_name: str):
        backup_dir = self.profile_dir / backup_dir_name
        cyclic_save(self.game_save_dir, self.restore_bak_root, 5, move=True)
        shutil.copytree(backup_dir, self.game_save_dir)

    def show_target_files(self):
        paths = list(self.game_save_dir.glob("**/*"))

        return paths


class SelectedFileBackupController(BackupControllerBase):
    def __init__(
        self,
        save_backup_root: Path,
        restore_bak_root: Path,
        game_save_dir: Path,
        spec: str,
    ):
        super().__init__(save_backup_root, restore_bak_root, game_save_dir)
        self.spec = spec

    def backup(self, backup_dir_name: str):
        backup_dir = self.profile_dir / backup_dir_name
        paths = file_select(self.game_save_dir, spec=self.spec)
        selective_file_copy(self.game_save_dir, paths, backup_dir)

    def restore(self, backup_dir_name: str):
        backup_dir = self.profile_dir / backup_dir_name
        restore_bak_dir = cyclic_mkdir(
            self.restore_bak_root, self.game_save_dir.name, 5
        )

        paths = file_select(self.game_save_dir, spec=self.spec)
        selective_file_copy(self.game_save_dir, paths, restore_bak_dir)

        shutil.copytree(backup_dir, self.game_save_dir, dirs_exist_ok=True)

    def show_target_files(self):
        paths = file_select(self.game_save_dir, spec=self.spec)

        return paths
