from django.test import TestCase

from .helpers import make_short_url, make_static_page


class ShortURLRedirectTests(TestCase):
    def test_temporary_short_url_redirects_to_target(self):
        make_short_url(slug="go", target="https://example.com/", permanent=False)

        response = self.client.get("/go/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "https://example.com/")

    def test_permanent_short_url_redirects_with_301(self):
        make_short_url(slug="go", target="https://example.com/", permanent=True)

        response = self.client.get("/go/")

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "https://example.com/")

    def test_root_short_url_serves_at_slash(self):
        make_short_url(slug="", target="https://example.com/home/", permanent=False)

        response = self.client.get("/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "https://example.com/home/")

    def test_short_url_takes_precedence_over_static_page_with_same_slug(self):
        make_short_url(slug="shared", target="https://example.com/from-short/")
        make_static_page(slug="shared", content="from static")

        response = self.client.get("/shared/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "https://example.com/from-short/")


class ShortURLStatsTests(TestCase):
    def test_hit_is_recorded_when_stats_are_enabled(self):
        url = make_short_url(slug="go", stats_enabled=True, hits=0)

        self.client.get("/go/")
        url.refresh_from_db()

        self.assertEqual(url.hits, 1)

    def test_hit_is_not_recorded_when_stats_are_disabled(self):
        url = make_short_url(slug="go", stats_enabled=False, hits=0)

        self.client.get("/go/")
        url.refresh_from_db()

        self.assertEqual(url.hits, 0)


class MissingSlugTests(TestCase):
    def test_unknown_slug_returns_404(self):
        response = self.client.get("/does-not-exist/")

        self.assertEqual(response.status_code, 404)
