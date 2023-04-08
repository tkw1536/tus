from django.http.response import Http404, HttpResponse
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
            return short.get(self.request)
        except ShortURL.DoesNotExist:
            pass

        # try a static page (less common)
        try:
            static = StaticPage.objects.get(slug=slug)
            return static.get(self.request)
        except StaticPage.DoesNotExist:
            pass

        raise Http404

def handler400(request, *args, **argv):
    return HttpResponse('Bad Request', content_type='text/plain', status=403)
def handler403(request, *args, **argv):
    return HttpResponse('Permission Denied', content_type='text/plain', status=403)
def handler404(request, *args, **argv):
    return HttpResponse('Not Found', content_type='text/plain', status=404)
def handler500(request, *args, **argv):
    return HttpResponse('Internal Server Error', content_type='text/plain', status=500)
