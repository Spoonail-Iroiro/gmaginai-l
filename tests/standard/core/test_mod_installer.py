from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
import pytest
from gmaginai_l.core.maginai_installer import MaginaiInstaller
from gmaginai_l.core.mod_installer import ModInstaller, AmbiguousModMainFolderError

logger = logging.getLogger(__name__)


@pytest.fixture
def installer(tmp_path):
    work_dir = tmp_path / "work"
    work_dir.mkdir(exist_ok=True)
    game_dir = tmp_path / "coaw"
    game_dir.mkdir(exist_ok=True)
    mods_dir = game_dir / "game" / "js" / "mod" / "mods"
    mods_dir.mkdir(parents=True, exist_ok=True)
    (mods_dir / "mods_load.js").write_text(
        """
LOADDATA = {
    mods: [
      // my mods
    ]
}
        """.strip()
    )
    # (game_dir / "Game.exe").write_bytes(b"")
    # (game_dir / "game" / "index.html").write_text(
    #     INDEX_HTML_TEMPLATE.format(game_tag), encoding="utf-8"
    # )
    maginai_installer = MaginaiInstaller(game_dir, "", work_dir)
    installer = ModInstaller(maginai_installer, tmp_path)

    return installer


def test_search_mod_main_folder(installer, tmp_path):
    mod_extracted_dir = tmp_path / "mods" / "sample-v0.1.0"
    sample_mod_dir = mod_extracted_dir / "sample"
    sample_mod_dir.mkdir(parents=True)
    (sample_mod_dir / "init.js").write_text("js", encoding="utf-8")

    assert installer.search_mod_main_folder(mod_extracted_dir) == sample_mod_dir

    another_mod_dir = mod_extracted_dir / "another"
    another_mod_dir.mkdir(parents=True)
    (another_mod_dir / "init.js").write_text("js2")

    with pytest.raises(AmbiguousModMainFolderError):
        installer.search_mod_main_folder(mod_extracted_dir)

    mod2_extracted_dir = tmp_path / "mods" / "sample2-v0.2.0"
    mod2_extracted_dir.mkdir(parents=True)

    assert installer.search_mod_main_folder(mod2_extracted_dir) is None
