from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from fucksia.accounts.views import CreateAccount
from fucksia.accounts.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm
)

urlpatterns = patterns(
    '',

    url(r'^new/$',
        CreateAccount.as_view(),
        name='new_account'),

    url(r'^settings/$',
        TemplateView.as_view(template_name='accounts/profile.html'),
        name='settings'),

    url(r'^profile/$',
        TemplateView.as_view(template_name='accounts/profile.html'),
        name='profile'),

    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'authentication_form': AuthenticationForm},
        name='login'),

    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        name='logout'),

    url(r'^password_change/$',
        'django.contrib.auth.views.password_change',
        {'password_change_form': PasswordChangeForm},
        name='password_change'),

    url(r'^password_change/done/$',
        'django.contrib.auth.views.password_change_done',
        name='password_change_done'),

    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset',
        {'password_reset_form': PasswordResetForm},
        name='password_reset'),

    url(r'^password_reset/done/$',
        'django.contrib.auth.views.password_reset_done',
        name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'set_password_form': SetPasswordForm},
        name='password_reset_confirm'),

    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete',
        name='password_reset_complete'),
)
