# Django imports
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Third part imports
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()


urlpatterns = patterns('fucksia.maker.views',
    url(r'^config/$', 'config', name='config'),
    url(r'^cuenta/$', 'perfil', name='perfil'),
    url(r'^$', 'login', name='login'),
    url(r'^home/$', 'home', name='home'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^generador/$', 'generador', name='generador'),
    url(r'^horario/$', 'horario', name='horario'),
    url(r'^admin/pensum/$', 'config_pensum', name='config_pensum'),

    url(r'^home/guardar-comentario/$', 'guardar_comentario', name='guardar_comentario'),
    url(r'^home/cargar-respuestas/(?P<id>\d+)$', 'cargar_respuestas', name='cargar_respuestas'),
    url(r'^guardar-respuesta/$', 'guardar_respuesta', name='guardar_respuesta'),
)

# urlpatterns += patterns('',
#     url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
# )
