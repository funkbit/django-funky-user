from django.conf import settings

# URL redirects
SIGNUP_REDIRECT_URL = getattr(settings, 'SIGNUP_REDIRECT_URL', settings.LOGIN_REDIRECT_URL)

# Templates
# BASE_TEMPLATE = getattr(settings, 'XX_USER_BASE_TEMPLATE', 'base.html')
BASE_TEMPLATE_HTML_EMAIL = getattr(settings, 'BASE_TEMPLATE_HTML_EMAIL', 'auth/emails/base.html')
BASE_TEMPLATE_TEXT_EMAIL = getattr(settings, 'BASE_TEMPLATE_TEXT_EMAIL', 'auth/emails/base.txt')

# URL regular expression for activation and password reset token
PASSWORD_TOKEN = r'(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})'
