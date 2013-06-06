from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField,
    PasswordResetForm as DjangoPasswordResetForm)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.utils.http import int_to_base36
from django.utils.translation import ugettext_lazy as _

from funky_user import conf

User = get_user_model()


class UserChangeForm(forms.ModelForm):
    """
    User change form for the Django Admin. Overrides the password field to
    explain it's content.
    """

    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = User


class SignupForm(forms.ModelForm):
    """
    Signup form for new users.

    It displays email and password fields by default, and adds the fields
    defined in `REQUIRED_FIELDS` in the current user model.
    """

    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
        ] + User.REQUIRED_FIELDS

    def clean_email(self):
        """
        Validate that the email is not already in use.
        """

        try:
            User.objects.get(email__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']

        raise forms.ValidationError(_('That email is already registered.'))

class PasswordResetForm(DjangoPasswordResetForm):
    """
    Overrides the save method on Django's PasswordResetForm to enable HTML email.
    """

    def save(self, domain_override=None,
             email_template_prefix='auth/emails/password_reset',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, **kwargs):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """

        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.pk),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
                'BASE_TEMPLATE_HTML_EMAIL': conf.BASE_TEMPLATE_HTML_EMAIL,
                'BASE_TEMPLATE_TEXT_EMAIL': conf.BASE_TEMPLATE_TEXT_EMAIL,
            }

            # Send HTML mail with Django Groove
            #from groove.email.html import send_html_email
            #send_html_email(user.email, email_template_prefix, c, from_email)
