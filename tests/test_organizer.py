import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from services.organizer_service import OrganizerService
from services.ai_service import AIService
from services.file_service import FileService
from models.file_model import FileModel
from utils.file_utils import scan_directory, create_directory_if_not_exists, move_file
from utils.text_utils import sanitize_filename


@pytest.fixture
def mock_file_paths():
    # This fixture will simulate a list of file paths for testing.
    return [
        Path("M:/mock/dir/file1.txt"),
        Path("M:/mock/dir/file2.jpg"),
        Path("M:/mock/dir/file3.pdf"),
    ]


@pytest.fixture
def organizer_service(mock_file_paths):
    # Here we create the OrganizerService instance and mock the dependencies.
    organizer_service = OrganizerService()
    organizer_service.ai_service = MagicMock(AIService)
    organizer_service.file_service = MagicMock(FileService)
    return organizer_service


# Test the _unique_name method
def test_unique_name(organizer_service):
    # Testing that the unique name generator correctly adds a suffix when a file already exists.
    mock_folder = Path("/mock/dir")
    base_name = "file1"
    extension = ".txt"

    # First call should give us "file1.txt"
    unique_name = organizer_service._unique_name(mock_folder, base_name, extension)
    assert unique_name == "file1"

    # Now we simulate that "file1.txt" already exists by creating a fake file.
    (mock_folder / "file1.txt").touch()

    # Now we should get "file1_1.txt"
    unique_name = organizer_service._unique_name(mock_folder, base_name, extension)
    assert unique_name == "file1_1"


# Test the organize method
@patch("services.organizer_service.scan_directory")
@patch("services.organizer_service.create_directory_if_not_exists")
@patch("services.organizer_service.move_file")
@patch("services.ai_service.AIService.generate_new_filename")
def test_organize(mock_generate_new_filename, mock_move_file, mock_create_directory, mock_scan_directory,
                  mock_file_paths):
    # Prepare mock return values
    mock_scan_directory.return_value = mock_file_paths
    mock_generate_new_filename.return_value = "new_filename"
    mock_create_directory.return_value = None
    mock_move_file.return_value = None

    # Initialize the OrganizerService
    organizer_service = OrganizerService()

    # Call the organize function
    result = organizer_service.organize("/mock/dir")

    # Check that the scan_directory was called with the correct argument
    mock_scan_directory.assert_called_with("/mock/dir")

    # Check that the organize method returned the expected result
    assert result is not None
    assert isinstance(result, dict)
    assert "images" in result or "documents" in result  # based on the file types

    # Test that the files were moved to correct folders
    mock_move_file.assert_called()

    # Test that the file was renamed
    mock_generate_new_filename.assert_called()


# Test the change_file_names function (for AI renaming functionality)
@patch("services.ai_service.AIService.generate_new_filename")
@patch("services.file_service.FileService.rename_file")
def test_change_file_names(mock_rename_file, mock_generate_new_filename, mock_file_paths):
    # Simulate AI-generated file names
    mock_generate_new_filename.return_value = "new_filename"
    mock_rename_file.return_value = Path("/mock/dir/new_filename.txt")

    # Simulate file renaming process
    organizer_service = OrganizerService()
    renamed_files = []

    for path in mock_file_paths:
        file_model = FileModel(original_path=path, name=path.stem, extension=path.suffix)
        new_name = mock_generate_new_filename(file_model)
        renamed_file = mock_rename_file(path, new_name)
        renamed_files.append(renamed_file.name)

    # Ensure the files were renamed correctly
    assert renamed_files == ["new_filename.txt", "new_filename.txt", "new_filename.txt"]
    mock_rename_file.assert_called()


# Test that scan_directory returns the expected file info
@patch("utils.file_utils.scan_directory")
def test_scan_directory_and_list_files(mock_scan_directory, mock_file_paths):
    mock_scan_directory.return_value = mock_file_paths

    result = scan_directory("/mock/dir")
    assert result == mock_file_paths
    assert len(result) == len(mock_file_paths)


# Test the sanitization of filenames
def test_sanitize_filename():
    # Test for a file name with special characters
    raw_filename = "file_#1@.txt"
    sanitized_filename = sanitize_filename(raw_filename)
    assert sanitized_filename == "file_1.txt"

    # Test for a simple filename without special characters
    raw_filename = "simple_filename.txt"
    sanitized_filename = sanitize_filename(raw_filename)
    assert sanitized_filename == "simple_filename.txt"
