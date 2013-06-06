from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _
from funky_user.urls import urlpatterns

# Extend the default urlpatterns provided by funky_user
urlpatterns += patterns('testapp.views',

    url(_(r'^edit/$'), 'edit', name='user-edit'),

)
