"""
IDaaS Python SDK - Browser Utility

This module provides utilities for opening URLs in a browser.
"""

import webbrowser
from typing import Union
from urllib.parse import urlparse


class BrowserUtil:
    """
    Utility class for browser operations.
    """

    @staticmethod
    def open(uri: Union[str, object]) -> None:
        """
        Open a URI in the default browser.

        Args:
            uri: The URI to open (string or object with __str__ method).

        Raises:
            IOError: If opening the browser fails.
        """
        uri_str = str(uri)

        # Validate the URI
        try:
            parsed = urlparse(uri_str)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError("Invalid URI format")
        except Exception as e:
            raise OSError(f"Invalid URI: {e}")

        try:
            # Open in the browser
            webbrowser.open(uri_str)
        except Exception as e:
            raise OSError(f"Failed to open browser: {e}")
