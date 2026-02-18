from pathlib import Path
from typing import Dict, List
from models.file_model import FileModel
from services.ai_service import AIService
from services.file_service import FileService
from utils.file_utils import scan_directory, create_directory_if_not_exists, move_file
from utils.text_utils import sanitize_filename


class OrganizerService:

    EXTENSION_MAP = {
        ".jpg": "images",
        ".png": "images",
        ".txt": "documents",
        ".pdf": "documents",
        ".docx": "documents",
        ".xlsx": "documents",
        ".csv": "documents",
        ".mp3": "audio",
        ".wav": "audio",
        ".mp4": "video"
    }

    def __init__(self):
        self.ai_service = AIService()
        self.file_service = FileService()

    def _read_file_content(self, path: Path) -> str | None:
        encodings = ["utf-8", "utf-16", "latin1"]
        for enc in encodings:
            try:
                return path.read_text(encoding=enc)
            except:
                continue
        return None

    def _unique_name(self, folder: Path, base_name: str, extension: str) -> str:
        candidate = base_name
        counter = 1
        while (folder / (candidate + extension)).exists():
            candidate = f"{base_name}_{counter}"
            counter += 1
        return candidate

    def organize(self, source_folder: str) -> Dict[str, List[str]]:
        result = {}
        files = scan_directory(source_folder)

        for path in files:
            extension = path.suffix.lower()
            target_folder_name = self.EXTENSION_MAP.get(extension, "others")
            target_folder = Path(source_folder) / target_folder_name
            create_directory_if_not_exists(target_folder)

            content = None
            if extension in [".txt"]:
                content = self._read_file_content(path)

            file_model = FileModel(
                original_path=path,
                name=path.stem,
                extension=extension,
                content=content
            )

            new_name = sanitize_filename(self.ai_service.generate_new_filename(file_model))
            unique_name = self._unique_name(target_folder, new_name, extension)

            renamed_path = self.file_service.rename_file(path, unique_name)
            final_path = target_folder / renamed_path.name
            move_file(renamed_path, final_path)

            result.setdefault(target_folder_name, []).append(final_path.name)

        return result
