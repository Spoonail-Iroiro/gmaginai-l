from pathlib import Path
import subprocess
from .. import dirs

template_launch = """
@echo off
chcp 65001
cd /d "{}"
start "" Game.exe
""".strip()

template_launch_with_dev_console = """
@echo off
chcp 65001
cd /d "{}"
set WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS=--auto-open-devtools-for-tabs
start "" Game.exe
""".strip()


class CoAWLauncher:
    def launch(self, game_dir: Path):
        script_path = dirs.application_dir / "temp" / "launch.bat"
        script_path.parent.mkdir(exist_ok=True)
        script_path.write_text(template_launch.format(game_dir), encoding="utf-8")
        subprocess.Popen(script_path)

    def launch_with_dev_console(self, game_dir: Path):
        script_path = dirs.application_dir / "temp" / "launch_with_dev_console.bat"
        script_path.parent.mkdir(exist_ok=True)
        script_path.write_text(template_launch_with_dev_console.format(game_dir), encoding="utf-8")
        subprocess.Popen(script_path)
