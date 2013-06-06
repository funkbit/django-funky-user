from django.contrib.auth.models import AbstractBaseUser as DjangoAbstractBaseUser
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.http import int_to_base36
from django.utils.translation import ugettext_lazy as _

from funky_user import conf
from funky_user.managers import UserManager


class AbstractBaseUser(DjangoAbstractBaseUser):
    """
    Abstract custom user model that utilizes email instead of username.

    Inherits the fields: password, last_login and is_active.
    """

    email = models.EmailField(_('email address'), max_length=254, unique=True, db_index=True)

    # Permissions
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=False,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))

    # Timestamps
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name = _('users')
        abstract = True

    def __unicode__(self):

        return self.get_full_name()

    def get_full_name(self):

        return self.get_username()

    def get_short_name(self):

        return self.get_full_name()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def send_activation_email(self, use_https=False):
        """
        Send an activation email for new users, to verify their email address.
        Creates an activation key with Django's reset password token generator.
        """

        # Create activation token URL
        uidb36 = int_to_base36(self.id)
        token = default_token_generator.make_token(self)
        url = reverse('user-activate', kwargs={
            'uidb36': uidb36,
            'token': token,
        })

        # Send email
        """from groove.email.html import send_html_email
        mail_sent = send_html_email(self.email, 'auth/emails/activation', {
            'activation_url': url,
            'protocol': use_https and 'https' or 'http',
            'BASE_TEMPLATE_HTML_EMAIL': conf.BASE_TEMPLATE_HTML_EMAIL,
            'BASE_TEMPLATE_TEXT_EMAIL': conf.BASE_TEMPLATE_TEXT_EMAIL,
        })

        return mail_sent
        """
        return False

class User(AbstractBaseUser):
    """
    Concrete version of AbstractBaseUser.

    Use this directly in your project if you don't need additional fields or
    functionality.
    """

    pass

############
# Examples #
############

class NameAbstractBaseUser(AbstractBaseUser):

    name = models.CharField(_('name'), max_length=75)

    REQUIRED_FIELDS = ['name', ]

    class Meta:
        abstract = True

    def get_full_name(self):
        "Returns the full name for the user."
        return self.name

    def get_short_name(self):
        "Returns the short name for the user."
        return self.get_full_name()


class FirstLastNameAbstractBaseUser(AbstractBaseUser):

    first_name = models.CharField(_('first name'), max_length=75)
    last_name = models.CharField(_('last name'), max_length=75)

    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        abstract = True

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """

        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name
