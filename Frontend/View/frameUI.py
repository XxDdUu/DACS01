# Form implementation generated from reading ui file 'dashboardUI.ui'
#
# Created by: PyQt6 UI code generator 6.9.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(700, 500)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.title_frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.title_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.title_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.title_frame.setObjectName("title_frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.title_frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.iconTitle_label = QtWidgets.QLabel(parent=self.title_frame)
        self.iconTitle_label.setObjectName("iconTitle_label")
        self.horizontalLayout.addWidget(self.iconTitle_label)
        self.title_label = QtWidgets.QLabel(parent=self.title_frame)
        self.title_label.setObjectName("title_label")
        self.horizontalLayout.addWidget(self.title_label)
        self.menuButton = QtWidgets.QPushButton(parent=self.title_frame)
        self.menuButton.setObjectName("menuButton")
        self.horizontalLayout.addWidget(self.menuButton)
        self.gridLayout.addWidget(self.title_frame, 0, 0, 1, 2)
        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stackedWidget.addWidget(self.page_2)
        self.gridLayout.addWidget(self.stackedWidget, 0, 2, 2, 1)
        self.listWidget = QtWidgets.QListWidget(parent=self.centralwidget)
        self.listWidget.setMaximumSize(QtCore.QSize(50, 16777215))
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 1, 0, 1, 1)
        self.listWidget_2 = QtWidgets.QListWidget(parent=self.centralwidget)
        self.listWidget_2.setMaximumSize(QtCore.QSize(155, 16777215))
        self.listWidget_2.setObjectName("listWidget_2")
        self.gridLayout.addWidget(self.listWidget_2, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 648, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.iconTitle_label.setText(_translate("MainWindow", "TextLabel"))
        self.title_label.setText(_translate("MainWindow", "TextLabel"))
        self.menuButton.setText(_translate("MainWindow", "PushButton"))
