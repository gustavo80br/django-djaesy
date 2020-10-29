#!/usr/bin/env python

import sys

from django.core.management import call_command
from boot_django import boot_django

# get the arguments
args = sys.argv[1:]

# call the django setup routine
boot_django()

call_command(*args)
