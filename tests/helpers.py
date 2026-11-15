from tus.models import ShortURL, StaticPage


def make_short_url(**overrides):
    """Create a ShortURL with sensible defaults for tests."""
    defaults = {
        "slug": "go",
        "target": "https://example.com/",
        "permanent": False,
        "stats_enabled": True,
        "hits": 0,
    }
    defaults.update(overrides)
    return ShortURL.objects.create(**defaults)


def make_static_page(**overrides):
    """Create a StaticPage with sensible defaults for tests."""
    defaults = {
        "slug": "about",
        "content": "hello",
        "content_type": "text/plain",
        "stats_enabled": True,
        "hits": 0,
    }
    defaults.update(overrides)
    return StaticPage.objects.create(**defaults)
