import os

from pathlib import Path
from subprocess import call

call('pip install gdal', shell=True)

try:
    from django import settings
    from django.core.management.base import BaseCommand
except:
    if os.name == 'nt':
        print('\n'
              'Ops! You are on Windows... :)\n'
              '\n'
              'Visit https://www.lfd.uci.edu/~gohlke/pythonlibs/ and download the right GDAL version for you.\n'
              'cp37 means Python 3.7 for example, and choose between amd64 or win32 version.\n'
              '\n'
              'Install the wheel file with pip, like this:\n'
              '\n'
              '     pip install GDAL‑3.1.3‑cp36‑cp36m‑win_amd64.whl\n'
              '\n'
              'Find the path to the wheel installation, set this path to the OSGEOS4W variable, and the code\n'
              'below to your project settings.py file:\n'
              '\n'
              '     OSGEO4W = r"G:/Dev/venv/iflew/Lib/site-packages/osgeo"\n'
              '     assert os.path.isdir(OSGEO4W), "Directory does not exist: " + OSGEO4W\n'
              '     os.environ["OSGEO4W_ROOT"] = OSGEO4W\n'
              '     os.environ["GDAL_DATA"] = OSGEO4W + r"/data/gdal"\n'
              '     os.environ["PROJ_LIB"] = OSGEO4W + r"/data/proj"\n'
              '     os.environ["PATH"] = OSGEO4W + r";" + os.environ["PATH"]\n'
              '     GEOS_LIBRARY_PATH = "OSGEO4W" + "/geos_c.dll"\n'
              '     GDAL_LIBRARY_PATH = "OSGEO4W" + "/gdal204.dll"\n'
              '\n'
              'Make shure you have the gdal204.dll in the folder, or user the respective version you installed.\n'
        )
    else:
        print('Could not pip install gdal!')
    
    
class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        if os.name == 'nt':
            print('\n'
                  'Ops! You are on Windows... :)\n'
                  '\n'
                  'Visit https://www.lfd.uci.edu/~gohlke/pythonlibs/ and download the right GDAL version for you.\n'
                  'cp37 means Python 3.7 for example, and choose between amd64 or win32 version.\n'
                  '\n'
                  'Install the wheel file with pip, like this:\n'
                  '\n'
                  '     pip install GDAL‑3.1.3‑cp36‑cp36m‑win_amd64.whl\n'
                  '\n'
                  'Find the path to the wheel installation, set this path to the OSGEOS4W variable, and the code\n'
                  'below to your project settings.py file:\n'
                  '\n'
                  '     OSGEO4W = r"G:/Dev/venv/iflew/Lib/site-packages/osgeo"\n'
                  '     assert os.path.isdir(OSGEO4W), "Directory does not exist: " + OSGEO4W\n'
                  '     os.environ["OSGEO4W_ROOT"] = OSGEO4W\n'
                  '     os.environ["GDAL_DATA"] = OSGEO4W + r"/data/gdal"\n'
                  '     os.environ["PROJ_LIB"] = OSGEO4W + r"/data/proj"\n'
                  '     os.environ["PATH"] = OSGEO4W + r";" + os.environ["PATH"]\n'
                  '     GEOS_LIBRARY_PATH = "OSGEO4W" + "/geos_c.dll"\n'
                  '     GDAL_LIBRARY_PATH = "OSGEO4W" + "/gdal204.dll"\n'
                  '\n'
                  'Make shure you have the gdal204.dll in the folder, or user the respective version you installed.\n'
            )
        else:
            call('pip install gdal', shell=True)
