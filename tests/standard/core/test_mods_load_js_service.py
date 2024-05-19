from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
import pytest
from gmaginai_l.core.mods_load_js_service import ModsLoadJsService

logger = logging.getLogger(__name__)


@pytest.fixture
def service():
    return ModsLoadJsService()


def test_to_dict(service):
    script = """
    // my mods
    LOADDATA = {
      mods: [
        "sample",
        "atrack",
        // "saves"
      ]
    }
    """

    assert service.to_dict(script) == {"mods": ["sample", "atrack"]}

    script = """
    // my mods
    var LOADDATA = {
      mods: [
        "sample",
        "atrack",
        // "saves"
      ]
    }

    """
    assert service.to_dict(script) == {"mods": ["sample", "atrack"]}


def test_from_dict(service):
    js = service.from_dict({"mods": ["atrack", "sample"]})
    expected = """
LOADDATA = {
  mods: [
    'atrack',
    'sample',
  ]
}
    """.strip()

    assert js == expected
