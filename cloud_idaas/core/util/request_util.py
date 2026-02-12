"""
IDaaS Python SDK - Request Utility

This module provides utilities for handling HTTP requests.
"""

import hashlib
import random
import threading
import time
import urllib.parse
from datetime import datetime, timezone
from typing import Dict, Optional

from cloud_idaas.core.exceptions import CredentialException, EncodingException


class RequestUtil:
    """
    Utility class for request operations.
    """

    _seq_id = 0
    _seq_lock = threading.Lock()

    @staticmethod
    def get_iso8601_time(date: datetime) -> str:
        """
        Format a datetime as ISO8601 UTC string.

        Args:
            date: The datetime to format.

        Returns:
            ISO8601 formatted string.
        """
        return date.strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def get_utc_date(date_str: str) -> datetime:
        """
        Parse an ISO8601 UTC string to datetime.

        Args:
            date_str: The date string to parse.

        Returns:
            Parsed datetime.

        Raises:
            CredentialException: If parsing fails.
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        except ValueError as e:
            raise CredentialException(f"Failed to parse date: {e}")

    @staticmethod
    def get_unique_nonce() -> str:
        """
        Generate a unique nonce string.

        Returns:
            A unique nonce string.
        """
        thread_id = threading.get_ident()
        current_time = int(time.time() * 1000)

        with RequestUtil._seq_lock:
            seq = RequestUtil._seq_id
            RequestUtil._seq_id += 1

        rand_val = random.randint(0, 2**63 - 1)

        sb = f"{current_time}-{thread_id}-{current_time}-{seq}-{rand_val}"

        try:
            digest = hashlib.md5(sb.encode("utf-8")).hexdigest()
            return digest
        except Exception as e:
            raise CredentialException(f"Failed to generate nonce: {e}")

    @staticmethod
    def compose_url(endpoint: str, path: Optional[str], queries: Dict[str, str], protocol: str) -> str:
        """
        Compose a URL from components.

        Args:
            endpoint: The endpoint (hostname).
            path: The path (optional).
            queries: Query parameters.
            protocol: The protocol (e.g., "https").

        Returns:
            Composed URL.

        Raises:
            EncodingException: If URL encoding fails.
        """
        url_builder = f"{protocol}://{endpoint}"
        if path is not None:
            url_builder += path
        url_builder += "?"

        builder_parts = []

        try:
            for key, val in queries.items():
                encoded_key = urllib.parse.quote(str(key), safe="")
                encoded_val = urllib.parse.quote(str(val), safe="")
                if val is not None:
                    builder_parts.append(f"{encoded_key}={encoded_val}")
        except Exception as e:
            raise EncodingException(f"Failed to encode URL: {e}")

        query = "&".join(builder_parts)
        return url_builder + query
