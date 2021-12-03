from django.db import models
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.db.models import F
from django.utils.translation import pgettext_lazy


class TUSModel(models.Model):
    class Meta:
        abstract = True

    slug = models.SlugField(unique=True, blank=True, help_text=pgettext_lazy(
        'help text for TUSModel.slug', 'Slug to forward from'),
    )

    @property
    def source(self):
        if not self.slug:
            return '/'
        return '/{}/'.format(self.slug)

    def get_absolute_url(self):
        return self.source

    def __str__(self):
        return '{}[{}]'.format(self.__class__.__name__, self.source)

    stats_enabled = models.BooleanField(default=True, help_text=pgettext_lazy(
        'help text for TUSModel.stats_enabled', 'Enable statistics',
    ))
    hits = models.PositiveIntegerField(default=0, help_text=pgettext_lazy(
        'help text for TUSModel.hits', 'Number of hits',
    ))

    def _record_stats(self, request):
        urls = self.__class__.objects.filter(
            slug=self.slug, stats_enabled=True)
        urls.update(hits=F('hits') + 1)


class ShortURL(TUSModel):
    """ A ShortURL that can be forwarded to """
    target = models.URLField(max_length=1000, help_text=pgettext_lazy(
        'help text for ShortURL.target', 'URL to forward to'))
    permanent = models.BooleanField(default=False, help_text=pgettext_lazy(
        'help text for ShortURL.permanent', 'Should the redirect be permanent'
    ))

    def __call__(self, request):
        """ Redirects request to this url """

        self._record_stats(request)

        # do the redirect!
        return redirect(self.target, permanent=self.permanent)


class StaticPage(TUSModel):
    """ A static page, if no ShortURL is found """

    content = models.TextField(help_text=pgettext_lazy(
        'help text for StaticPage.content', 'Content of static page'))
    content_type = models.TextField(default='text/plain', help_text=pgettext_lazy(
        'help text for StaticPage.content_type', 'Content Type of static page'))

    def __call__(self, request):
        """ Responds with the static page """

        self._record_stats(request)

        res = HttpResponse(self.content, content_type=self.content_type)
        res['Content-Length'] = len(self.content)

        return res
