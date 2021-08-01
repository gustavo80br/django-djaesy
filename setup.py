#!/usr/bin/env python

import os
from setuptools import find_packages, setup

# with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
#     README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-djaesy',
    version='0.1.0',
    packages=['djaesy'],
    package_data={'djaesy': ['*']},
    include_package_data=True,
    license='MIT License',
    description='Django Djaesy',
    long_description='Django Djaesy',
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
        'Django==3.2.5',
        'django-localflavor==3.1',
        'django-autocomplete-light==3.8.2',
        'django-crum==0.7.9',
        'django-crispy-forms==1.12.0',
        'django-filter==2.4.0',
        'django-image-cropping==1.5.0',
        'django_countries==7.2.1',
        'django_polymorphic==3.0.0',
        'django-stubs==1.8.0',
        'django_leaflet==0.28.1',
        'djangorestframework==3.12.4',
        'djangorestframework-stubs==1.4.0',
        'django-cleanup==5.2.0',
        'simplejson==3.17.3',
        'orjson==3.6.0',
        'django-geojson==3.2.0',
        'django-chartjs==2.2.1',
        'pandas==1.3.1',
        'jinja2==3.0.1',
        'openpyxl==3.0.7',
        'xlwt==1.3.0',
        'xlsxwriter==1.4.5',
        'easy_thumbnails==2.7.1',
        'requests==2.26.0',
        'pytz==2021.1',
        'whitenoise[brotli]==5.3.0',
        'markdown==3.3.4',
    ]
)
