#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from os.path import abspath, dirname, join

from . import settings

# -------------------------------------------------------


def is_frozen():
    return getattr(sys, 'frozen', False)


# Set USE_PYSIDE to False to run with PyQt instead of PySide
USE_PYSIDE = True

# Set to False to use modules generated by pyuic
DYNAMIC_UI = True
WATCH_UI_CHANGES = True

if not DYNAMIC_UI:
    WATCH_UI_CHANGES = False

if is_frozen():
    DYNAMIC_UI = False
    WATCH_UI_CHANGES = False

# -------------------------------------------------------

PYSIDE_PRESENT = False
if USE_PYSIDE:
    try:
        import PySide
        sys.modules['PyQt4'] = PySide  # HACK for ImageQt
        from PySide import QtGui, QtCore
        # Upward compatibility with PyQt5
        QtWidgets = QtGui
        from PySide.QtCore import Signal
        # The explicit import of PySide.QtXml is needed for PyInstaller
        if is_frozen():
            import PySide.QtXml

        from . import pyside_dynamic as uic
        PYSIDE_PRESENT = True
    except ImportError:
        pass

if not PYSIDE_PRESENT:
    try:
        from PyQt4 import QtCore, QtGui
        QtWidgets = QtGui
        from PyQt4.QtCore import pyqtSignal as Signal
        from PyQt4 import uic
    except ImportError:
        from PyQt5 import QtCore, QtGui, QtWidgets
        from PyQt5.QtCore import pyqtSignal as Signal
        from PyQt5 import uic


def load_ui_file(obj, modulepath, uibasename):
    if is_frozen():
        uifile = join(settings.BASE_DIRECTORY, uibasename)
    else:
        uifile = join(dirname(abspath(modulepath)), uibasename)
    return uic.loadUi(uifile, obj)


def version():
    return "Python %s, %s" % (sys.version.splitlines()[0].strip(), qtversion())


def qtversion():
    try:
        binding = "PyQt %s" % getattr(QtCore, 'PYQT_VERSION_STR')
    except AttributeError:
        binding = "PySide %s" % PySide.__version__
    binding += ", Qt %s" % QtCore.qVersion()
    return binding
