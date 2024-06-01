from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
import pytest
from gmaginai_l.core.config_service import ConfigService, Config
from gmaginai_l.core.config_enum import Theme, Language
from serde import serde
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@pytest.fixture
def service(tmp_db):
    service = ConfigService(tmp_db)
    return service


def test_config_service(service, tmp_db):
    config = service.get_config()
    logger.info(config)
    config.appearance.language = Language.JA
    config.external_source.list_release_endpoint = "https://example.com"

    config_not_updated = service.get_config()
    logger.info(config_not_updated)

    service.save_config(config)
    logger.info(service.get_config())

    # logger.info(service.config_table.all())
    # config.externalSource.list_release_endpoint = "https://example.com"
    # config.appearance.language = Language.JA
    # config = service.get_config()
    # logger.info(service.config_table.all())
