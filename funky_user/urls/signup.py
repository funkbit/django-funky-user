from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _

from funky_user.conf import PASSWORD_TOKEN


# Signup views
urlpatterns = patterns('funky_user.views',

    url(_(r'^signup/$'), 'signup', name='user-signup'),
    url(_(r'^signup/done/$'), 'signup_done', name='user-signup-done'),
    url(_(r'^signup/%s/$') % PASSWORD_TOKEN, 'activate', name='user-activate'),

)
