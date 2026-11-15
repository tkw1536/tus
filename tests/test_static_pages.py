from django.core.exceptions import ValidationError
from django.test import TestCase

from tus.models import StaticPage

from .helpers import make_static_page


class StaticPageResponseTests(TestCase):
    def test_static_page_returns_content_and_content_type(self):
        make_static_page(
            slug="about",
            content="hello world",
            content_type="text/plain",
        )

        response = self.client.get("/about/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"hello world")
        self.assertEqual(response["Content-Type"], "text/plain")

    def test_hit_is_recorded_when_stats_are_enabled(self):
        page = make_static_page(slug="about", stats_enabled=True, hits=0)

        self.client.get("/about/")
        page.refresh_from_db()

        self.assertEqual(page.hits, 1)

    def test_hit_is_not_recorded_when_stats_are_disabled(self):
        page = make_static_page(slug="about", stats_enabled=False, hits=0)

        self.client.get("/about/")
        page.refresh_from_db()

        self.assertEqual(page.hits, 0)


class StaticPageValidationTests(TestCase):
    def test_json_content_type_accepts_valid_json(self):
        page = StaticPage(
            slug="api",
            content='{"ok": true}',
            content_type="application/json",
        )

        page.clean()

    def test_json_content_type_rejects_invalid_json(self):
        page = StaticPage(
            slug="api",
            content="not-json",
            content_type="application/json",
        )

        with self.assertRaises(ValidationError):
            page.clean()
