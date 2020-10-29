import os

from pathlib import Path
from subprocess import call

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        webpack_source = os.path.join(
            Path(os.path.abspath(__file__)).parent.parent.parent,
            settings.DJAESY_WEBPACK_FOLDER
        )
        os.chdir(webpack_source)
        path = os.path.join(webpack_source, 'webpack.config.js')
        call(f'npx webpack --config {path}', shell=True)
