"""
Tests for ExceptionAnalyzer class
"""

import unittest

from cloud_idaas.core.util.exception_analyzer import ExceptionAnalyzer


class TestExceptionAnalyzer(unittest.TestCase):
    """Test cases for ExceptionAnalyzer class"""

    def test_max_cause_depth(self):
        """Test MAX_CAUSE_DEPTH constant"""
        self.assertEqual(ExceptionAnalyzer.MAX_CAUSE_DEPTH, 5)

    def test_is_target_cause_exist_with_matching_cause(self):
        """Test is_target_cause_exist with matching cause"""
        try:
            raise ValueError("test error message")
        except Exception as e:
            result = ExceptionAnalyzer.is_target_cause_exist(e, ValueError, "test error")
            self.assertTrue(result)

    def test_is_target_cause_exist_with_non_matching_cause(self):
        """Test is_target_cause_exist with non-matching cause"""
        try:
            raise ValueError("test error message")
        except Exception as e:
            result = ExceptionAnalyzer.is_target_cause_exist(e, TypeError, "test error")
            self.assertFalse(result)

    def test_is_target_cause_exist_with_non_matching_message(self):
        """Test is_target_cause_exist with non-matching message"""
        try:
            raise ValueError("test error message")
        except Exception as e:
            result = ExceptionAnalyzer.is_target_cause_exist(e, ValueError, "other message")
            self.assertFalse(result)

    def test_is_target_cause_exist_with_none_message(self):
        """Test is_target_cause_exist with None message"""
        try:
            raise ValueError()
        except Exception as e:
            result = ExceptionAnalyzer.is_target_cause_exist(e, ValueError, "test")
            self.assertFalse(result)

    def test_is_target_cause_exist_with_chained_exception(self):
        """Test is_target_cause_exist with chained exception"""
        try:
            try:
                raise ValueError("inner error")
            except ValueError as inner_e:
                raise TypeError("outer error") from inner_e
        except TypeError as e:
            result = ExceptionAnalyzer.is_target_cause_exist(e, ValueError, "inner error")
            self.assertTrue(result)

    def test_is_target_cause_exist_by_message(self):
        """Test is_target_cause_exist_by_message"""
        try:
            raise ValueError("test error message")
        except Exception as e:
            result = ExceptionAnalyzer.is_target_cause_exist_by_message(e, "test error")
            self.assertTrue(result)

    def test_is_target_cause_exist_by_message_not_found(self):
        """Test is_target_cause_exist_by_message with message not found"""
        try:
            raise ValueError("test error message")
        except Exception as e:
            result = ExceptionAnalyzer.is_target_cause_exist_by_message(e, "other message")
            self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
