import os

from PyQt6.QtWidgets import (QMainWindow, QApplication,
                             QLabel, QListWidget, QListWidgetItem, QWidget)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QFont, QIcon
from Frontend.View.loginUI import Ui_MainWindow
class Login(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setFixedSize(743,490)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('Frontend/View/img/logo/dark_pythonLogo.png'))

        self.loginTitle = self.ui.title_header
        self.loginTitle.setObjectName("loginTitle")
        self.loginTitle.setText("Sign Up")

        self.bg_logo = self.ui.label
        self.bg_logo.setObjectName("bgLogo")
        self.bg_logo.setPixmap(QPixmap("Frontend/View/img/logo/dark_pythonLogo.png"))
        self.bg_logo.setFixedSize(400, 450)
        self.bg_logo.setScaledContents(True)

        self.usernameLabel = self.ui.usernameLabel
        self.usernameLabel.setObjectName("usernameLabel")
        self.usernameLabel.setText("Username:")

        self.passwordLabel = self.ui.passLabel
        self.passwordLabel.setObjectName("passwordLabel")
        self.passwordLabel.setText("Password:")

        self.signUp_button = self.ui.login_btn
        self.signUp_button.setObjectName("signUpButton")
        self.signUp_button.setText("Login")

        self.register_button = self.ui.register_btn
        self.register_button.setObjectName("registerButton")
        self.register_button.setText("Create new account?")

        self.nameLineEdit = self.ui.passLineEdit.setObjectName("nameLineEdit")
        self.passLineEdit = self.ui.passLineEdit.setObjectName("passLineEdit")

        self.switch_to_register = None
        self.register_button.clicked.connect(self.handle_switch)

        self.load_stylesheet()
    def handle_switch(self):
        if self.switch_to_register:
            self.switch_to_register()
    def load_stylesheet(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        css_path = os.path.join(script_dir, 'loginStyle.css')
        
        try:
            with open(css_path, 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Error: CSS file not found at {css_path}")
        except Exception as e:
            print(f"Error loading stylesheet: {e}")