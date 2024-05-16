from pathlib import Path
import re
import time
from typing import Optional, List, Tuple, Dict
import pytest
import logging
from gmaginai_l.core.maginai_installer import MaginaiInstaller

logger = logging.getLogger(__name__)

LIST_RELEASE_ENDPOINT = "https://api.github.com/repos/Spoonail-Iroiro/maginai/releases"

INDEX_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <link href="./style.css" rel="stylesheet">
  <script src="./sample.js"></script>
  {}
<title>Test Title</title>
</head>
<body>
  <div class="test">
  </div>
</body>
</html>
""".strip()
game_tag = '  \t<script src="./js/game/union.js"></script>'


@pytest.fixture
def installer(tmp_path):
    work_dir = tmp_path / "work"
    work_dir.mkdir(exist_ok=True)
    game_dir = tmp_path / "coaw"
    game_dir.mkdir(exist_ok=True)
    (game_dir / "game" / "js").mkdir(parents=True, exist_ok=True)
    (game_dir / "Game.exe").write_bytes(b"")
    (game_dir / "game" / "index.html").write_text(
        INDEX_HTML_TEMPLATE.format(game_tag), encoding="utf-8"
    )
    installer = MaginaiInstaller(work_dir, game_dir, LIST_RELEASE_ENDPOINT)

    return installer


@pytest.fixture
def dummy_extracted_dir(tmp_path):
    dummy_extracted_dir = tmp_path / "dummy_extracted"
    mods_dir = dummy_extracted_dir / "maginai" / "mod" / "mods"
    (mods_dir).mkdir(parents=True)
    (mods_dir / "mods_load.js").write_text("dummy mods_load.js")

    return dummy_extracted_dir


def test_tagname(installer, tmp_path):
    logger.info(installer.get_release_tag_names())
    pass


def test_download(installer, tmp_path):
    tag_names = [
        "v0.3.0",
        "v0.3.1",
        "v0.4.0",
        "v0.6.0",
        "v0.7.0",
    ]
    for tn in tag_names:
        installer.download_by_tag_name(tn)
        time.sleep(0.5)
    logger.info(tmp_path)


def test_unzip(installer):
    zip_path = installer.download_by_tag_name("v0.7.0")
    unzipped_dir = installer.unzip_to_work_temp(zip_path)
    logger.info(unzipped_dir)
    pass


def test_install_and_backup(installer, dummy_extracted_dir):
    installer.install_to_game(dummy_extracted_dir)
    logger.info(installer.get_index_html_path().read_text(encoding="utf-8"))

    pass
