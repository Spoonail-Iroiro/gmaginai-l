from pathlib import Path
import os
import tomli
import pytest

from . import dirs


@pytest.fixture()
def proj_dir():
    return dirs.proj_dir


@pytest.fixture()
def test_data_dir(proj_dir):
    path = proj_dir / "test" / "test_data"

    return path
