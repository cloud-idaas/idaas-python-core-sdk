"""
IDaaS Python SDK - File Utility

This module provides file reading and writing utilities.
"""

import os
from pathlib import Path
from typing import Optional


class FileUtil:
    """
    Utility class for file operations.
    """

    @staticmethod
    def read_file(file_path: str) -> Optional[str]:
        """
        Read file content as string.

        Args:
            file_path: Path to the file.

        Returns:
            File content as string, or None if file doesn't exist or read fails.

        Raises:
            IOError: If file doesn't exist.
        """
        if not os.path.exists(file_path):
            raise OSError("File does not exist")

        try:
            with open(file_path, encoding="utf-8") as f:
                return f.read()
        except OSError as e:
            print(f"Error reading file: {e}")
            return None

    @staticmethod
    def write_file(file_path: str, content: str) -> None:
        """
        Write content to file.

        Args:
            file_path: Path to the file.
            content: Content to write.
        """
        path = Path(file_path)

        # Create parent directories and file if they don't exist
        if not path.exists():
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch()
            except OSError as e:
                print(f"Error creating file: {e}")

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        except OSError as e:
            print(f"Error writing file: {e}")
