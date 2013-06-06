import os
import re
import sys

from setuptools import setup, find_packages

package = 'funky_user'


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """

    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]", init_py, re.MULTILINE).group(1)


# Publish to Pypi
if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    args = {'version': get_version(package)}
    print("You probably want to tag the version:")
    print("  git tag -a %(version)s -m 'version %(version)s'" % args)
    print("  git push --tags")
    sys.exit()

setup(
    name='django-funky-user',
    version=get_version(package),
    url='https://github.com/funkbit/django-funky-user',
    license='BSD',
    description='Django custom user model, registration and tools',
    long_description=open('README.md').read(),
    author='Funkbit',
    author_email='',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        'Topic :: Internet :: WWW/HTTP',
    ],
    test_suite='tests.runtests.main',
    install_requires=['Django>=1.5'],
)
