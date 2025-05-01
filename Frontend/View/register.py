from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtCore import Qt, QPoint
import sys
import resources_rc

from PyQt6.QtWidgets import QApplication

class Register(QtWidgets.QWidget):
    def __init__(self):
        super().__init__(   )
        uic.loadUi("../login_resgister.ui", self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.placeholder_label = QLabel("Enter your date of birth", self)
        self.placeholder_label.setStyleSheet("color: gray; position: absolute;")
        self.placeholder_label.move(self.DateOfBirth.x() + 5, self.DateOfBirth.y() + 3)
        self.placeholder_label.raise_()
        self.DateOfBirth.dateChanged.connect(self.hide_placeholder)
        self.DateOfBirth.installEventFilter(self)
        def hide_placeholder(self):
            self.placeholder_label.hide()

        def eventFilter(self, obj, event):
            if obj == self.DateOfBirth and event.type() == QEvent.FocusIn:
                self.placeholder_label.hide()
            return super().eventFilter(obj, event)
        
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



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = Register()
    main.show()

    sys.exit(app.exec())