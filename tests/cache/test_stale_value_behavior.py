"""
Tests for StaleValueBehavior enum
"""

import unittest

from cloud_idaas.core.cache.stale_value_behavior import StaleValueBehavior, _StrEnum


class TestStrEnum(unittest.TestCase):
    """Test cases for _StrEnum base class"""

    def test_str_enum_string_conversion(self):
        """Test that _StrEnum returns value when converted to string"""

        class TestEnum(_StrEnum):
            TEST_VALUE = "test_value"

        self.assertEqual(str(TestEnum.TEST_VALUE), "test_value")

    def test_str_enum_in_string_interpolation(self):
        """Test _StrEnum in string interpolation"""

        class TestEnum(_StrEnum):
            TEST_VALUE = "test_value"

        result = f"Value is {TestEnum.TEST_VALUE}"
        self.assertEqual(result, "Value is test_value")


class TestStaleValueBehavior(unittest.TestCase):
    """Test cases for StaleValueBehavior enum"""

    def test_strict_value(self):
        """Test STRICT enum value"""
        self.assertEqual(StaleValueBehavior.STRICT.value, "STRICT")

    def test_allow_value(self):
        """Test ALLOW enum value"""
        self.assertEqual(StaleValueBehavior.ALLOW.value, "ALLOW")

    def test_enum_members(self):
        """Test enum has expected members"""
        self.assertIn(StaleValueBehavior.STRICT, StaleValueBehavior)
        self.assertIn(StaleValueBehavior.ALLOW, StaleValueBehavior)

    def test_enum_comparison(self):
        """Test enum comparison"""
        self.assertEqual(StaleValueBehavior.STRICT, StaleValueBehavior.STRICT)
        self.assertNotEqual(StaleValueBehavior.STRICT, StaleValueBehavior.ALLOW)

    def test_str_method_strict(self):
        """Test __str__ method returns value for STRICT"""
        self.assertEqual(str(StaleValueBehavior.STRICT), "STRICT")

    def test_str_method_allow(self):
        """Test __str__ method returns value for ALLOW"""
        self.assertEqual(str(StaleValueBehavior.ALLOW), "ALLOW")

    def test_str_in_string_format(self):
        """Test StaleValueBehavior in string formatting"""
        result = f"Behavior: {StaleValueBehavior.STRICT}"
        self.assertEqual(result, "Behavior: STRICT")

    def test_str_in_string_concatenation(self):
        """Test StaleValueBehavior in string concatenation"""
        result = "Behavior: " + str(StaleValueBehavior.ALLOW)
        self.assertEqual(result, "Behavior: ALLOW")

    def test_enum_iteration(self):
        """Test iterating over enum members"""
        members = list(StaleValueBehavior)
        self.assertEqual(len(members), 2)
        self.assertIn(StaleValueBehavior.STRICT, members)
        self.assertIn(StaleValueBehavior.ALLOW, members)

    def test_enum_name(self):
        """Test enum name property"""
        self.assertEqual(StaleValueBehavior.STRICT.name, "STRICT")
        self.assertEqual(StaleValueBehavior.ALLOW.name, "ALLOW")

    def test_enum_value(self):
        """Test enum value property"""
        self.assertEqual(StaleValueBehavior.STRICT.value, "STRICT")
        self.assertEqual(StaleValueBehavior.ALLOW.value, "ALLOW")

    def test_enum_hashable(self):
        """Test that enum is hashable"""
        enum_set = {StaleValueBehavior.STRICT, StaleValueBehavior.ALLOW}
        self.assertEqual(len(enum_set), 2)


if __name__ == "__main__":
    unittest.main()
