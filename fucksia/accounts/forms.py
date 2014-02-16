
from django import forms
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm as PasswordChangeFormBase
from django.contrib.auth.forms import PasswordResetForm as PasswordResetFormBase
from django.contrib.auth.forms import SetPasswordForm as SetPasswordFormBase
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Field, Hidden, Submit

from fucksia.accounts.utils import PrependedIconText
from fucksia.accounts.models import User

SUBMIT_FORM_CLASSES = 'btn btn-lg btn-primary btn-block'


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput)

    class Meta:
        model = User

    def clean_email(self):
        # TODO: Do not allowed existing emails
        return self.cleaned_data.get("email")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.set_password(self.cleaned_data["password1"])
        #TODO: Delete this Line after UserSignup are implemented
        user.is_active = True

        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text=(
            "Raw passwords are not stored, so there is no way to see "
            "this user's password, but you can change the password "
            "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = User

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class CreateAccountForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CreateAccountForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = ''
        self.helper.form_class = 'user-form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username', placeholder=_('Username'),),
            Field('first_name', placeholder=_('first name'),),
            Field('last_name', label=_('last name'), placeholder=_('last name'),),
            Field('email', placeholder=_('Email'),),
            Field('gender', _('Gender')),
            Field('password1', placeholder=_('Password'),),
            Field('password2', placeholder=_('Password confirmation'),),
            Submit('submit', 'Create Account', css_class=SUBMIT_FORM_CLASSES),
        )
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email',
                  'gender','password1','password2',)



class AuthenticationForm(BaseAuthenticationForm):
    """
    Form for authenticating users.
    """
    remember_me = forms.BooleanField(initial=False, required=False)

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('login')
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            PrependedIconText('username', placeholder="Username", icon_class="fa fa-user"),
            PrependedIconText('password', placeholder="Password", icon_class="fa fa-lock", css_class="login-pass"),
            Field('remember_me'),
            Hidden('next', value='{{next}}'),
            Submit('submit', 'Login ',
                   css_class=SUBMIT_FORM_CLASSES),
        )


class PasswordChangeForm(PasswordChangeFormBase):
    """
    A form that lets a user change his/her password by entering
    their old password.
    """

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('password_change')
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('old_password', autofocus=True),
            Field('new_password1'),
            Field('new_password2'),
            Submit('submit', _('Change my password'),
                   css_class=SUBMIT_FORM_CLASSES),
        )


class PasswordResetForm(PasswordResetFormBase):
    """
    Form to request reset your password
    """

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('password_reset')
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('email', placeholder="Email address", autofocus=True),
            Submit('submit', _('Reset my password'),
                   css_class=SUBMIT_FORM_CLASSES),
        )


class SetPasswordForm(SetPasswordFormBase):
    """
    A form that lets a user change set his/her password without entering the
    old password
    """

    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('password_reset_confirm')
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('new_password1', autofocus=True, template=""),
            Field('new_password2'),
            Submit('submit', _('Change my password'),
                   css_class=SUBMIT_FORM_CLASSES),
        )
