from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _

from funky_user.conf import PASSWORD_TOKEN
from funky_user.forms import PasswordResetForm


# Built-in Django views
urlpatterns = patterns('django.contrib.auth.views',

    url(_(r'^login/$'), 'login',
        {'template_name': 'auth/login.html'}, name='user-login'),
    url(_(r'^logout/$'), 'logout',
        {'template_name': 'auth/logged_out.html'}, name='user-logout'),

    url(_(r'^password-change/$'), 'password_change',
        {'template_name': 'auth/password_change_form.html'}, name='user-password-change'),
    url(_(r'^password-change/done/$'), 'password_change_done',
        {'template_name': 'auth/password_change_done.html'}, name='user-password-change-done'),

    url(_(r'^password-reset/$'), 'password_reset',
        {'template_name': 'auth/password_reset_form.html',
        'password_reset_form': PasswordResetForm}, name='user-password-reset'),
    url(_(r'^password-reset/done/$'), 'password_reset_done',
        {'template_name': 'auth/password_reset_done.html'}, name='user-password-reset-done'),

    url(_(r'^reset/%s/$') % PASSWORD_TOKEN, 'password_reset_confirm',
        {'template_name': 'auth/password_reset_confirm.html'}, name='user-password-reset-confirm'),
    url(_(r'^reset/done/$'), 'password_reset_complete',
        {'template_name': 'auth/password_reset_complete.html'}, name='user-password-reset-complete'),

)
