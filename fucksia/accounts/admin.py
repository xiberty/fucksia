from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.utils.translation import ugettext, ugettext_lazy as _

from fucksia.accounts.forms import UserCreationForm, UserChangeForm
from fucksia.accounts.models import User

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = (
        'username',
        'get_email_formatted_address',
        'last_active',
        'is_active',
        'is_staff',
        'is_superuser'
    )

    list_filter = ('is_superuser', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),

        (
            _('Personal info'), {
                'fields': ('first_name', 'last_name', 'photo')
            }
        ),
        (
            _('Permissions'), {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                           'user_permissions')
            }
        ),
        (
            _('Important dates'), {
                'fields': ('last_active', 'active_since')
            }
        ),
    )


    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2'
            )}
        ),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-active_since',)
    date_hierarchy = 'active_since'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super(UserAdmin, self).get_inline_instances(request, obj)


admin.site.register(User, UserAdmin)
