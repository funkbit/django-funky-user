from django.conf import settings
from django.contrib.auth import login as auth_login, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, render
from django.utils.http import base36_to_int
from django.views.decorators.debug import sensitive_post_parameters

from funky_user import conf
from funky_user.forms import SignupForm


@sensitive_post_parameters('password')
def signup(request, template_name='auth/signup.html', extra_context=None):
    """
    Signup form for new users.
    """

    UserModel = get_user_model()

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():

            # Create the the new user
            new_user = UserModel.objects.create_user(**form.cleaned_data)

            # Send activation email
            new_user.send_activation_email()

            return redirect('user-signup-done')

    else:
        form = SignupForm()

    # Template context
    context = {
        'form': form
    }

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template_name, context)


def signup_done(request, template_name='auth/signup_done.html', extra_context=None):
    """
    Screen shown to user after successfully signing up.
    """

    return render(request, template_name, extra_context)


def activate(request, uidb36, token,
             template_name='auth/signup_activation_failed.html',
             extra_context=None):
    """
    Check activation token for newly registered users. If successful,
    mark as active and log them in. If not, show an error page.

    Code borrowed from Django's auth reset mechanism.
    """

    UserModel = get_user_model()

    # Look up the user object
    try:
        uid_int = base36_to_int(uidb36)
        user = UserModel.objects.get(id=uid_int)
    except (ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None:

        # Is the token valid?
        if default_token_generator.check_token(user, token):

            # Activate the user
            user.is_active = True
            user.save()

            # Log in the user
            user.backend = settings.AUTHENTICATION_BACKENDS[0]
            auth_login(request, user)

            # Redirect to URL specified in settings
            return redirect(conf.SIGNUP_REDIRECT_URL)

    return render(request, template_name, extra_context)
