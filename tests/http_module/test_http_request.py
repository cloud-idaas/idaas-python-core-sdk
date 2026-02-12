"""
Tests for HttpRequest class
"""

import unittest

from cloud_idaas import Builder, ContentType, HttpRequest
from cloud_idaas.core.http.http_method import HttpMethod


class TestHttpRequest(unittest.TestCase):
    """Test cases for HttpRequest class"""

    def test_default_request(self):
        """Test creating a default request"""
        request = HttpRequest()
        self.assertIsNone(request.method)
        self.assertIsNone(request.url)
        self.assertIsNone(request.headers)
        self.assertIsNone(request.body)
        self.assertIsNone(request.form_body)
        self.assertIsNone(request.content_type)

    def test_request_with_properties(self):
        """Test request with properties set"""
        request = HttpRequest()
        request.method = HttpMethod.POST
        request.url = "https://example.com/api"
        request.body = "test body"
        request.content_type = ContentType.JSON

        self.assertEqual(request.method, HttpMethod.POST)
        self.assertEqual(request.url, "https://example.com/api")
        self.assertEqual(request.body, "test body")
        self.assertEqual(request.content_type, ContentType.JSON)

    def test_builder_pattern(self):
        """Test builder pattern for creating request"""
        request = (
            Builder()
            .http_method(HttpMethod.POST)
            .url("https://example.com/api")
            .body("test body")
            .content_type(ContentType.JSON)
            .build()
        )

        self.assertEqual(request.method, HttpMethod.POST)
        self.assertEqual(request.url, "https://example.com/api")
        self.assertEqual(request.body, "test body")
        self.assertEqual(request.content_type, ContentType.JSON)

    def test_builder_with_headers(self):
        """Test builder with headers"""
        headers = {"Authorization": ["Bearer token"], "Accept": ["application/json"]}
        request = Builder().http_method(HttpMethod.GET).url("https://example.com/api").headers(headers).build()

        self.assertEqual(request.headers, headers)

    def test_builder_with_form_body(self):
        """Test builder with form body"""
        form_body = {"username": ["test"], "password": ["secret"]}
        request = (
            Builder()
            .http_method(HttpMethod.POST)
            .url("https://example.com/api")
            .form_body(form_body)
            .content_type(ContentType.FORM)
            .build()
        )

        self.assertEqual(request.form_body, form_body)
        self.assertEqual(request.content_type, ContentType.FORM)

    def test_repr(self):
        """Test __repr__ method"""
        request = HttpRequest()
        request.method = HttpMethod.POST
        request.url = "https://example.com/api"
        request.body = "test body"
        request.content_type = ContentType.JSON
        headers = {"Authorization": ["Bearer token"], "Accept": ["application/json"]}
        request.headers = headers

        repr_str = repr(request)
        self.assertIn("HttpRequest", repr_str)
        self.assertIn("https://example.com/api", repr_str)
        self.assertIn("test body", repr_str)

    def test_repr_empty(self):
        """Test __repr__ method with empty request"""
        request = HttpRequest()
        repr_str = repr(request)
        self.assertIn("HttpRequest", repr_str)

    def test_eq_equal(self):
        """Test __eq__ method with equal requests"""
        headers = {"Authorization": ["Bearer token"]}
        request1 = HttpRequest()
        request1.method = HttpMethod.POST
        request1.url = "https://example.com/api"
        request1.body = "test body"
        request1.content_type = ContentType.JSON
        request1.headers = headers

        request2 = HttpRequest()
        request2.method = HttpMethod.POST
        request2.url = "https://example.com/api"
        request2.body = "test body"
        request2.content_type = ContentType.JSON
        request2.headers = headers

        self.assertEqual(request1, request2)

    def test_eq_not_equal_method(self):
        """Test __eq__ method with different method"""
        request1 = HttpRequest()
        request1.method = HttpMethod.POST
        request1.url = "https://example.com/api"
        request1.body = "test body"

        request2 = HttpRequest()
        request2.method = HttpMethod.GET
        request2.url = "https://example.com/api"
        request2.body = "test body"

        self.assertNotEqual(request1, request2)

    def test_eq_not_equal_url(self):
        """Test __eq__ method with different URL"""
        request1 = HttpRequest()
        request1.method = HttpMethod.POST
        request1.url = "https://example.com/api1"
        request1.body = "test body"

        request2 = HttpRequest()
        request2.method = HttpMethod.POST
        request2.url = "https://example.com/api2"
        request2.body = "test body"

        self.assertNotEqual(request1, request2)

    def test_eq_not_equal_body(self):
        """Test __eq__ method with different body"""
        request1 = HttpRequest()
        request1.method = HttpMethod.POST
        request1.url = "https://example.com/api"
        request1.body = "body1"

        request2 = HttpRequest()
        request2.method = HttpMethod.POST
        request2.url = "https://example.com/api"
        request2.body = "body2"

        self.assertNotEqual(request1, request2)

    def test_eq_not_equal_content_type(self):
        """Test __eq__ method with different content_type"""
        request1 = HttpRequest()
        request1.method = HttpMethod.POST
        request1.url = "https://example.com/api"
        request1.content_type = ContentType.JSON

        request2 = HttpRequest()
        request2.method = HttpMethod.POST
        request2.url = "https://example.com/api"
        request2.content_type = ContentType.FORM

        self.assertNotEqual(request1, request2)

    def test_eq_not_equal_headers(self):
        """Test __eq__ method with different headers"""
        request1 = HttpRequest()
        request1.method = HttpMethod.POST
        request1.url = "https://example.com/api"
        request1.headers = {"Authorization": ["Bearer token1"]}

        request2 = HttpRequest()
        request2.method = HttpMethod.POST
        request2.url = "https://example.com/api"
        request2.headers = {"Authorization": ["Bearer token2"]}

        self.assertNotEqual(request1, request2)

    def test_eq_with_none_values(self):
        """Test __eq__ method with None values"""
        request1 = HttpRequest()
        request2 = HttpRequest()
        self.assertEqual(request1, request2)

    def test_eq_different_type(self):
        """Test __eq__ method with different type"""
        request = HttpRequest()
        request.url = "https://example.com/api"

        self.assertNotEqual(request, "https://example.com/api")
        self.assertNotEqual(request, 123)
        self.assertNotEqual(request, None)

    def test_hash_equal(self):
        """Test __hash__ method with equal requests"""
        headers = {"Authorization": ["Bearer token"]}
        request1 = HttpRequest()
        request1.method = HttpMethod.POST
        request1.url = "https://example.com/api"
        request1.body = "test body"
        request1.content_type = ContentType.JSON
        request1.headers = headers

        request2 = HttpRequest()
        request2.method = HttpMethod.POST
        request2.url = "https://example.com/api"
        request2.body = "test body"
        request2.content_type = ContentType.JSON
        request2.headers = headers

        self.assertEqual(hash(request1), hash(request2))

    def test_hash_not_equal(self):
        """Test __hash__ method with different requests"""
        request1 = HttpRequest()
        request1.method = HttpMethod.POST
        request1.url = "https://example.com/api1"
        request1.body = "test body"

        request2 = HttpRequest()
        request2.method = HttpMethod.POST
        request2.url = "https://example.com/api2"
        request2.body = "test body"

        self.assertNotEqual(hash(request1), hash(request2))

    def test_hash_consistent(self):
        """Test __hash__ method returns consistent hash"""
        request = HttpRequest()
        request.method = HttpMethod.POST
        request.url = "https://example.com/api"
        request.body = "test body"

        hash1 = hash(request)
        hash2 = hash(request)
        self.assertEqual(hash1, hash2)

    def test_hash_with_none_values(self):
        """Test __hash__ method with None values"""
        request1 = HttpRequest()
        request2 = HttpRequest()
        self.assertEqual(hash(request1), hash(request2))

    def test_can_use_in_set(self):
        """Test that HttpRequest can be used in a set"""
        headers = {"Authorization": ["Bearer token"]}
        request1 = HttpRequest()
        request1.method = HttpMethod.POST
        request1.url = "https://example.com/api"
        request1.body = "test body"
        request1.headers = headers

        request2 = HttpRequest()
        request2.method = HttpMethod.POST
        request2.url = "https://example.com/api"
        request2.body = "test body"
        request2.headers = headers

        request3 = HttpRequest()
        request3.method = HttpMethod.POST
        request3.url = "https://example.com/api2"
        request3.body = "test body"

        request_set = {request1, request2, request3}
        self.assertEqual(len(request_set), 2)  # request1 and request2 are equal

    def test_builder_repr(self):
        """Test __repr__ method for Builder"""
        builder = Builder()
        repr_str = repr(builder)
        self.assertIn("Builder", repr_str)

    def test_builder_eq_equal(self):
        """Test __eq__ method for Builder with equal builders"""
        builder1 = Builder()
        builder1.http_method(HttpMethod.POST)
        builder1.url("https://example.com/api")
        builder1.body("test body")

        builder2 = Builder()
        builder2.http_method(HttpMethod.POST)
        builder2.url("https://example.com/api")
        builder2.body("test body")

        self.assertEqual(builder1, builder2)

    def test_builder_eq_not_equal(self):
        """Test __eq__ method for Builder with different builders"""
        builder1 = Builder()
        builder1.http_method(HttpMethod.POST)
        builder1.url("https://example.com/api1")

        builder2 = Builder()
        builder2.http_method(HttpMethod.POST)
        builder2.url("https://example.com/api2")

        self.assertNotEqual(builder1, builder2)

    def test_builder_eq_different_type(self):
        """Test __eq__ method for Builder with different type"""
        builder = Builder()
        builder.url("https://example.com/api")

        self.assertNotEqual(builder, "https://example.com/api")
        self.assertNotEqual(builder, 123)
        self.assertNotEqual(builder, None)

    def test_builder_hash_equal(self):
        """Test __hash__ method for Builder with equal builders"""
        builder1 = Builder()
        builder1.http_method(HttpMethod.POST)
        builder1.url("https://example.com/api")
        builder1.body("test body")

        builder2 = Builder()
        builder2.http_method(HttpMethod.POST)
        builder2.url("https://example.com/api")
        builder2.body("test body")

        self.assertEqual(hash(builder1), hash(builder2))

    def test_builder_hash_not_equal(self):
        """Test __hash__ method for Builder with different builders"""
        builder1 = Builder()
        builder1.http_method(HttpMethod.POST)
        builder1.url("https://example.com/api1")

        builder2 = Builder()
        builder2.http_method(HttpMethod.POST)
        builder2.url("https://example.com/api2")

        self.assertNotEqual(hash(builder1), hash(builder2))

    def test_builder_can_use_in_set(self):
        """Test that Builder can be used in a set"""
        builder1 = Builder()
        builder1.http_method(HttpMethod.POST)
        builder1.url("https://example.com/api")
        builder1.body("test body")

        builder2 = Builder()
        builder2.http_method(HttpMethod.POST)
        builder2.url("https://example.com/api")
        builder2.body("test body")

        builder3 = Builder()
        builder3.http_method(HttpMethod.POST)
        builder3.url("https://example.com/api2")

        builder_set = {builder1, builder2, builder3}
        self.assertEqual(len(builder_set), 2)  # builder1 and builder2 are equal


if __name__ == "__main__":
    unittest.main()
