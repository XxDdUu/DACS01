from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtCore import Qt, QPoint, QEvent
import sys
import Frontend.View.resources_rc

from PyQt6.QtWidgets import QApplication

class Register(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("Frontend/login_resgister.ui", self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.close_btn.clicked.connect(self.close)
        self.minimize_btn.clicked.connect(self.showMinimized)
        self.maximize_btn.clicked.connect(self.toggle_maximize)

        self.is_maximized = False

        self._drag_active = False
        self._drag_position = QPoint()

        # Assume your header is called headerFrame
        self.header.mousePressEvent = self.mouse_press_event
        self.header.mouseMoveEvent = self.mouse_move_event
        self.header.mouseReleaseEvent = self.mouse_release_event


        # Example: custom button signals
        self.minimize_btn.clicked.connect(self.showMinimized)
        self.close_btn.clicked.connect(self.close)

        self.switch_to_login = None
        self.login_label.clicked.connect(self.handle_switch)
    
    def handle_switch(self):
        if self.switch_to_login:
            self.switch_to_login()
    def mouse_press_event(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_active = True
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouse_move_event(self, event):
        if self._drag_active and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def mouse_release_event(self, event):
        self._drag_active = False
    def toggle_maximize(self):
        if self.is_maximized:
            self.showNormal()
        else:
            self.showMaximized()
        self.is_maximized = not self.is_maximized

