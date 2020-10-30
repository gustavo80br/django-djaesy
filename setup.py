#!/usr/bin/env python

import os
from setuptools import find_packages, setup

# with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
#     README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-djaesy',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Django Djaesy',
    long_description=README,
    url='https://github.com/gustavo80br/django-djaesy/',
    author='Gustavo H. de A. Gonçalves',
    author_email='gustavo@gemtech.net.br',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.0.1',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'django==3.0.1',
        'django-localflavor==2.2',
        'django-autocomplete-light==3.5.0',
        'django-crum==0.7.5',
        'django-crispy-forms==1.8.1',
        'django-filter==2.2.0',
        'django-image-cropping==1.3.0',
        'django_countries==5.5',
        'django_polymorphic==2.1.2',
        'django-stubs',
        'django_leaflet==0.26.0',
        'djangorestframework',
        'djangorestframework-stubs',
        'django-cleanup',
        'simplejson',
        'orjson',
        'django-geojson',
        'django-chartjs',
        'pandas==1.0.0',
        'jinja2==2.11.1',
        'openpyxl==3.0.3',
        'xlwt==1.3.0',
        'xlsxwriter',
        'easy_thumbnails==2.7',
        'requests',
        'pytz',
        'whitenoise[brotli]',
        'markdown',
    ],
    test_suite = tests.get_suite
)
