#Django imports
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView

# Project imports
from fucksia.core.views import LandingView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', LandingView.as_view(), name="home"),
    url(r'', include('fucksia.maker.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('fucksia.accounts.urls')),


    url(r'^about/$',
        TemplateView.as_view(template_name="about.html"), name="about"),
    url(r'^contact/$',
        TemplateView.as_view(template_name="contact.html"), name="contact"),
    url(r'^timeline/$',
        TemplateView.as_view(template_name='accounts/profile.html'),
        name='timeline'),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.conf.urls.static import static

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
