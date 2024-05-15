from pathlib import Path
import os
import shutil
from send2trash import send2trash
import re
from typing import Optional, List, Tuple, Dict, Callable
import logging

logger = logging.getLogger(__name__)


def cyclic_mkdir(root, dir_name, gen_limit):
    """Cyclicly Move dirs in root up to gen_limit and mkdir newest dir
    Note:
        name of dirs in root should be {n}__<dir_name>
    """
    new_dir = root / ("0__" + dir_name)
    if new_dir.exists():
        bak_dirs = root.glob("*" + dir_name)
        dir_infos = [(d, int(d.name.split("__")[0])) for d in bak_dirs]
        dir_infos.sort(key=lambda di: di[1], reverse=True)
        for dir_path, idx in dir_infos:
            new_name = "__".join([str(idx + 1), dir_name])
            new_path = dir_path.parent / new_name
            shutil.move(dir_path, new_path)
            if not (idx < gen_limit - 1):
                send2trash(new_path)

    new_dir.mkdir()
    return new_dir


def cyclic_save(src_dir, dst_root, gen_limit, move=False):
    new_dir = cyclic_mkdir(dst_root, src_dir.name, gen_limit)

    if not move:
        shutil.copytree(src_dir, new_dir, dirs_exist_ok=True)
    else:
        # remove new_dir mkdir-ed
        os.rmdir(new_dir)
        # and move src_dir as new_dir
        shutil.move(src_dir, new_dir)


def get_paths_from_spec(src_dir: Path, spec: str):
    # Path.glob is already recursive (**/... enabled)
    file_paths = list(src_dir.glob(spec))
    return file_paths


def file_select(
    src_dir: Path,
    *,
    spec: Optional[str] = None,
    get_save_file_callable: Optional[Callable[[List[Path]], List[Path]]] = None,
):
    # For now, spec is equal to glob
    if spec is None:
        spec = "**/*"
    file_paths = get_paths_from_spec(src_dir, spec)
    if get_save_file_callable is not None:
        paths_for_copy = get_save_file_callable(file_paths)
    else:
        paths_for_copy = file_paths
    paths_for_copy.sort()
    return paths_for_copy


def selective_file_copy(
    src_dir: Path,
    selected_path: List[Path],
    dst_dir: Path,
    *,
    dry_run=False,
):
    if len(selected_path) == 0:
        raise ValueError("No files to copy")
    dst_dir.mkdir(exist_ok=True)
    paths_for_copy = selected_path

    for path in paths_for_copy:
        src_path = path
        rel_path = path.relative_to(src_dir)
        dst_path = dst_dir / rel_path
        if src_path.is_file():
            if dry_run:
                print(f"Copy {src_path} to {dst_path} (dry-run)")
            else:
                # mkdir
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(src_path, dst_path)
        elif src_path.is_dir():
            if dry_run:
                print(f"Make dir {dst_path} (dry-run)")
            else:
                dst_path.mkdir(parents=True, exist_ok=True)


def ark_select_paths(file_paths):
    bak_paths = set([path for path in file_paths if path.name.endswith("bak")])
    world_bak_paths = set(
        [
            path
            for path in file_paths
            if re.match(r".*_.*_.*\.ark", path.name) is not None
        ]
    )
    file_paths_set = set(file_paths)

    save_paths = file_paths_set - bak_paths - world_bak_paths

    from pprint import pprint

    return list(save_paths)
