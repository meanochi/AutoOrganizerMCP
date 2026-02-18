import os
from pathlib import Path
from typing import List


def scan_directory(source_path: str) -> List[Path]:
    files = []
    for root, _, filenames in os.walk(source_path):
        for file in filenames:
            files.append(Path(root) / file)
    return files


def create_directory_if_not_exists(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def move_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    source.rename(destination)
