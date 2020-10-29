#!/usr/bin/env python
from __future__ import absolute_import

import os

import django
from django.db import connections
from django.db.utils import OperationalError

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sample_project.settings")
    django.setup()

    db_conn = connections['default']
    try:
        c = db_conn.cursor()
    except OperationalError as e:
        print('--------------OperationalError--------------')
        print(e)
        exit(1)

    exit(0)
