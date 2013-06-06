# Django Funky User

**Django 1.5 user model enhancements**

*This is a work in progress, some functionality is not finalized.*


Django Funky User is a Django application with various functionality
to replace the built-in Django User model. It is compatible with Django 1.5 and
above.

The intention of the project is to be able to easily use (long) email addresses
as usernames, have the reset password view send HTML email and fix other minor
annoyances with Django's otherwise brilliant auth built-in package.

It also includes a sensible user registration/activation process and is very
well suited to bootstrap new projects with basic registered user functionality.

Before digging in too deep, you should be familiar with custom user models in Django:
https://docs.djangoproject.com/en/1.5/topics/auth/customizing/#substituting-a-custom-user-model


## Features

* An extendable User model that utilizes email as username, and allows long email addresses
* URL configuration (and optionally templates) for Django's built-in auth views
* User registration and email verification functionality
* Password reset email with HTML alternative

You are free to extend the provided User model with your own fields, and you
can freely choose what included functionality you want to use in your project.

### Built-in Django views configuration

If you use the provided URL configuration, it sets up the following built-in Django
views with sensible default templates.

* Login and logout
* Password change
* Password reset

### User registration

User registration functionality and templates is also included and works as
follows:

* User signs up for an account
* User receives an activation email
* User clicks activation link in mail, account is activated/email is verified
and user is automatically logged in


## Installation

Install `django-funky-user` (available on PyPi):

    pip install django-funky-user

Add it to `INSTALLED_APPS` in your `settings.py` (so Django can locate
templates):

    INSTALLED_APPS += ['funky_user']


### Vanilla setup

If you don't need any additional fields on the user model, and want to use all
included functionality, set your project up like this:

Add to your root URL configuration (`urls.py`):

    urlpatterns = patterns('',
        ...
        url(r'^account/', include('funky_user.urls')),
    )

Define the bare bones user model in your settings:

    AUTH_USER_MODEL = 'funky_user.User'

Remember to run the `syncdb` management command to create the database table.


## Usage and customizations

See example usage of customizations in the example/demo_project/accounts
directory.


### Model references

When refering to the user model in your code, you should avoid referencing
the actual model and instead do something like this (from the
[Django docs](https://docs.djangoproject.com/en/1.5/topics/auth/customizing/#referencing-the-user-model)):

    from django.contrib.auth import get_user_model
    User = get_user_model()

    user = User.objects.get(id=1)

When you create a relation to your user model, you should utilize the setting:

    from django.conf import settings
    from django.db import models

    class BlogPost(models.Model):
        author = models.ForeignKey(settings.AUTH_USER_MODEL)


### Custom User model

You can easily extend the provided model with your own fields and methods.
Create a new application (eg. `accounts`) and create a new model:

    from funky_user.models import AbstractBaseUser

    class User(AbstractBaseUser):
        website = models.URLField(_('website'))
        twitter_handle = models.CharField(_('twitter handle'), max_length=100)

When you create your own model, you must point the `AUTH_USER_MODEL` setting
to it.

    AUTH_USER_MODEL = 'accounts.User'


#### Permissions

If you want permissions support (per user, for groups, etc, provided by
default in earlier versions of Django), you can use the `PermissionsMixin`
provided by Django:

    from django.contrib.auth.models import PermissionsMixin
    from funky_user.models import AbstractBaseUser

    class User(AbstractBaseUser, PermissionsMixin):
        website = models.URLField(_('website'))


#### User model in Django admin

For the custom User model to work with the Django admin, we had to override it
since it depends on a `username` field. We have provided a basic admin
configuration that works with the default model.

If you don't want the provided admin configuration, unregister it and add your
own: In your application's `admin.py` file:

    from django.contrib import admin
    from django.contrib.auth import get_user_model

    admin.site.unregister(get_user_model())

You can subclass the provided admin configuration and override the things you
need.


### Included views and URL configuration

The URL configuration is split into two modules: login, logout, password change
and password reset (Django's built-in views) are located in `funky_user.urls.auth`,
and the registration functionality is in `funky_user.urls.signup`. If you want
to utilize both, you can import from `funky_user.urls` directly.

If you want custom functionality in the same URL namespace, you can just extend
the provided configuration in your own URL configuration:

    from django.conf.urls import patterns, url
    from funky_user.urls import urlpatterns

    urlpatterns += patterns('accounts.views',
        url(r'^edit/$', 'edit', name='user-edit'),
    )


### Templates

Since every project has different requirements for templates, we have chosen
not to include them with the `funky_user` package. Instead they are available
separately, in the `tests/templates/auth` folder. Just drop them in your
project's template folder and you should have a decent starting point.
(They fit perfectly with Twitter's Bootstrap project.)


## Implementation notes

* We would like to know which of our registered users has logged in and have
the `last_login` field be nullable. But to override it, we need to duplicate
Django's `AbstractBaseUser` model with password functionality, etc. Instead, we
set `last_login` to a date way back (1970-01-01) when a user registers.


### TODO

_Developer notes_

Things to do:

* Only send activation mail if user is inactive?
* Email field in login as EmailField?
* Remove dependency on django-groove, include send_html_email function?
* Provide example User models in documentation, remove from models.py?
* More tests

Random thoughts:

* Don't include a concrete class, so we don't have to manage migrations in this project?
* Add translations
* Support for changing email addresses?
* Package name: django-funky-user
* Module name: funky_user
* Template directory name: auth?
* URL name prefix: user? account? accounts?
