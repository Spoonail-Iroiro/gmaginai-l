from pathlib import Path
import traceback
import shutil
import os
import zipfile
import tempfile
from typing import Optional, List, Tuple, Dict
import re
import logging
import requests

logger = logging.getLogger(__name__)

RELEASE_ZIP_PATTERN = r"maginai-\d+\.\d+\.\d.*\.zip"


class MaginaiInstaller:
    def __init__(
        self, game_dir: Path, list_release_endpoint: str, work_dir: Path | None = None
    ):
        self.game_dir = game_dir
        self.list_release_endpoint = list_release_endpoint
        self._work_dir = work_dir

        self.maginai_tag_service = MaginaiTagService()
        pass

    def get_mod_dir(self):
        return self.game_dir / "game" / "js" / "mod"

    def get_backup_dir(self):
        return self.get_mod_dir().parent / "__mod"

    def get_index_html_path(self):
        return self.game_dir / "game" / "index.html"

    def set_work_dir(self, work_dir: Path):
        self._work_dir = work_dir

    @property
    def work_dir(self):
        if self._work_dir is None:
            raise ValueError(f"work_dir required")
        return self._work_dir

    def get_version(self) -> str | None:
        version_js_path = self.get_mod_dir() / "version.js"

        if version_js_path.exists():
            target_text = version_js_path.read_text(encoding="utf-8")
        else:
            target_text = (self.get_mod_dir() / "loader.js").read_text(encoding="utf-8")

        matches = re.findall(r"\d+\.\d+\.\d+", target_text)

        if len(matches) == 0:
            return None
        else:
            return matches[-1]

    def get_release_tag_names(self, timeout: int | None = None) -> List[str]:
        res = requests.get(self.list_release_endpoint, timeout=timeout)
        res.raise_for_status()
        release_list = res.json()
        tag_names_with_release = (
            []
        )  # Releases with no distribution zip (maginai-X.Y.Z.zip) are not listed here
        for release in release_list:
            for asset in release["assets"]:
                if re.match(RELEASE_ZIP_PATTERN, asset["name"]):
                    tag_names_with_release.append(release["tag_name"])
                    break

        return tag_names_with_release

    def download_by_tag_name(self, tag_name: str, timeout: int | None = None) -> Path:
        res = requests.get(self.list_release_endpoint, timeout=timeout)
        res.raise_for_status()
        release_list = res.json()
        target_release_asset: dict | None = None
        for release in release_list:
            if release["tag_name"] == tag_name:
                for asset in release["assets"]:
                    if re.match(RELEASE_ZIP_PATTERN, asset["name"]):
                        target_release_asset = asset
                        break

        if target_release_asset is None:
            raise ValueError(f"No release/asset for the tag: {tag_name}")

        filename = target_release_asset["name"]
        download_url = target_release_asset["browser_download_url"]

        res = requests.get(download_url)
        res.raise_for_status()

        path = self.work_dir / filename
        path.write_bytes(res.content)

        return path

    def unzip_to_work_temp(self, zip_path: Path) -> Path:
        temp_dir = Path(tempfile.mkdtemp(dir=self.work_dir))

        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(temp_dir)

        return temp_dir

    def install_to_game(self, extracted_dir: Path):
        mod_dir_dst = self.get_mod_dir()
        if not mod_dir_dst.parent.exists():
            raise ValueError(
                f"Incorrect game directory. No `js` directory exists:{self.game_dir}"
            )

        if mod_dir_dst.exists():
            raise ValueError(f"`mod` directory already exists. Please remove it first")

        mod_dir_src = extracted_dir / "maginai" / "mod"

        shutil.copytree(mod_dir_src, mod_dir_dst)

        try:
            if not self.maginai_tags_exist():
                self._write_tags()
        except Exception as ex:
            error_message = "\n".join(traceback.format_exception_only(ex))
            raise ValueError(
                f"An error occured during writing tags on index.html: {error_message}"
            ) from ex

    def migrate_mods(self, src_mod_dir: Path):
        """Overwrite `mods` dir of the current game directory by src_mod_dir/mods

        !! The current 'mods' will be removed silently. You should call this just after clean-install.

        """
        mod_dir = self.get_mod_dir()
        src_mods = src_mod_dir / "mods"
        if not src_mods.exists():
            raise ValueError(
                f"No mod/mods directory of src exists. May be incorrect `mod` dir: {src_mod_dir}"
            )

        dst_mods = mod_dir / "mods"
        if (dst_mods).exists():
            shutil.rmtree(dst_mods)

        shutil.copytree(src_mods, dst_mods)

    def maginai_tags_exist(self):
        index_html_path = self.get_index_html_path()
        html = index_html_path.read_text(encoding="utf-8")
        return self.maginai_tag_service.tags_exist(html)

    def _write_tags(self):
        index_html_path = self.get_index_html_path()
        html = index_html_path.read_text(encoding="utf-8")
        new_html = self.maginai_tag_service.add_tags(html)
        index_html_path.write_text(new_html, encoding="utf-8")

    def backup_existing_install_by_move(self):
        """Backup existing `mod` directory

        !! If backup already exists, it will be deleted silently.

        """
        mod_dir = self.get_mod_dir()
        bak_dir = self.get_backup_dir()
        if bak_dir.exists():
            shutil.rmtree(bak_dir)

        os.rename(mod_dir, bak_dir)

    def recover_from_backup(self):
        """Recover `mod` from backup directory

        !! This rmeoves current `mod` directory silently.

        """
        mod_dir = self.get_mod_dir()
        bak_dir = self.get_backup_dir()
        if mod_dir.exists():
            shutil.rmtree(mod_dir)

        shutil.copytree(bak_dir, mod_dir)

    def uninstall_only_tags(self):
        index_html_path = self.get_index_html_path()
        html = index_html_path.read_text(encoding="utf-8")
        new_html = self.maginai_tag_service.remove_tags(html)
        index_html_path.write_text(new_html, encoding="utf-8")

    def uninstall_all(self):
        mod_dir = self.get_mod_dir()
        if mod_dir.exists():
            shutil.rmtree(mod_dir)

        self.uninstall_only_tags()


class MaginaiTagService:
    GAME_MAIN_JS_PATTERN = r"\s*<script src=.*?js/game/union\.js"
    MOD_LOADER_JS_PATTERN = r"\s*<script src=.*?js/mod/loader\.js"
    MOD_CONFIG_JS_PATTERN = r"\s*<script src=.*?js/mod/config\.js"

    MOD_CONFIG_JS_TAG = '<script src="./js/mod/config.js"></script>'
    MOD_LOADER_JS_TAG = '<script src="./js/mod/loader.js"></script>'

    def __init__(self):
        pass

    def tags_exist(self, html: str) -> bool:
        """Returns if both of loader tag and config tag exist"""
        lines = html.split("\n")
        loader_ln = _get_matched_ln(lines, self.MOD_LOADER_JS_PATTERN)
        config_ln = _get_matched_ln(lines, self.MOD_CONFIG_JS_PATTERN)

        return loader_ln is not None and config_ln is not None

    def remove_tags(self, html: str):
        """Returns new `html` without maginai tags"""
        lines = html.split("\n")
        loader_ln = _get_matched_ln(lines, self.MOD_LOADER_JS_PATTERN)
        if loader_ln is not None:
            del lines[loader_ln]

        config_ln = _get_matched_ln(lines, self.MOD_CONFIG_JS_PATTERN)
        if config_ln is not None:
            del lines[config_ln]

        return "\n".join(lines)

    def add_tags(self, html: str):
        """Returns new `html` with maginai tags

        This removes existing tags to ensure there are only one set of them in the html.
        """
        lines = html.split("\n")
        loader_ln = _get_matched_ln(lines, self.MOD_LOADER_JS_PATTERN)
        config_ln = _get_matched_ln(lines, self.MOD_CONFIG_JS_PATTERN)
        game_main_ln = _get_matched_ln(lines, self.GAME_MAIN_JS_PATTERN)

        if game_main_ln is None:
            raise ValueError(f"Invalid html. No union.js loading is found")

        if game_main_ln == config_ln or game_main_ln == loader_ln:
            raise ValueError(
                f"Invalid html. Mod tags shouldn't be on the same line with union.js"
            )

        html = self.remove_tags(html)

        lines = html.split("\n")

        game_main_ln = _get_matched_ln(lines, self.GAME_MAIN_JS_PATTERN)

        if game_main_ln is None:
            raise ValueError(f"Invalid html. No union.js loading is found")

        lines.insert(game_main_ln + 1, self.MOD_LOADER_JS_TAG)
        lines.insert(game_main_ln + 1, self.MOD_CONFIG_JS_TAG)

        return "\n".join(lines)


def _get_matched_ln(lines: List[str], pattern: str) -> int | None:
    rtn = None
    for i, line in enumerate(lines):
        if re.match(pattern, line):
            rtn = i

    return rtn
