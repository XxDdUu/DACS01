import sys

from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import (QMainWindow, QApplication,
                             QLabel, QListWidget, QListWidgetItem, QWidget)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QFont, QIcon
from frameUI import Ui_MainWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Initialize the UI from the generated mainFrame class
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon("img/logo/dark_pythonLogo.png"))

        # Initialize UI elements
        self.titleLabel = self.ui.title_label
        self.titleLabel.setText("PyMe")

        self.titleLogo = self.ui.iconTitle_label
        self.titleLogo.setText("")
        self.titleLogo.setPixmap(QPixmap("img/logo/dark_pythonLogo.png"))
        self.titleLogo.setFixedSize(QSize(50, 50))
        self.titleLogo.setScaledContents(True)

        self.sideFullMenu = self.ui.listWidget_2
        self.sideFullMenu.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.sideIconMenu = self.ui.listWidget
        self.sideIconMenu.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.sideIconMenu.hide()

        self.menuBtn = self.ui.menuButton
        self.menuBtn.setText("")
        self.menuBtn.setObjectName("menu_btn")
        self.menuBtn.setIcon(QIcon("img/icon/sidebar.png"))
        self.menuBtn.setIconSize(QSize(20, 20))
        self.menuBtn.setCheckable(True)
        self.menuBtn.setChecked(False)

        self.mainContent = self.ui.stackedWidget

        # Define a list of menu items with name and icon
        self.menuItems = [
            {
                "name": "Home",
                "icon": "img/icon/home.png"
            },
            {
                "name": "Revenue Data",
                "icon": "img/icon/revenue_chart.png"
            },
            {
                "name": "Reports",
                "icon": "img/icon/report.png"
            },
            {
                "name": "Setting",
                "icon": "img/icon/setting.png"
            },
        ]
        # Initialize the main Q
        self.init_ListWidget()
        self.connect_signal_slot()
        self.init_stackWidget()

    def init_ListWidget(self):
        self.sideIconMenu.clear()
        self.sideFullMenu.clear()

        for item in self.menuItems:
            # Set items for the side menu with the icons only
            item_A = QListWidgetItem()
            item_A.setIcon(QIcon(item.get("icon")))
            item_A.setSizeHint(QSize(45, 50))
            self.sideIconMenu.addItem(item_A)
            self.sideIconMenu.setCurrentRow(0)

            # Set items for the side 'full' menu
            item_B = QListWidgetItem()
            item_B.setIcon(QIcon(item.get("icon")))
            item_B.setText(item.get("name"))
            item_B.setSizeHint(QSize(50, 50))
            self.sideFullMenu.addItem(item_B)
            self.sideFullMenu.setCurrentRow(0)

    def connect_signal_slot(self):
        self.menuBtn.toggled["bool"].connect(self.sideFullMenu.setHidden)
        self.menuBtn.toggled["bool"].connect(self.titleLogo.setHidden)
        self.menuBtn.toggled["bool"].connect(self.titleLabel.setHidden)
        self.menuBtn.toggled["bool"].connect(self.sideIconMenu.setVisible)

        self.sideFullMenu.currentRowChanged["int"].connect(self.mainContent.setCurrentIndex)
        self.sideIconMenu.currentRowChanged["int"].connect(self.mainContent.setCurrentIndex)
        self.sideIconMenu.currentRowChanged["int"].connect(self.sideFullMenu.setCurrentRow)
        self.sideIconMenu.currentRowChanged["int"].connect(self.sideIconMenu.setCurrentRow)

        self.menuBtn.toggled.connect(self.iconButtonChange)

    def iconButtonChange(self, status):
        # change the icon button of menu based on its status
        if status:
            self.menuBtn.setIcon(QIcon("img/icon/sidebar.png"))
        else:
            self.menuBtn.setIcon(QIcon("img/icon/sidebar.png"))

    def init_stackWidget(self):
        # create content page in stackWidget
        widget_list = self.mainContent.findChildren(QWidget)
        for widgetChild in widget_list:
            self.mainContent.removeWidget(widgetChild)

        for menu in self.menuItems:
            text = menu.get("name")
            layout = QGridLayout()
            label = QLabel(text=text)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            font = QFont()
            font.setPixelSize(20)
            label.setFont(font)
            layout.addWidget(label,0,0)
            newPage = QWidget()
            newPage.setLayout(layout)
            self.mainContent.addWidget(newPage)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
