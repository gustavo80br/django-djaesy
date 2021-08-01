#!/usr/bin/env python
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

djaesy_package = 'git+https://github.com/gustavo80br/django-djaesy'
src_folder = 'src'


def start_project(project_name, execution_path):
    project_path = os.path.join(execution_path, project_name)
    if not Path(os.path.join(execution_path, project_name)).is_dir():
        os.mkdir(project_path)
        os.chdir(project_path)
        subprocess.call([sys.executable, '-m', 'pip', 'install', 'django'], shell=True)
        subprocess.call([sys.executable, '-m', 'pip', 'install', 'virtualenv'], shell=True)
        subprocess.call(['django-admin', 'startproject', project_name], shell=True)
        os.rename(project_name, src_folder)
        os.chdir('..')
    else:
        print("Assuming the project exists, skipping.")


def install_virtualenv(project_path, execution_path):
    if not Path(os.path.join(project_path, 'venv')).is_dir():
        os.chdir(project_path)
        subprocess.call(['virtualenv', '--python', sys.executable, 'venv'], shell=True)
        os.chdir(execution_path)
    else:
        print("Assuming the virtualenv exists, skipping.")


def create_gitignore(project_path):
    if not Path(os.path.join(project_path, '.gitignore')).exists():
        gitignore = open(f"{project_path}/.gitignore", "w")
        gitignore.write("""
venv/
.idea/
__pycache__/
*.py[cod]
*$py.class
        """)
        gitignore.close()
    else:
        print("Assuming the .gitignore exists, skipping.")


def call_in_venv_step(project, project_path, src_path, main_path):
    venv_python_bin = os.path.join(project_path, 'venv', 'Scripts', 'python.exe')
    subprocess.call([venv_python_bin,
        'bootstrap-djaesy.py',
        project,
        '--path', project_path,
        '--src-folder', src_path,
        '--main-folder', main_path,
        '--in-venv'
    ])


def append_item_to_list(position_re, append_str, work_file, adjust=2):

    regexp = re.compile(position_re)

    fp = open(work_file, "r")
    file_str = fp.read()

    match_str = regexp.findall(file_str)

    if match_str:
        match_str = match_str[0]
    else:
        return

    match_pos = file_str.find(match_str)
    match_pos = match_pos + len(match_str) - adjust

    file_head = file_str[:match_pos]
    file_bottom = file_str[match_pos:]

    file_str = file_head + append_str + file_bottom

    fp.close()
    fp = open(work_file, "w")
    fp.write(file_str)
    fp.close()


def install_djaesy(project_path):
    if not Path(os.path.join(project_path, 'requirements.txt')).exists():
        subprocess.call(['pip', 'install', '--no-cache-dir', '-U', djaesy_package], shell=True)
        requirements = open(os.path.join(project_path, 'requirements.txt'), "w")
        requirements.write(djaesy_package)
        requirements.close()
    else:
        print(f'Assuming requirements.txt exists, skipping. Add {djaesy_package} to the requirements.txt manually')


def setup_djaesy(project_path, src_folder, main_folder):
    append_item_to_list(r"INSTALLED_APPS = \[[\s'\w\.,]*\]", "\n    'djaesy',", f"{os.path.join(project_path, src_folder, main_folder, 'settings.py')}")
    append_item_to_list(r"from django\.urls import path", ", include", f"{os.path.join(project_path, src_folder, main_folder, 'urls.py')}", adjust=0)
    append_item_to_list(r"urlpatterns = \[[\s\w\('\/,\.\)]*\]", "\n    path('', include('djaesy.urls')),", f"{os.path.join(project_path, src_folder, main_folder, 'urls.py')}")


def parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument("project")
    parser.add_argument("--in-venv", action='store_true')
    parser.add_argument("--path")
    parser.add_argument("--src-folder")
    parser.add_argument("--main-folder")

    arguments, other_arguments = parser.parse_known_args()
    return arguments, other_arguments


def main():

    args, other_args = parse_arguments()
    project = args.project

    start_pwd = os.getcwd()
    project_pwd = os.path.join(start_pwd, project)

    if not args.in_venv:
        print("Starting Django project")
        start_project(project, start_pwd)
        print("Installing a virtualenv environment")
        install_virtualenv(project_pwd, start_pwd)
        print("Creating a .gitignore file")
        create_gitignore(project_pwd)
        print("Going into Venv environment...")
        call_in_venv_step(project, project_pwd, src_folder, project)
    else:
        path = args.path
        src_path = args.src_folder
        main_path = args.main_folder
        print("Installing Djaesy into venv")
        install_djaesy(path)
        print("Setting up Djaesy for the project")
        setup_djaesy(path, src_path, main_path)


if __name__ == '__main__':
    main()