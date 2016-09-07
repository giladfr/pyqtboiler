#!/usr/bin/env python
# -*- coding: utf-8 -*-

from paver.easy import *
import os.path

TOPLEVEL_DIRS = 'baseapp exampleapp'.split()
SPECFILE = 'start_app.spec'

# UIC_EXECUTABLE = 'pyside-uic-2.7'   # for PySide
# UIC_EXECUTABLE = 'pyside-uic'   # for PySide on Windows
# UIC_EXECUTABLE = 'pyuic4'     # for PyQt 4
UIC_EXECUTABLE = 'pyuic5'     # for PyQt 5


@task
def install_requirements():
    sh('pip install --upgrade -r requirements.txt')


@task
def uic():
    for top in TOPLEVEL_DIRS:
        for path, dirs, files in os.walk(top):
            for name in files:
                if not name.endswith('.ui'):
                    continue
                uifile = os.path.join(path, name)
                pyfile = os.path.splitext(uifile)[0]
                pyfile += '_ui.py'
                sh("%s -o %s %s" % (UIC_EXECUTABLE, pyfile, uifile),
                   env=os.environ)


@task
def buildapp():
    sh("pyinstaller -y %s" % SPECFILE)
