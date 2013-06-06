from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


class UserChangeForm(forms.ModelForm):
    """
    Edit profile example form for registered users.
    """

    first_name = forms.CharField(label=_('First name'), max_length=75)
    last_name = forms.CharField(label=_('Last name'), max_length=75)

    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'email',
            'description',
        )

    def clean_first_name(self):

        val = self.cleaned_data['first_name'].strip()
        if not len(val) > 0:
            raise forms.ValidationError(_('Text cannot be empty.'))

        return val

    def clean_last_name(self):

        val = self.cleaned_data['last_name'].strip()
        if not len(val) > 0:
            raise forms.ValidationError(_('Text cannot be empty.'))

        return val
