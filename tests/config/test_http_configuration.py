"""
Tests for HttpConfiguration class
"""

import unittest

from cloud_idaas.core.config.http_configuration import HttpConfiguration


class TestHttpConfiguration(unittest.TestCase):
    """Test cases for HttpConfiguration class"""

    def test_default_values(self):
        """Test default values"""
        config = HttpConfiguration()
        self.assertEqual(config.connect_timeout, 5000)
        self.assertEqual(config.read_timeout, 10000)
        self.assertFalse(config.unsafe_ignore_ssl_cert)

    def test_set_properties(self):
        """Test setting properties"""
        config = HttpConfiguration()
        config.connect_timeout = 3000
        config.read_timeout = 5000
        config.unsafe_ignore_ssl_cert = True

        self.assertEqual(config.connect_timeout, 3000)
        self.assertEqual(config.read_timeout, 5000)
        self.assertTrue(config.unsafe_ignore_ssl_cert)

    def test_copy(self):
        """Test copy method"""
        source = HttpConfiguration()
        source.connect_timeout = 3000
        source.read_timeout = 5000
        source.unsafe_ignore_ssl_cert = True

        target = HttpConfiguration.copy(source)
        self.assertEqual(target.connect_timeout, 3000)
        self.assertEqual(target.read_timeout, 5000)
        self.assertTrue(target.unsafe_ignore_ssl_cert)

    def test_copy_none(self):
        """Test copy method with None"""
        result = HttpConfiguration.copy(None)
        self.assertIsNone(result)

    def test_copy_creates_new_instance(self):
        """Test that copy creates a new instance"""
        source = HttpConfiguration()
        target = HttpConfiguration.copy(source)
        self.assertIsNot(source, target)

    def test_repr(self):
        """Test __repr__ method"""
        config = HttpConfiguration()
        config.connect_timeout = 3000
        config.read_timeout = 5000
        config.unsafe_ignore_ssl_cert = True

        repr_str = repr(config)
        self.assertIn("HttpConfiguration", repr_str)
        self.assertIn("3000", repr_str)
        self.assertIn("5000", repr_str)
        self.assertIn("True", repr_str)

    def test_repr_default(self):
        """Test __repr__ method with default values"""
        config = HttpConfiguration()
        repr_str = repr(config)
        self.assertIn("HttpConfiguration", repr_str)
        self.assertIn("5000", repr_str)  # default connect_timeout
        self.assertIn("10000", repr_str)  # default read_timeout

    def test_eq_equal(self):
        """Test __eq__ method with equal configs"""
        config1 = HttpConfiguration()
        config1.connect_timeout = 3000
        config1.read_timeout = 5000
        config1.unsafe_ignore_ssl_cert = True

        config2 = HttpConfiguration()
        config2.connect_timeout = 3000
        config2.read_timeout = 5000
        config2.unsafe_ignore_ssl_cert = True

        self.assertEqual(config1, config2)

    def test_eq_not_equal_connect_timeout(self):
        """Test __eq__ method with different connect_timeout"""
        config1 = HttpConfiguration()
        config1.connect_timeout = 3000
        config1.read_timeout = 5000

        config2 = HttpConfiguration()
        config2.connect_timeout = 4000
        config2.read_timeout = 5000

        self.assertNotEqual(config1, config2)

    def test_eq_not_equal_read_timeout(self):
        """Test __eq__ method with different read_timeout"""
        config1 = HttpConfiguration()
        config1.connect_timeout = 3000
        config1.read_timeout = 5000

        config2 = HttpConfiguration()
        config2.connect_timeout = 3000
        config2.read_timeout = 6000

        self.assertNotEqual(config1, config2)

    def test_eq_not_equal_unsafe_ignore_ssl_cert(self):
        """Test __eq__ method with different unsafe_ignore_ssl_cert"""
        config1 = HttpConfiguration()
        config1.connect_timeout = 3000
        config1.unsafe_ignore_ssl_cert = True

        config2 = HttpConfiguration()
        config2.connect_timeout = 3000
        config2.unsafe_ignore_ssl_cert = False

        self.assertNotEqual(config1, config2)

    def test_eq_with_default_values(self):
        """Test __eq__ method with default values"""
        config1 = HttpConfiguration()
        config2 = HttpConfiguration()
        self.assertEqual(config1, config2)

    def test_eq_different_type(self):
        """Test __eq__ method with different type"""
        config = HttpConfiguration()

        self.assertNotEqual(config, 5000)
        self.assertNotEqual(config, "HttpConfiguration")
        self.assertNotEqual(config, None)

    def test_hash_equal(self):
        """Test __hash__ method with equal configs"""
        config1 = HttpConfiguration()
        config1.connect_timeout = 3000
        config1.read_timeout = 5000
        config1.unsafe_ignore_ssl_cert = True

        config2 = HttpConfiguration()
        config2.connect_timeout = 3000
        config2.read_timeout = 5000
        config2.unsafe_ignore_ssl_cert = True

        self.assertEqual(hash(config1), hash(config2))

    def test_hash_not_equal(self):
        """Test __hash__ method with different configs"""
        config1 = HttpConfiguration()
        config1.connect_timeout = 3000
        config1.read_timeout = 5000

        config2 = HttpConfiguration()
        config2.connect_timeout = 4000
        config2.read_timeout = 5000

        self.assertNotEqual(hash(config1), hash(config2))

    def test_hash_consistent(self):
        """Test __hash__ method returns consistent hash"""
        config = HttpConfiguration()
        config.connect_timeout = 3000
        config.read_timeout = 5000

        hash1 = hash(config)
        hash2 = hash(config)
        self.assertEqual(hash1, hash2)

    def test_hash_with_default_values(self):
        """Test __hash__ method with default values"""
        config1 = HttpConfiguration()
        config2 = HttpConfiguration()
        self.assertEqual(hash(config1), hash(config2))

    def test_can_use_in_set(self):
        """Test that HttpConfiguration can be used in a set"""
        config1 = HttpConfiguration()
        config1.connect_timeout = 3000
        config1.read_timeout = 5000
        config1.unsafe_ignore_ssl_cert = True

        config2 = HttpConfiguration()
        config2.connect_timeout = 3000
        config2.read_timeout = 5000
        config2.unsafe_ignore_ssl_cert = True

        config3 = HttpConfiguration()
        config3.connect_timeout = 4000
        config3.read_timeout = 5000

        config_set = {config1, config2, config3}
        self.assertEqual(len(config_set), 2)  # config1 and config2 are equal

    def test_can_use_as_dict_key(self):
        """Test that HttpConfiguration can be used as dict key"""
        config1 = HttpConfiguration()
        config1.connect_timeout = 3000
        config1.read_timeout = 5000

        config2 = HttpConfiguration()
        config2.connect_timeout = 3000
        config2.read_timeout = 5000

        config3 = HttpConfiguration()
        config3.connect_timeout = 4000
        config3.read_timeout = 5000

        config_dict = {}
        config_dict[config1] = "value1"
        config_dict[config2] = "value2"
        config_dict[config3] = "value3"

        self.assertEqual(len(config_dict), 2)  # config1 and config2 are the same key
        self.assertEqual(config_dict[config1], "value2")  # value was overwritten
        self.assertEqual(config_dict[config3], "value3")


if __name__ == "__main__":
    unittest.main()
