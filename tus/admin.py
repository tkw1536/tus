import csv

from django.contrib import admin
from django.forms import ModelForm, Select
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from .models import ShortURL, StaticPage


class TUSAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        self.request = request
        return qs

    def source(self, instance):
        return instance.source
    source.short_description = 'Source'
    source.admin_order_field = 'slug'

    def public_url(self, obj):
        url = self.request.build_absolute_uri(obj.get_absolute_url())
        return mark_safe(u"<a href='{}'>{}</a>".format(url, url))
    public_url.allow_tags = True
    public_url.short_description = u"Public URL"


def make_csv_exporter(*field_names):
    def export_as_csv(self, request, queryset):

        meta = self.model._meta

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
            meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field)
                                  for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"
    return export_as_csv


@admin.register(ShortURL)
class ShortURLAdmin(TUSAdmin):
    list_display = ('source', 'public_url', 'target',
                    'permanent', 'stats_enabled', 'hits',)
    list_filter = ('permanent', 'stats_enabled',)
    search_fields = ('slug', 'target',)

    fieldsets = (
        ('URL', {'fields': ('slug',)}),
        ('Target', {'fields': ('target', 'permanent')}),
        ('Stats', {'fields': ('stats_enabled', 'hits')}),
    )
    readonly_fields = ('hits',)

    export_as_csv = make_csv_exporter(
        'slug', 'target', 'permanent', 'stats_enabled', 'hits')
    actions = ('export_as_csv',)


CONTENT_TYPES = ('text/plain', 'text/html', 'application/json')


class StaticPageForm(ModelForm):
    class Meta:
        model = StaticPage
        widgets = {
            'content_type': Select(choices=[(tp, tp) for tp in CONTENT_TYPES]),
        }
        fields = '__all__'


@admin.register(StaticPage)
class StaticPageAdmin(TUSAdmin):
    form = StaticPageForm

    list_display = ('source', 'public_url',
                    'content_type', 'stats_enabled', 'hits',)
    list_filter = ('content_type', 'stats_enabled',)
    search_fields = ('content_type', 'content', 'slug',)
    actions = ('export_as_csv',)

    fieldsets = (
        ('URL', {'fields': ('slug',)}),
        ('Content', {'fields': ('content', 'content_type')}),
        ('Stats', {'fields': ('stats_enabled', 'hits')}),
    )
    readonly_fields = ('hits',)
