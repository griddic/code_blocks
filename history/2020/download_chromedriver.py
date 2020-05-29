#!/usr/bin/env python

import contextlib
import os
import shutil
import stat
import zipfile
from urllib.request import urlretrieve

import click

import pip
import requests
from tqdm import tqdm


@contextlib.contextmanager
def pushd(new_dir):
    previous_dir = os.getcwd()
    os.makedirs(new_dir, exist_ok=True)
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)


@click.group()
def cli():
    pass


@cli.group()
def install():
    pass


@install.command()
def chromedriver():
    with pushd('.tmp'):
        url = "https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_mac64.zip"
        file = url.split('/')[-1]
        with requests.get(url, stream=True) as resp:
            with open(file, 'wb') as out:
                for pice in tqdm(resp.iter_content(chunk_size=None)):
                    out.write(pice)
        dir = '.'.join(file.split('.')[:-1])
        with zipfile.ZipFile(file) as zip_ref:
            zip_ref.extractall(dir)
    os.makedirs('.driver', exist_ok=True)
    driver_file = os.path.join('.driver', 'chromedriver')
    shutil.copy(os.path.join('.tmp', dir, 'chromedriver'), driver_file)
    st = os.stat(driver_file)
    os.chmod(driver_file, st.st_mode | stat.S_IEXEC)


@install.command()
def requirements():
    pip.main('install -r requirements.txt'.split())


if __name__ == '__main__':
    cli()
