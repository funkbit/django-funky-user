from funky_user.urls.auth import urlpatterns as auth_urlpatterns
from funky_user.urls.signup import urlpatterns as signup_urlpatterns


# Import this if you want both auth and signup urls
urlpatterns = auth_urlpatterns + signup_urlpatterns
