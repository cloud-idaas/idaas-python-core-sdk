"""
IDaaS Python SDK - Exception Analyzer

This module provides utilities for analyzing exceptions.
"""


class ExceptionAnalyzer:
    """
    Utility class for analyzing exceptions.
    """

    MAX_CAUSE_DEPTH = 5

    @staticmethod
    def is_target_cause_exist(throwable: Exception, cause_clazz: type, sub_message: str) -> bool:
        """
        Check if a target cause exists in the exception chain.

        Args:
            throwable: The exception to analyze.
            cause_clazz: The class of the cause to look for.
            sub_message: The message substring to look for.

        Returns:
            True if the target cause exists, False otherwise.
        """
        current_depth = 0
        cause = throwable

        while cause is not None:
            if isinstance(cause, cause_clazz):
                if str(cause) is not None and sub_message in str(cause):
                    return True

            cause = cause.__cause__
            current_depth += 1
            if current_depth >= ExceptionAnalyzer.MAX_CAUSE_DEPTH:
                break

        return False

    @staticmethod
    def is_target_cause_exist_by_message(throwable: Exception, sub_message: str) -> bool:
        """
        Check if a specific message exists in the exception.

        Args:
            throwable: The exception to analyze.
            sub_message: The message substring to look for.

        Returns:
            True if the message exists, False otherwise.
        """
        return sub_message in str(throwable)
