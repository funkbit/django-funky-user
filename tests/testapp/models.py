from django.db import models
from django.utils.translation import ugettext_lazy as _
from funky_user.models import NameAbstractBaseUser


class User(NameAbstractBaseUser):
    """
    Extends the abstract base user class from funky_user, adds additional fields.
    """

    short_bio = models.TextField(_('short bio'))
    description = models.TextField(_('description'), blank=True)
    twitter_url = models.URLField(_('twitter url'), blank=True)

    # Required fields, shown on signup screen
    REQUIRED_FIELDS = NameAbstractBaseUser.REQUIRED_FIELDS + ['short_bio', ]
