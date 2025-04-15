import sys

from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtWidgets import (QMainWindow, QApplication, QPushButton,
                             QLabel, QLineEdit, QVBoxLayout, QWidget, QSizePolicy, QHBoxLayout, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QGuiApplication


class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(220,100,500,550)
        # self.setFixedSize(700, 500)
        # self.resize(700, 500)

        self.img_label = QLabel()
        self.signUp_label = QLabel("Sign-in", self)
        self.username_label = QLabel("Username:", self)
        self.username_input = QLineEdit(self)
        self.password_label = QLabel("Password:", self)
        self.password_input = QLineEdit(self)
        self.signUp_button = QPushButton("Đăng nhập", self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("PyMe APP")

        login_layout = QVBoxLayout()
        login_layout.addWidget(self.signUp_label)
        login_layout.addWidget(self.username_label)
        login_layout.addWidget(self.username_input)
        login_layout.addWidget(self.password_label)
        login_layout.addWidget(self.password_input)
        login_layout.addWidget(self.signUp_button)

        pixmap = QPixmap("img/logo/dark_pythonLogo.png")
        self.img_label.setPixmap(pixmap.scaled(350,350))


        self.signUp_label.setFixedSize(500,52)
        self.username_label.setFixedSize(350,30)
        self.password_label.setFixedSize(350,30)
        self.username_input.setFixedSize(350,30)
        self.password_input.setFixedSize(350,30)
        self.signUp_button.setFixedSize(120,35)

        self.signUp_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.username_input.setAlignment(Qt.AlignmentFlag.AlignCenter |
                                         Qt.AlignmentFlag.AlignTop)
        self.password_input.setAlignment(Qt.AlignmentFlag.AlignCenter |
                                         Qt.AlignmentFlag.AlignTop)

        self.signUp_label.setObjectName("signUp_label")
        self.username_label.setObjectName("username_label")
        self.username_input.setObjectName("username_input")
        self.password_label.setObjectName("password_label")
        self.password_input.setObjectName("password_input")
        self.signUp_button.setObjectName("signUp_button")

        self.setStyleSheet("""
            QLabel,QPushbutton,QPixmap{
                background-color: white;
                color: black;
                font-family: Cascadia Mono SemiBold;
            }
            QLabel#signUp_label{
                font-size: 39px;
                padding-left: 50%;
            }
            QLabel#username_label{
                font-size: 19px;
            }
            QLabel#password_label{
                font-size: 19px;
                indent: 10px;
            }
            QLineEdit#username_input{
                font-size: 19px;
                padding-right: 300px;
                border-radius: 10px;
                border: 2px solid black;
            }
            QLineEdit#password_input{
                font-size: 19px;
                padding-right: 300px;
                border-radius: 10px;
                border: 2px solid black;
            }
            # QPushButton#signUp_button{
            #     font-size: 18px;
            #     border-radius: 10px;
            # }
           QPushButton#signUp_button:hover{
                background-color: #c9c9c9;
        """)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.img_label)
        main_layout.addLayout(login_layout)
        self.setLayout(main_layout)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window,QColor("white"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec())
