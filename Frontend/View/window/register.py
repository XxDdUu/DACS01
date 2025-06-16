from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.QtWidgets import QMainWindow, QLabel, QMessageBox
from PyQt6.QtCore import Qt, QPoint, QEvent
import sys
import Frontend.View.resource.resources_rc

from PyQt6.QtWidgets import QApplication

class Register(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("Frontend/View/ui/login_resgister.ui", self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

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
        self.close_btn.clicked.connect(self.confirm_exit)

        self.switch_to_login = None
        self.login_label.clicked.connect(self.handle_switch)

        self.Background.setCurrentWidget(self.Register_page)

        self.create_enterprise.clicked.connect(lambda: self.Background.setCurrentWidget(self.Enterprise_register))

        self.goback_register.clicked.connect(lambda: self.Background.setCurrentWidget(self.Register_page))

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
    def confirm_exit(self):
        qm = QMessageBox
        res = qm.question(self, 'Confirm', 'Are you sure to exit?', qm.StandardButton.Yes | qm.StandardButton.No)
        if res == qm.StandardButton.Yes:
            self.close()
    def get_employer_form_data(self):
        return {
            "username": self.Username.text().strip(),
            "email": self.Email.text().strip(),
            "phone_number": self.Phone_Num.text().strip(),
            "enterprise_id": self.Enterprise_id.text().strip(),
            "enterprise_password_employer": self.enterprise_password_employer.text().strip(),
            "date_of_birth": self.DateOfBirth.date().toString("yyyy-MM-dd"),
            "password": self.Password.text().strip(),
            "confirm_password": self.Confirm_password.text().strip()
        }
    def get_enterprise_form_data(self):
        return {
            "enterprise_name": self.enterprise_name.text().strip(),
            "enterprise_founder": self.enterprise_founder.text().strip(),
            "enterprise_address": self.enterprise_address.text().strip(),
            "enterprise_phone_number": self.enterprise_phone_number.text().strip(),
            "business_type" : self.business_type.currentText(),
            "enterprise_industry": self.enterprise_industry.text().strip(),
            "enterprise_password": self.enterprise_password.text().strip(),
            "confirm_enterprise_password": self.confirm_enterprise_password.text().strip()
        }
