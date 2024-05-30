from pathlib import Path
import shutil
import json
import logging
import subprocess

logger = logging.getLogger(__name__)

logging.basicConfig(level="INFO")

proj_dir = Path(__file__).parent.parent

lic_json_path = proj_dir / "lic" / "lic.json"
lic_ex_dir = proj_dir / "tools" / "licex"
licenses_dir = proj_dir / "asset" / "LICENSES"

lic_json_path.parent.mkdir(parents=True, exist_ok=True)

with open(lic_json_path, "w", encoding="utf-8") as f:
    subprocess.run(
        [
            "pip-licenses",
            "--with-urls",
            "--with-license-file",
            "--with-notice-file",
            "--from=mixed",
            "--format=json",
        ],
        stdout=f,
        check=True,
    )

lic_json_dict = json.loads(lic_json_path.read_text(encoding="utf-8"))

for lic_dict in lic_json_dict:
    name = lic_dict["Name"]
    if lic_dict["LicenseFile"] == "UNKNOWN":
        lic_path = lic_ex_dir / f"license-{name}.txt"
        if not lic_path.exists():
            raise ValueError(f"License not found: {name}, {lic_dict['License']}")
    else:
        lic_path = Path(lic_dict["LicenseFile"])

    license_dir = licenses_dir / name
    license_dir.mkdir(exist_ok=True, parents=True)
    shutil.copy(lic_path, license_dir / lic_path.name)

    if lic_dict["NoticeFile"] != "UNKNOWN":
        notice_path = Path(lic_dict["NoticeFile"])
        shutil.copy(notice_path, license_dir / lic_path.name)

    if lic_dict["URL"] != "UNKNOWN":
        url_path = license_dir / "source.txt"
        url_path.write_text(lic_dict["URL"], encoding="utf-8")
