# Python Imports
import re
from hashlib import sha1
from email.utils import formataddr

# Django Imports
from django.conf import settings
from django.core import validators
from django.core.files.storage import FileSystemStorage
from django.db import models

from django.utils.http import urlquote
from django.utils.timezone import now, pytz
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin)

# Local Imports
from fucksia.core.utils import send_mail


class OverwriteStorage(FileSystemStorage):
    def save(self, name, content):
        if self.exists(name):
            self.delete(name)
        return super(OverwriteStorage, self).save(name, content)

    def get_available_name(self, name):
        return name


def upload_to_photo(instance, filename):
    extension = filename.split('.')[-1].lower()
    hash = sha1('%s%s' % (settings.SECRET_KEY, instance.id)).hexdigest()
    return 'accounts/%(hash)s.%(extension)s' % {
        'hash': hash[:20],
        'extension': extension
    }


class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = UserManager.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        u = self.create_user(username, email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser, PermissionsMixin):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True
    )
    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(
                re.compile('^[a-zA-Z-_.]+$'),
                _('Enter a valid username.'), 'invalid')
        ]
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    last_active = models.DateTimeField(
        blank=True,
        null=True,
        help_text='The last date that the user was active.'
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        auto_now_add=True
    )
    active_since = models.DateTimeField(
        blank=True,
        null=True
    )
    photo = models.ImageField(
        blank=True,
        storage=OverwriteStorage(),
        upload_to=upload_to_photo
    )

    GENDER_CHOICES = [(MALE, _('Male')), (FEMALE, _('Female')), (OTHER, _('Other'))]

    gender = models.CharField(_('gender'), max_length=1, choices=GENDER_CHOICES,default=MALE)
    TIMEZONE_CHOICES = [('', "Use system's default TZ")]
    TIMEZONE_CHOICES += map(lambda t: (t, t), pytz.common_timezones)

    # TODO: The adhoc ``TimeZoneField`` I put together wasn't working, so for
    # now ``timezone`` will be a ``CharField``.  [a:FSD]
    timezone = models.CharField(
        _("timezone"),
        blank=True,
        max_length=128,
        null=True,
        choices=TIMEZONE_CHOICES,
        help_text=_("Timezone in which you reside or work. This will be"
                    " used to represent all dates in this site in your selected timezone.")
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'

    def __unicode__(self):
        return self.get_full_name()

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        if self.first_name and self.last_name:
            name = '%s %s' % (self.first_name, self.last_name)
        else:
            name = self.username
        return unicode(name.strip())

    def get_photo_url(self):
        """Get the URL for the user's profile photo.

        :rtype: str
        """
        # TODO: Implement support for gravatar URLs, and also caching the
        # gravatar image, for user profile photos.

        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return "%s%s" % (settings.STATIC_URL, "img/anonymous.png")

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, text_message, html_message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, text_message, html_message, from_email, [self.email])

    def get_email_formatted_address(self):
        return u"%s" % formataddr((self.get_full_name(), self.email))

    get_email_formatted_address.short_description = 'Contact Address'

    def get_timezone(self):
        return self.timezone or settings.TIME_ZONE


class UserSignup(models.Model):
    user = models.OneToOneField(User,
                                related_name='userena_signup')
    activation_key = models.CharField(max_length=40, blank=True)
    activation_notification_send = models.BooleanField(default=False)
    email_unconfirmed = models.EmailField(blank=True)
    email_confirmation_key = models.CharField(max_length=40, blank=True)


    def change_email(self, email):
        """
        Changes the email address for a user.

        A user needs to verify this new email address before it becomes
        active. By storing the new email address in a temporary field --
        ``temporary_email`` -- we are able to set this email address after the
        user has verified it by clicking on the verification URI in the email.
        This email gets send out by ``send_verification_email``.

        :param email:
            The new email address that the user wants to use.

        """
        confirmation_hash = sha1(str(self.user.username)).hexdigest()
        self.email_unconfirmed = email
        self.email_confirmation_key = confirmation_hash[:40]
        self.email_confirmation_key_created = now()
        self.save()

        # Send email for activation
        self.send_confirmation_email()

    def send_confirmation_email(self):
        raise NotImplementedError()

    def send_activation_email(self):
        raise NotImplementedError()
