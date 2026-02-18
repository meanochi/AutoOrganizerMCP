from __future__ import annotations

import asyncio
from fastmcp import FastMCP

from dotenv import load_dotenv
from services.organizer_service import OrganizerService
from services.ai_service import AIService
from services.file_service import FileService
from models.file_model import FileModel
from utils.file_utils import scan_directory, create_directory_if_not_exists, move_file
from utils.text_utils import sanitize_filename
from settings import build_settings, get_default_env_path
from models.result import ToolResult
from utils import errors

# Load environment variables
env_path = get_default_env_path()
load_dotenv(dotenv_path=env_path, override=False)

# Build settings
settings = build_settings()

# Initialize services
organizer = OrganizerService()
ai_service = AIService()
file_service = FileService()

# Create FastMCP instance
mcp = FastMCP("file-organizer-server")


# Tool: Organize Files
@mcp.tool(
    description="""Organize files in the specified directory into folders based on their type (images, documents, etc.)""")
async def organize_files(source_folder: str) -> dict:
    """
    Organizes files into folders based on their type and renames them.
    """
    try:
        # Scan the source folder and process files
        result = organizer.organize(source_folder)

        # Return the organized result
        return {"ok": True, "data": result}

    except Exception as e:
        return ToolResult(
            ok=False,
            error={"code": errors.GENERAL_ERROR, "message": str(e)}
        ).model_dump()


# Tool: Change File Names
@mcp.tool(description="""Change the names of files based on content analysis""")
async def change_file_names(source_folder: str) -> dict:
    """
    Changes the file names by analyzing their content (e.g., for text files, images, etc.).
    """
    try:
        files = scan_directory(source_folder)
        renamed_files = []

        # Iterate over files to rename them
        for path in files:
            # For simplicity, consider renaming files based on their content using AI
            file_model = FileModel(
                original_path=path,
                name=path.stem,
                extension=path.suffix,
                content=None
            )

            new_name = ai_service.generate_new_filename(file_model)
            new_name = sanitize_filename(new_name)

            renamed_path = file_service.rename_file(path, new_name)
            renamed_files.append(renamed_path.name)

        # Return the renamed files result
        return {"ok": True, "data": renamed_files}

    except Exception as e:
        return ToolResult(
            ok=False,
            error={"code": errors.GENERAL_ERROR, "message": str(e)}
        ).model_dump()


# Tool: Create Folders for Files
@mcp.tool(description="""Create folders for files based on their extension (images, documents, etc.)""")
async def create_folders_and_move_files(source_folder: str) -> dict:
    """
    Creates necessary folders for the files and moves them to their respective directories based on type.
    """
    try:
        result = organizer.organize(source_folder)
        return {"ok": True, "data": result}

    except Exception as e:
        return ToolResult(
            ok=False,
            error={"code": errors.GENERAL_ERROR, "message": str(e)}
        ).model_dump()


# Tool: Scan Directory and Display Files
@mcp.tool(description="""Scan the directory and display all files with their respective types""")
async def scan_directory_and_list_files(source_folder: str) -> dict:
    """
    Scans a directory and lists all the files found in it, grouped by file type.
    """
    try:
        files = scan_directory(source_folder)
        file_info = []

        for path in files:
            file_info.append({
                "name": path.name,
                "type": path.suffix,
                "size": path.stat().st_size
            })

        return {"ok": True, "data": file_info}

    except Exception as e:
        return ToolResult(
            ok=False,
            error={"code": errors.GENERAL_ERROR, "message": str(e)}
        ).model_dump()


# Main entry point
if __name__ == "__main__":
    mcp.run()
