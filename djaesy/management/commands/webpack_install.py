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
        node_modules = os.path.join(webpack_source, 'node_modules')

        call('npm install -g yarn', shell=True)

        call(
            f'yarn add --modules-folder {node_modules} --dev '
            f'webpack '
            f'webpack-cli '
            f'vue '
            f'@vue/cli '
            f'lodash '
            f'@coreui/coreui@3.0.0-beta.4',
            shell=True
        )
