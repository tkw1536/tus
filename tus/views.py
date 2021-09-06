from django.http.response import Http404
from django.views import View
from .models import ShortURL, StaticPage


class StaticOrShort(View):
    def get(self, *args, **kwargs):
        slug = ''
        if 'slug' in kwargs:
            slug = kwargs['slug']

        # try a redirect (more common)
        try:
            short = ShortURL.objects.get(slug=slug)
            return short(self.request)
        except ShortURL.DoesNotExist:
            pass

        # try a static page (less common)
        try:
            static = StaticPage.objects.get(slug=slug)
            return static(self.request)
        except StaticPage.DoesNotExist:
            pass

        raise Http404
