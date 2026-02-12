"""
Tests for RefreshResult class
"""

import unittest
from datetime import datetime, timedelta, timezone

from cloud_idaas.core.cache.refresh_result import RefreshResult, RefreshResultBuilder


class TestRefreshResult(unittest.TestCase):
    """Test cases for RefreshResult class"""

    def test_refresh_result_creation(self):
        """Test RefreshResult creation with all parameters"""
        value = "test_value"
        stale_time = datetime.now(timezone.utc) + timedelta(hours=1)
        prefetch_time = datetime.now(timezone.utc) + timedelta(minutes=30)

        result = RefreshResult(value, stale_time, prefetch_time)

        self.assertEqual(result.value, value)
        self.assertEqual(result.stale_time, stale_time)
        self.assertEqual(result.prefetch_time, prefetch_time)

    def test_refresh_result_creation_with_none_times(self):
        """Test RefreshResult creation with None times"""
        value = "test_value"
        result = RefreshResult(value, None, None)

        self.assertEqual(result.value, value)
        self.assertIsNone(result.stale_time)
        self.assertIsNone(result.prefetch_time)

    def test_refresh_result_creation_with_stale_time_only(self):
        """Test RefreshResult creation with only stale_time"""
        value = "test_value"
        stale_time = datetime.now(timezone.utc) + timedelta(hours=1)
        result = RefreshResult(value, stale_time, None)

        self.assertEqual(result.value, value)
        self.assertEqual(result.stale_time, stale_time)
        self.assertIsNone(result.prefetch_time)

    def test_refresh_result_creation_with_prefetch_time_only(self):
        """Test RefreshResult creation with only prefetch_time"""
        value = "test_value"
        prefetch_time = datetime.now(timezone.utc) + timedelta(minutes=30)
        result = RefreshResult(value, None, prefetch_time)

        self.assertEqual(result.value, value)
        self.assertIsNone(result.stale_time)
        self.assertEqual(result.prefetch_time, prefetch_time)

    def test_refresh_result_equality(self):
        """Test RefreshResult equality"""
        value = "test_value"
        stale_time = datetime.now(timezone.utc) + timedelta(hours=1)
        prefetch_time = datetime.now(timezone.utc) + timedelta(minutes=30)

        result1 = RefreshResult(value, stale_time, prefetch_time)
        result2 = RefreshResult(value, stale_time, prefetch_time)

        self.assertEqual(result1, result2)

    def test_refresh_result_inequality(self):
        """Test RefreshResult inequality"""
        result1 = RefreshResult("value1", None, None)
        result2 = RefreshResult("value2", None, None)

        self.assertNotEqual(result1, result2)

    def test_refresh_result_equality_with_different_value(self):
        """Test RefreshResult inequality with different value"""
        stale_time = datetime.now(timezone.utc) + timedelta(hours=1)
        result1 = RefreshResult("value1", stale_time, None)
        result2 = RefreshResult("value2", stale_time, None)

        self.assertNotEqual(result1, result2)

    def test_refresh_result_equality_with_different_stale_time(self):
        """Test RefreshResult inequality with different stale_time"""
        result1 = RefreshResult("value", datetime.now(timezone.utc), None)
        result2 = RefreshResult("value", datetime.now(timezone.utc) + timedelta(hours=1), None)

        self.assertNotEqual(result1, result2)

    def test_refresh_result_equality_with_different_prefetch_time(self):
        """Test RefreshResult inequality with different prefetch_time"""
        result1 = RefreshResult("value", None, datetime.now(timezone.utc))
        result2 = RefreshResult("value", None, datetime.now(timezone.utc) + timedelta(minutes=30))

        self.assertNotEqual(result1, result2)

    def test_refresh_result_equality_with_non_refresh_result(self):
        """Test RefreshResult equality with non-RefreshResult object"""
        result = RefreshResult("value", None, None)
        self.assertNotEqual(result, "value")
        self.assertNotEqual(result, None)
        self.assertNotEqual(result, {"value": "value"})

    def test_refresh_result_hash(self):
        """Test RefreshResult hash"""
        value = "test_value"
        stale_time = datetime.now(timezone.utc) + timedelta(hours=1)
        prefetch_time = datetime.now(timezone.utc) + timedelta(minutes=30)

        result1 = RefreshResult(value, stale_time, prefetch_time)
        result2 = RefreshResult(value, stale_time, prefetch_time)

        self.assertEqual(hash(result1), hash(result2))

    def test_refresh_result_hash_consistency(self):
        """Test that hash is consistent across multiple calls"""
        result = RefreshResult("value", None, None)
        hash1 = hash(result)
        hash2 = hash(result)
        self.assertEqual(hash1, hash2)

    def test_refresh_result_hash_for_set(self):
        """Test that RefreshResult can be used in a set"""
        result1 = RefreshResult("value1", None, None)
        result2 = RefreshResult("value1", None, None)
        result3 = RefreshResult("value2", None, None)

        result_set = {result1, result2, result3}

        # Should contain only 2 unique elements (result1 and result2 are same)
        self.assertEqual(len(result_set), 2)

    def test_refresh_result_hash_for_dict_key(self):
        """Test that RefreshResult can be used as dict key"""
        result1 = RefreshResult("key1", None, None)
        result2 = RefreshResult("key1", None, None)
        result3 = RefreshResult("key2", None, None)

        result_dict = {result1: "value1", result3: "value3"}

        # result2 should map to same value as result1
        self.assertEqual(result_dict[result2], "value1")
        self.assertEqual(result_dict[result3], "value3")
        self.assertEqual(len(result_dict), 2)

    def test_refresh_result_repr(self):
        """Test RefreshResult string representation"""
        value = "test_value"
        stale_time = datetime.now(timezone.utc) + timedelta(hours=1)
        prefetch_time = datetime.now(timezone.utc) + timedelta(minutes=30)

        result = RefreshResult(value, stale_time, prefetch_time)
        repr_str = repr(result)

        self.assertIn("test_value", repr_str)
        self.assertIn("RefreshResult", repr_str)
        self.assertIn("stale_time", repr_str)
        self.assertIn("prefetch_time", repr_str)

    def test_refresh_result_repr_with_none_times(self):
        """Test RefreshResult repr with None times"""
        result = RefreshResult("value", None, None)
        repr_str = repr(result)

        self.assertIn("value", repr_str)
        self.assertIn("RefreshResult", repr_str)
        self.assertIn("None", repr_str)

    def test_refresh_result_properties_are_readonly(self):
        """Test that properties are read-only"""
        result = RefreshResult("value", None, None)

        # Properties should be accessible
        self.assertEqual(result.value, "value")
        self.assertIsNone(result.stale_time)
        self.assertIsNone(result.prefetch_time)

        # Attempting to set properties should fail
        with self.assertRaises(AttributeError):
            result.value = "new_value"
        with self.assertRaises(AttributeError):
            result.stale_time = datetime.now(timezone.utc)
        with self.assertRaises(AttributeError):
            result.prefetch_time = datetime.now(timezone.utc)

    def test_refresh_result_with_complex_value(self):
        """Test RefreshResult with complex value types"""
        # Test with dict
        dict_value = {"key": "value", "nested": {"inner": "data"}}
        result = RefreshResult(dict_value, None, None)
        self.assertEqual(result.value, dict_value)

        # Test with list
        list_value = [1, 2, 3, {"key": "value"}]
        result = RefreshResult(list_value, None, None)
        self.assertEqual(result.value, list_value)

        # Test with custom class
        class CustomClass:
            def __init__(self, value):
                self.value = value

        custom_value = CustomClass("test")
        result = RefreshResult(custom_value, None, None)
        self.assertEqual(result.value.value, "test")

    def test_refresh_result_with_none_value(self):
        """Test RefreshResult with None value"""
        result = RefreshResult(None, None, None)
        self.assertIsNone(result.value)

    def test_refresh_result_with_numeric_value(self):
        """Test RefreshResult with numeric values"""
        # Test with int
        result = RefreshResult(42, None, None)
        self.assertEqual(result.value, 42)
        self.assertIsInstance(result.value, int)

        # Test with float
        result = RefreshResult(3.14, None, None)
        self.assertEqual(result.value, 3.14)
        self.assertIsInstance(result.value, float)

    def test_refresh_result_with_boolean_value(self):
        """Test RefreshResult with boolean values"""
        result_true = RefreshResult(True, None, None)
        self.assertTrue(result_true.value)

        result_false = RefreshResult(False, None, None)
        self.assertFalse(result_false.value)

        # Boolean values should not be equal
        self.assertNotEqual(result_true, result_false)


class TestRefreshResultBuilder(unittest.TestCase):
    """Test cases for RefreshResultBuilder class"""

    def test_builder_with_all_parameters(self):
        """Test builder with all parameters"""
        value = "test_value"
        stale_time = datetime.now(timezone.utc) + timedelta(hours=1)
        prefetch_time = datetime.now(timezone.utc) + timedelta(minutes=30)

        result = RefreshResult.builder(value).stale_time(stale_time).prefetch_time(prefetch_time).build()

        self.assertEqual(result.value, value)
        self.assertEqual(result.stale_time, stale_time)
        self.assertEqual(result.prefetch_time, prefetch_time)

    def test_builder_with_value_only(self):
        """Test builder with only value"""
        value = "test_value"
        result = RefreshResult.builder(value).build()

        self.assertEqual(result.value, value)
        self.assertIsNone(result.stale_time)
        self.assertIsNone(result.prefetch_time)

    def test_builder_chaining(self):
        """Test builder method chaining"""
        value = "test_value"
        stale_time = datetime.now(timezone.utc) + timedelta(hours=1)
        prefetch_time = datetime.now(timezone.utc) + timedelta(minutes=30)

        builder = RefreshResult.builder(value)
        self.assertIsInstance(builder.stale_time(stale_time), RefreshResultBuilder)
        self.assertIsInstance(builder.prefetch_time(prefetch_time), RefreshResultBuilder)

    def test_builder_with_stale_time_only(self):
        """Test builder with only stale_time"""
        value = "test_value"
        stale_time = datetime.now(timezone.utc) + timedelta(hours=1)

        result = RefreshResult.builder(value).stale_time(stale_time).build()

        self.assertEqual(result.value, value)
        self.assertEqual(result.stale_time, stale_time)
        self.assertIsNone(result.prefetch_time)

    def test_builder_with_prefetch_time_only(self):
        """Test builder with only prefetch_time"""
        value = "test_value"
        prefetch_time = datetime.now(timezone.utc) + timedelta(minutes=30)

        result = RefreshResult.builder(value).prefetch_time(prefetch_time).build()

        self.assertEqual(result.value, value)
        self.assertIsNone(result.stale_time)
        self.assertEqual(result.prefetch_time, prefetch_time)

    def test_builder_reverse_order(self):
        """Test builder with parameters in reverse order"""
        value = "test_value"
        stale_time = datetime.now(timezone.utc) + timedelta(hours=1)
        prefetch_time = datetime.now(timezone.utc) + timedelta(minutes=30)

        result = RefreshResult.builder(value).prefetch_time(prefetch_time).stale_time(stale_time).build()

        self.assertEqual(result.value, value)
        self.assertEqual(result.stale_time, stale_time)
        self.assertEqual(result.prefetch_time, prefetch_time)

    def test_builder_multiple_builds(self):
        """Test that builder can be used to build multiple results"""
        value = "test_value"
        stale_time1 = datetime.now(timezone.utc) + timedelta(hours=1)
        stale_time2 = datetime.now(timezone.utc) + timedelta(hours=2)

        builder = RefreshResult.builder(value)

        result1 = builder.stale_time(stale_time1).build()
        result2 = builder.stale_time(stale_time2).build()

        self.assertEqual(result1.value, value)
        self.assertEqual(result1.stale_time, stale_time1)
        self.assertEqual(result2.value, value)
        self.assertEqual(result2.stale_time, stale_time2)

    def test_builder_with_none_value(self):
        """Test builder with None value"""
        result = RefreshResult.builder(None).build()
        self.assertIsNone(result.value)

    def test_builder_with_complex_value(self):
        """Test builder with complex value"""
        dict_value = {"key": "value"}
        result = RefreshResult.builder(dict_value).build()
        self.assertEqual(result.value, dict_value)

    def test_builder_creates_fresh_instance(self):
        """Test that builder creates fresh RefreshResult instances"""
        value = "test_value"
        stale_time = datetime.now(timezone.utc) + timedelta(hours=1)

        result1 = RefreshResult.builder(value).stale_time(stale_time).build()
        result2 = RefreshResult.builder(value).stale_time(stale_time).build()

        # Should be equal but not the same object
        self.assertEqual(result1, result2)
        self.assertIsNot(result1, result2)


if __name__ == "__main__":
    unittest.main()
