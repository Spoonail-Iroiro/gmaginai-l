from pathlib import Path
import os
import tomli
import pytest
from gmaginai_l.core.db import get_db

from . import dirs


@pytest.fixture()
def proj_dir():
    return dirs.proj_dir


@pytest.fixture()
def test_data_dir(proj_dir):
    path = proj_dir / "test" / "test_data"

    return path


@pytest.fixture
def tmp_db(tmp_path):
    db = get_db(tmp_path / "temp_db.json")
    return db
