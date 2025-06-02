"""
File operations and validation.
"""
import os
from typing import List
from gbofe.exceptions import InvalidFileFormatError, FileNoFoundError

def validate_file_path(file_path: str, allowed_extensions: List[str]) -> bool:
    """
    Validates that the file exists and has an allowed extension.

    Args:
        file_path: File path
        allowed_extensions: List of allowed extensions

    Returns:
        True if the file is valid

    Raises:
        FileNoFoundError: If the file does not exist,
        InvalidFileFormatError: If the extension is not valid
    """
    if not os.path.isfile(file_path):
        raise FileNoFoundError(f"File {file_path} does not exist")

    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension not in allowed_extensions:
        raise InvalidFileFormatError(
            f"Extension {file_extension} not supported. "
            f"Allowed extensions: {allowed_extensions}"
        )

    return True

def create_output_directory(output_path: str) -> None:
    """
    Creates the output directory if it does not exist.

    Args:
        output_path: Output directory path
    """
    directory = os.path.dirname(output_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)