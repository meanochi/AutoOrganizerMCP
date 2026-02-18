from dataclasses import dataclass
from pathlib import Path


@dataclass
class FileModel:
    original_path: Path
    name: str
    extension: str
    content: str | None = None

    @property
    def full_name(self) -> str:
        return f"{self.name}{self.extension}"
