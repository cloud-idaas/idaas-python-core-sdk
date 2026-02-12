"""
Tests for HttpResponse class
"""

import unittest

from cloud_idaas import HttpResponse


class TestHttpResponse(unittest.TestCase):
    """Test cases for HttpResponse class"""

    def test_response_with_status_and_body(self):
        """Test response with status code and body"""
        response = HttpResponse(200, '{"result": "success"}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, '{"result": "success"}')

    def test_response_with_properties(self):
        """Test response with properties set"""
        response = HttpResponse()
        response.status_code = 404
        response.body = "Not Found"

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.body, "Not Found")

    def test_is_success_2xx(self):
        """Test is_success returns True for 2xx status codes"""
        for code in range(200, 300):
            response = HttpResponse(code, "body")
            self.assertTrue(response.is_success(), f"Status code {code} should be successful")

    def test_is_success_not_2xx(self):
        """Test is_success returns False for non-2xx status codes"""
        for code in [100, 199, 300, 400, 500]:
            response = HttpResponse(code, "body")
            self.assertFalse(response.is_success(), f"Status code {code} should not be successful")

    def test_response_with_headers(self):
        """Test response with headers"""
        response = HttpResponse(200, "body")
        response.headers = {"Content-Type": "application/json"}

        self.assertEqual(response.headers["Content-Type"], "application/json")

    def test_response_with_none_body(self):
        """Test response with None body"""
        response = HttpResponse(200)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.body)

    def test_repr(self):
        """Test __repr__ method"""
        response = HttpResponse(200, '{"result": "success"}')
        response.headers = {"Content-Type": "application/json"}

        repr_str = repr(response)
        self.assertIn("HttpResponse", repr_str)
        self.assertIn("200", repr_str)
        self.assertIn('{"result": "success"}', repr_str)

    def test_repr_empty(self):
        """Test __repr__ method with minimal response"""
        response = HttpResponse()
        repr_str = repr(response)
        self.assertIn("HttpResponse", repr_str)

    def test_eq_equal(self):
        """Test __eq__ method with equal responses"""
        headers = {"Content-Type": "application/json"}
        response1 = HttpResponse(200, '{"result": "success"}')
        response1.headers = headers

        response2 = HttpResponse(200, '{"result": "success"}')
        response2.headers = headers

        self.assertEqual(response1, response2)

    def test_eq_not_equal_status_code(self):
        """Test __eq__ method with different status code"""
        response1 = HttpResponse(200, '{"result": "success"}')
        response2 = HttpResponse(404, '{"result": "success"}')

        self.assertNotEqual(response1, response2)

    def test_eq_not_equal_body(self):
        """Test __eq__ method with different body"""
        response1 = HttpResponse(200, '{"result": "success"}')
        response2 = HttpResponse(200, '{"result": "failure"}')

        self.assertNotEqual(response1, response2)

    def test_eq_not_equal_headers(self):
        """Test __eq__ method with different headers"""
        response1 = HttpResponse(200, '{"result": "success"}')
        response1.headers = {"Content-Type": "application/json"}

        response2 = HttpResponse(200, '{"result": "success"}')
        response2.headers = {"Content-Type": "application/xml"}

        self.assertNotEqual(response1, response2)

    def test_eq_with_none_values(self):
        """Test __eq__ method with None values"""
        response1 = HttpResponse()
        response2 = HttpResponse()
        self.assertEqual(response1, response2)

    def test_eq_different_type(self):
        """Test __eq__ method with different type"""
        response = HttpResponse(200, '{"result": "success"}')

        self.assertNotEqual(response, 200)
        self.assertNotEqual(response, '{"result": "success"}')
        self.assertNotEqual(response, None)

    def test_hash_equal(self):
        """Test __hash__ method with equal responses"""
        headers = {"Content-Type": "application/json"}
        response1 = HttpResponse(200, '{"result": "success"}')
        response1.headers = headers

        response2 = HttpResponse(200, '{"result": "success"}')
        response2.headers = headers

        self.assertEqual(hash(response1), hash(response2))

    def test_hash_not_equal(self):
        """Test __hash__ method with different responses"""
        response1 = HttpResponse(200, '{"result": "success"}')
        response2 = HttpResponse(404, '{"result": "success"}')

        self.assertNotEqual(hash(response1), hash(response2))

    def test_hash_consistent(self):
        """Test __hash__ method returns consistent hash"""
        response = HttpResponse(200, '{"result": "success"}')
        hash1 = hash(response)
        hash2 = hash(response)
        self.assertEqual(hash1, hash2)

    def test_hash_with_none_values(self):
        """Test __hash__ method with None values"""
        response1 = HttpResponse()
        response2 = HttpResponse()
        self.assertEqual(hash(response1), hash(response2))

    def test_can_use_in_set(self):
        """Test that HttpResponse can be used in a set"""
        headers = {"Content-Type": "application/json"}
        response1 = HttpResponse(200, '{"result": "success"}')
        response1.headers = headers

        response2 = HttpResponse(200, '{"result": "success"}')
        response2.headers = headers

        response3 = HttpResponse(404, '{"result": "failure"}')

        response_set = {response1, response2, response3}
        self.assertEqual(len(response_set), 2)  # response1 and response2 are equal

    def test_can_use_as_dict_key(self):
        """Test that HttpResponse can be used as dict key"""
        headers = {"Content-Type": "application/json"}
        response1 = HttpResponse(200, '{"result": "success"}')
        response1.headers = headers

        response2 = HttpResponse(200, '{"result": "success"}')
        response2.headers = headers

        response3 = HttpResponse(404, '{"result": "failure"}')

        response_dict = {}
        response_dict[response1] = "value1"
        response_dict[response2] = "value2"
        response_dict[response3] = "value3"

        self.assertEqual(len(response_dict), 2)  # response1 and response2 are the same key
        self.assertEqual(response_dict[response1], "value2")  # value was overwritten
        self.assertEqual(response_dict[response3], "value3")


if __name__ == "__main__":
    unittest.main()
