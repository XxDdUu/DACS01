import sys

from PyQt6.QtWidgets import (QMainWindow, QApplication,
                             QLabel, QListWidget, QListWidgetItem, QWidget)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QFont, QIcon
from loginUI import Ui_MainWindow


class Login(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setFixedSize(743,490)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('./img/logo/dark_pythonLogo.png'))

        self.loginTitle = self.ui.title_header
        self.loginTitle.setObjectName("loginTitle")
        self.loginTitle.setText("Sign Up")

        self.bg_logo = self.ui.label
        self.bg_logo.setObjectName("bgLogo")
        self.bg_logo.setPixmap(QPixmap("./img/logo/dark_pythonLogo.png"))
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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open('./loginStyle.qss') as f:
        loginQss = f.read()
        app.setStyleSheet(loginQss)

    window = Login()
    window.show()
    sys.exit(app.exec())
