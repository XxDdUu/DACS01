from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QFrame

import time
import sys
import os
import traceback

import Frontend.View.resources_rc

class LoaderThread(QThread):
    finished = pyqtSignal()

    def run(self):
        self.finished.emit()


class LoadingWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("Frontend/Loading_Screen.ui", self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.drop_shadow()
    def start_loading(self, on_done_callback):
        self.progressBar.setValue(0)
        self._value = 0
        self._loading_done = False
        self._on_done_callback = on_done_callback

        # Start progress animation
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_progress)
        self._timer.start(30)

        # Start actual loading in a thread
        self._thread = LoaderThread()
        self._thread.finished.connect(self._on_loading_finished)
        self._thread.start()

    def _on_loading_finished(self):
        self._loading_done = True

    def _update_progress(self):
        if self._value < 100:
            self._value += 2
            self.progressBar.setValue(self._value)

        if self._value >= 100 and self._loading_done:
            self._timer.stop()
            self._on_done_callback()
    def drop_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(50)
        shadow.setXOffset(10)
        shadow.setYOffset(10)
        shadow.setColor(QtGui.QColor(0, 0, 0, 255)) 

        self.main_display_load.setGraphicsEffect(shadow)