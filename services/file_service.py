from pathlib import Path


class FileService:

    def rename_file(self, file_path: Path, new_name: str) -> Path:
        new_path = file_path.with_name(new_name + file_path.suffix)
        file_path.rename(new_path)
        return new_path

