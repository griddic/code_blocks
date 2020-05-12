"""
usage:
    python setup_client_from_protos {path to directory with protos}
"""
import os
import site
import sys
from contextlib import contextmanager
from distutils.dir_util import copy_tree

import pkg_resources
from grpc_tools.protoc import main as protoc_main


def iter_files(path: str):
    for _path, subdirs, files in os.walk(path):
        for name in files:
            yield _path, name


def join_py_with_pyi(folder):
    for _dir, name in iter_files(folder):
        if name.find('.py') == -1:
            continue
        file_path = os.path.join(_dir, name)
        new_folder = _dir[0] + _dir[1:].replace('.', os.path.sep)
        if _dir == new_folder:
            continue
        new_path = os.path.join(new_folder, name)
        os.makedirs(new_folder, exist_ok=True)
        os.rename(file_path, new_path)


def workaround_none_emums(folder):
    for _dir, name in iter_files(folder):
        if name.find('.py') == -1:
            continue
        file_path = os.path.join(_dir, name)
        with open(file_path) as inn:
            content = inn.read()

        content = content.replace('\nNone = ', '\nNONE = ')

        with open(file_path, 'w') as outt:
            outt.write(content)


def _protoc_main(command):
    if isinstance(command, str):
        command = command.split()
    proto_include = pkg_resources.resource_filename('grpc_tools', '_proto')
    protoc_main(command + ['-I{}'.format(proto_include)])


@contextmanager
def change_cwd(new_cwd):
    original_cwd = os.getcwd()
    os.chdir(new_cwd)
    yield
    os.chdir(original_cwd)


if __name__ == '__main__':
    path_to_proceed = sys.argv[1]
    path_to_proceed = os.path.normpath(path_to_proceed)

    with change_cwd(path_to_proceed):
        for folder, name in iter_files('.'):
            if name.find('.proto') == -1:
                continue
            file_path = os.path.join(folder, name)
            file_path = os.path.normpath(file_path)
            _protoc_main(f'{sys.argv[0]} -I=./ --python_out=./ --mypy_out=./ --grpc_python_out=./ {file_path}')

        join_py_with_pyi('.')

        workaround_none_emums('.')

        sitepackages_path = site.getsitepackages()[0]
        copy_tree('.', sitepackages_path)
        print(f'Client has been installed into {sitepackages_path}')
