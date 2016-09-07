#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import sys
import os.path
from os.path import abspath, dirname
import importlib

from .utils import settings
from .utils import threadutils
from .utils.compat import QtCore, QtGui, QtWidgets, version
from .utils.compat import WATCH_UI_CHANGES


def onHotswap():
    """Called when the source of this module has changed.

    When a function named 'onHotswap' is present in a module,
    this function is called after the module is reloaded.
    This should be used to trigger a redisplay of the screen or
    in general to discard cached results that are to be calculated
    again using the new method definitions.

    If onHotswap is not defined the module is reloaded anyway, but afterwards
    no further actions are performed. In this case the changed code has to be
    activated some other way like minimizing and restoring the window to be
    repainted.
    """
    threadutils.invoke_in_main_thread(create_mainwindow)


def create_widget_func():
    return _create_widget_func


def create_mainwindow():
    create_widget_func()()


def directory_changed(path):
    pass


_timers = {}


def file_changed(path):
    print('file_changed', path)
    if path.endswith('.ui'):
        # When a ui file is written by Qt Designer we can get
        # more than one file change notification.
        # We only want to recreate the user interface after
        # the last notification.
        milliseconds = 100
        oldtimer = _timers.get(path)
        if oldtimer is not None:
            oldtimer.stop()
        timer = QtCore.QTimer()
        _timers[path] = timer
        timer.timeout.connect(lambda: recreate_widget(path))
        timer.setSingleShot(True)
        timer.start(milliseconds)


def recreate_widget(uifile):
    try:
        del _timers[uifile]
    except KeyError:
        pass
    # Calculate the absolute module name from the
    # name of the changed ui file.
    parentpath = dirname(dirname(abspath(__file__)))
    module = uifile[len(parentpath + os.sep):]
    module = module[:-len('.ui')]
    module = module.replace(os.sep, '.')
    ui_module = importlib.import_module(module)
    try:
        create_widget = ui_module.create_widget
    except AttributeError:
        create_widget = None
    if create_widget is not None:
        create_widget()


def start_ui_watcher(paths):
    fs_watcher = QtCore.QFileSystemWatcher(paths)
    fs_watcher.directoryChanged.connect(directory_changed)
    fs_watcher.fileChanged.connect(file_changed)
    return fs_watcher

# -------------------------------------------------------


def ui_paths(projectdir):
    """

    Returns:
        A list of .ui files in the project.
    """
    entries = []
    for path, dirs, files in os.walk(abspath(projectdir)):
        for name in files:
            if name.endswith('.ui'):
                filename = os.path.join(path, name)
                entries.append(filename)
    return entries


def start_app(modulename):
    global _create_widget_func

    ui_module = importlib.import_module(modulename)
    try:
        create_widget = ui_module.create_widget
    except AttributeError:
        create_widget = None
    _create_widget_func = create_widget

    settings.BASE_DIRECTORY = dirname(abspath(sys.argv[0]))
    print(settings.BASE_DIRECTORY)
    print(version())

    if WATCH_UI_CHANGES:
        paths = ui_paths(settings.BASE_DIRECTORY)
        print(paths)

        # We store a reference to fs_watcher otherwise
        # it would be garbage collected immediately.
        fs_watcher = start_ui_watcher(paths)

    useGUI = True
    app = QtWidgets.QApplication(sys.argv)
    widget = create_mainwindow()
    return app.exec_()


def main(modulename):
    return start_app(modulename)

if __name__ == "__main__":
    main()
