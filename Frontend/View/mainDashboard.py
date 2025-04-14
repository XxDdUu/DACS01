import sys

from PyQt6.QtWidgets import (QMainWindow, QApplication,
                             QLabel, QListWidget,QListWidgetItem)
from PyQt6.QtCore import Qt,QSize
from PyQt6.QtGui import QPixmap,QFont,QIcon

#import class UI from 'frameUI.py' module
from frameUI import Ui_MainWindow

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        #Innitalize the UI from the generated mainFrame class
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Initalize UI elements
        self.titleLabel = self.ui.title_label
        self.titleLabel.setText("MOONApp")

        self.titleLogo = self.ui.iconTitle_label
        self.titleLogo.setText("")
        self.titleLogo.setPixmap(QPixmap("/App_Project1/View/img/logo/dark_pythonLogo.png"))
        self.titleLogo.setFixedSize(QSize(50,50))
        self.titleLogo.setScaledContents(True)

        self.sideFullMenu = self.ui.listWidget_2
        self.sideFullMenu.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.sideIconMenu = self.ui.listWidget
        self.sideIconMenu.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.menuBtn = self.ui.menuButton
        self.menuBtn.setText("")
        self.menuBtn.setObjectName("menu_btn")
        self.menuBtn.setIcon(QIcon("D:/PYTHON/py_project/App_Project1/View/img/icon/sidebar.png"))
        self.menuBtn.setIconSize(QSize(20,20))
        self.menuBtn.setCheckable(True)
        self.menuBtn.setChecked(False)

        self.mainContent = self.ui.stackedWidget

        #Define a list of menu items with name and icon
        self.menuItems = [
            {
                "name": "Home",
                "icon": "D:/PYTHON/py_project/App_Project1/View/img/icon/home.png"
            },
            {
                "name": "Revenue Data",
                "icon": "D:/PYTHON/py_project/App_Project1/View/img/icon/revenue_chart.png"
            },
            {
                "name": "Reports",
                "icon": "D:/PYTHON/py_project/App_Project1/View/img/icon/report.png"
            },
            {
                "name": "Setting",
                "icon": "D:/PYTHON/py_project/App_Project1/View/img/icon/setting.png"
            },
        ]
        #Initialize the main Q
        self.init_ListWidget()


    def init_ListWidget(self):
        self.sideIconMenu.clear()
        self.sideFullMenu.clear()

        for item in self.menuItems:
            #Set items for the side menu with the icons only
            item_A = QListWidgetItem()
            item_A.setIcon(QIcon(item.get("icon")))
            item_A.setSizeHint(QSize(50,50))
            self.sideIconMenu.addItem(item_A)
            self.sideIconMenu.setCurrentRow(0)

            #Set items for the side 'full' menu
            item_B = QListWidgetItem()
            item_B.setIcon(QIcon(item.get("icon")))
            item_B.setText(item.get("name"))
            item_B.setSizeHint(QSize(50,50))
            self.sideFullMenu.addItem(item_B)
            self.sideFullMenu.setCurrentRow(0 )




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window =  MainWindow()
    window.show()
    sys.exit(app.exec())