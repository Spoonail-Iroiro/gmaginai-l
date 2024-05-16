from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
import pytest
from gmaginai_l.core.maginai_installer import MaginaiTagService

logger = logging.getLogger(__name__)

base_template = """
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
loader_tags = """
<script src="./js/mod/config.js"></script>
<script src="./js/mod/loader.js"></script>
""".strip()


def test_add_tags():
    service = MaginaiTagService()
    html = base_template.format(game_tag)
    new_html = service.add_tags(html)

    assert loader_tags in new_html

    html_added2 = service.add_tags(new_html)

    # TODO: one tag set test
    logger.info(html_added2)


def test_add_tags_error():
    service = MaginaiTagService()
    no_game_main_html = base_template.format("")

    with pytest.raises(ValueError, match="No union.js"):
        service.add_tags(no_game_main_html)

    union_same_line_html = base_template.format(game_tag + loader_tags)

    with pytest.raises(
        ValueError, match="Mod tags shouldn't be on the same line with union.js"
    ):
        service.add_tags(union_same_line_html)


def test_tags_exist():
    service = MaginaiTagService()
    html = base_template.format(game_tag)

    assert not service.tags_exist(html)

    new_html = service.add_tags(html)
    assert service.tags_exist(new_html)


def test_remove_tags():
    service = MaginaiTagService()
    html = base_template.format(game_tag + "\n" + loader_tags)

    assert service.tags_exist(html)

    new_html = service.remove_tags(html)
    assert not service.tags_exist(new_html)
    logger.info(new_html)
