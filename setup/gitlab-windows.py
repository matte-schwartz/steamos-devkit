#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import shutil

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PACKAGE_FILE = 'devkit-gui-win64.zip'

assert sys.platform == 'win32'
assert sys.prefix == sys.base_prefix    # executed at build VM OS level


# don't let python buffering get in the way or readable output
# https://stackoverflow.com/questions/107705/disable-output-buffering
class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)


def call(cmd):
    print(f'BEGIN CMD: {cmd}')
    subprocess.check_call(cmd, cwd=ROOT_DIR, shell=True)
    print(f'END CMD: {cmd}')


if __name__ == '__main__':
    sys.stdout = Unbuffered(sys.stdout)
    sys.stderr = Unbuffered(sys.stderr)

    call(f'python3.12 -m venv .')
    interpreter = os.path.join(ROOT_DIR, r'Scripts\python.exe')
    call(f'{interpreter} -m pip install --upgrade pip')
    pip = os.path.join(ROOT_DIR, r'Scripts\pip.exe')
    call(f'{pip} install --upgrade setuptools')
    call(f'{pip} install -r requirements.txt')
    call(rf'{interpreter} .\setup\package-windows.py')
    if not os.path.exists(PACKAGE_FILE):
        raise Exception(f'{PACKAGE_FILE} not found')
    os.makedirs('artifacts', exist_ok=True)
    # copy to an artifacts/ file, consistent with the linux build
    shutil.copyfile(PACKAGE_FILE, os.path.join('artifacts', PACKAGE_FILE))
