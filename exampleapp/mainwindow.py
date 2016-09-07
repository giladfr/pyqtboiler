#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
from baseapp.utils.compat import QtCore, QtGui, QtWidgets, uic, Signal, DYNAMIC_UI, load_ui_file
from baseapp.utils import settings


if DYNAMIC_UI:
    class DlgClass(object): pass
else:
    from . import mainwindow_ui
    DlgClass = mainwindow_ui.Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, DlgClass):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent, flags=QtCore.Qt.WindowStaysOnTopHint)

        if DYNAMIC_UI:
            load_ui_file(self, __file__, 'mainwindow.ui')
        else:
            self.setupUi(self)

        self.setWindowTitle("ExampleApp")

        basedirectory = settings.base_directory()
        default_imgpath = os.path.join(basedirectory, 'data', 'images', 'appicon.png')
        appIcon = QtGui.QIcon(default_imgpath)
        self.setWindowIcon(appIcon)

        self.model = None

        self.pushButton.clicked.connect(self.buttonPressed)

        QtCore.QTimer.singleShot(0, self.after_init)

    def after_init(self):
        pass

    def closeEvent(self, event):
        event.accept()

    def buttonPressed(self, event):
        button_pressed()

    def paintEvent(self, e):
        p = QtGui.QPainter()
        p.begin(self)
        draw_shapes(p)
        p.end()


def button_pressed():
    print("button pressed")


def draw_shapes(p):
    color = QtGui.QColor(0, 0, 0)
    color.setNamedColor('#000000')
    p.setPen(color)

    v = 100
    p.setBrush(QtGui.QColor(255, 0, 0))
    p.drawRect(10, v, 100, 100)

    p.setBrush(QtGui.QColor(0, 255, 0))
    p.drawRect(120, v, 100, 100)

    p.setBrush(QtGui.QColor(0, 0, 255))
    p.drawRect(230, v, 100, 100)

    p.drawLine(10, v - 20, 330, v - 20)


def onHotswap():
    global theform
    print("onHotswap")
    theform.update()


def create_widget():
    global theform

    qapp = QtCore.QCoreApplication.instance()
    toplevelwidgets = qapp.topLevelWidgets()

    geometry = None
    old_data = None
    if toplevelwidgets:
        for oldwidget in toplevelwidgets:
            if isinstance(oldwidget, QtWidgets.QMainWindow):
                old_data = oldwidget.model
                geometry = oldwidget.pos()
                oldwidget.close()
                oldwidget.setParent(None)

    widget = MainWindow()
    widget.model = old_data
    widget.show()
    # Prevent immediate garbage collection
    theform = widget
    widget.setWindowState(QtCore.Qt.WindowActive)
    if geometry is not None:
        widget.move(geometry)
    widget.raise_()

    return widget
