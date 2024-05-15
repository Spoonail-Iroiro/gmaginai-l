from pathlib import Path
from typing import Optional, List, Tuple, Dict
import logging
from gmaginai_l.core.profile_service import ProfileService
from gmaginai_l.core.db import get_db

logger = logging.getLogger(__name__)


def test_profile_service(tmp_path):
    db = get_db(tmp_path / "db.json")
    service = ProfileService(db)

    logger.info(service.get_all_profile())

    prof1_1_id = service.add_profile("prof1", Path(r"C:\Users"))
    logger.info(prof1_1_id)
    prof1_2_id = service.add_profile("prof1", Path(r"C:\Users\testuser"))
    logger.info(prof1_2_id)

    profiles = service.get_all_profile()
    logger.info(profiles)

    rec0 = profiles[0]
    rec0_id = profiles[0]["id"]
    service.update_profile(rec0_id, "prof2", rec0["game_dir"])

    service.remove_profile(prof1_2_id)
    logger.info(service.get_all_profile())
