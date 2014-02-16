# -*- encoding:utf8 -*-
import os
from email.utils import parseaddr
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

raise RuntimeError(
    "Needs author, email and version, edit the setup.py"
    "file and remove this Exception."
)

author, author_email = parseaddr("Author <email>")  # Edit
version = "0.1"  # Edit
url = 'http://github.com/c1srl/fucksia'  # Edit

setup(name='fucksia-django',
    url=url,
    version=version,
    description=README.split('\n\n')[0],
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author=author,
    author_email=author_email,
    packages=find_packages(),
    namespace_packages=['django-fucksia'],
    include_package_data=True,
    install_requires=[
        'setuptools',
    ],
    zip_safe=False,
)
