from django.contrib.auth import get_user_model
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

# User model defined in settings
User = get_user_model()

class AnonymousUserTestCase(TestCase):
    """
    Test as anonymous user.
    """

    def setUp(self):

        # Add a user to the database
        self.user = User.objects.create(
            email='foo@example.com',
            password='foobar',
            is_active=True,
        )

    def testSignupValid(self):

        # Check that the user is logged in
        response = self.client.get(reverse('user-signup'))
        self.assertEquals(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated())

        # Sign up
        response = self.client.post(reverse('user-signup'), {
            'email': 'test@example.com',
            'password': '12345',
            'name': 'Mr. Foo Bar',
            'short_bio': 'About me',
        })
        self.assertRedirects(response, reverse('user-signup-done'))

        # Check that the user object is created correctly
        self.assertEquals(User.objects.count(), 2)
        user = User.objects.get(id=2)
        self.assertEquals(user.email, 'test@example.com')
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user in User.objects.active())

        # TODO Check outgoing email

        # Log in inactive user, should fail
        response = self.client.post(reverse('user-login'), {
            'username': 'test@example.com',
            'password': '12345',
        })
        self.assertEquals(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated())

        # Activate account with link from email
        """
        response = self.client.post(reverse('user-login'), {
            'username': 'test@example.com',
            'password': '12345',
        })
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL)

        # Check that user gets logged in
        response = self.client.get(reverse('user-login'))
        self.assertTrue(response.context['user'].is_authenticated())
        """

        # Check that the user is now activated

    def testSignupDone(self):

        # Sign up done screen
        response = self.client.get(reverse('user-signup-done'))
        self.assertEquals(response.status_code, 200)

    def testSignupEmailAlreadyInUse(self):

        # Sign up with an email address already registered
        response = self.client.post(reverse('user-signup'), {
            'email': 'foo@example.com',
            'password': '12345',
            'name': 'Registered again',
            'short_bio': 'About me',
        })
        self.assertEquals(response.status_code, 200)
        self.assertTrue('That email is already registered.' in str(response.context['form'].errors))
        self.assertEquals(User.objects.count(), 1)

    def testPasswordReset(self):

        self.assertEqual(len(mail.outbox), 0)

        # Request new password
        response = self.client.get(reverse('user-password-reset'))
        self.assertEquals(response.status_code, 200)

        response = self.client.post(reverse('user-password-reset'), {
            'email': 'foo@example.com',
        })
        self.assertRedirects(response, reverse('user-password-reset-done'))

        # Check that email is sent
        self.assertEqual(len(mail.outbox), 1)


        #'user-password-reset-confirm'
        #'user-password-reset-complete'


class AuthenticatedUserTestCase(TestCase):
    """
    Test as logged in user.
    """

    def setUp(self):

        # Create active user to test with
        user = User(email='test@example.com', is_active=True)
        user.set_password('1234')
        user.save()

        # Sign in user
        self.client.login(username=user.email, password='1234')

    def testPasswordChange(self):

        response = self.client.get(reverse('user-password-change'))
        self.assertEquals(response.status_code, 200)

        response = self.client.post(reverse('user-password-change'), {
            'old_password': '1234',
            'new_password1': '54321',
            'new_password2': '54321',
        })
        self.assertRedirects(response, reverse('user-password-change-done'))

    def testAccountLogout(self):

        # Check that the user is logged in
        response = self.client.get(reverse('user-login'))
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated())

        # Sign-out
        response = self.client.get(reverse('user-logout'))
        self.assertEquals(response.status_code, 200)

        # Check that the user is logged out
        response = self.client.get(reverse('user-login'))
        self.assertEquals(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated())
