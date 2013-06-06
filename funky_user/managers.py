from datetime import datetime

from django.contrib.auth.models import BaseUserManager as DjangoBaseUserManager
from django.utils import timezone


class UserManager(DjangoBaseUserManager):
    """
    Default manager for the User model.
    """

    ###################################
    # Required Django manager methods #
    ###################################

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """

        # We set last login in the past so we know which users has logged in once
        last_login_date = datetime(1970, 1, 1).replace(tzinfo=timezone.utc)

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=False,
            is_active=False,
            last_login=last_login_date,
            date_joined=timezone.now(),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user

    ##################
    # Custom methods #
    ##################

    def active(self):
        """
        Returns only active users.
        """

        return self.filter(is_active=True)
