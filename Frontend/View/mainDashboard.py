import os
import sys

from PyQt6.QtWidgets import QScrollArea, QPushButton, QLineEdit, QTableWidget, QFormLayout, QHBoxLayout
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QSizePolicy
from PyQt6.QtWidgets import (QMainWindow, QApplication,
                             QLabel, QListWidgetItem, QWidget)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QFont, QIcon

from Backend.Model.plot_dataChart import generalChart, ProductChart
from Frontend.View.frameUI import Ui_MainWindow

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class MainDashboard(QMainWindow):

    def __init__(self):
        super().__init__()
        screen = QApplication.primaryScreen()
        size = screen.availableGeometry()  # kích thước vùng làm việc (không gồm taskbar)
        self.setGeometry(size)  # set kích thước cửa sổ = màn hình lap,pc

        # Initialize the UI from the generated mainFrame class
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon("D:/Python/py_project/App_Project1/View/img/logo/dark_pythonLogo.png"))

        # Initialize UI elements
        self.titleLabel = self.ui.title_label
        self.titleLabel.setText("PyMe")

        self.titleLogo = self.ui.iconTitle_label
        self.titleLogo.setText("")
        self.titleLogo.setPixmap(QPixmap("D:/Python/py_project/App_Project1/View/img/logo/dark_pythonLogo.png"))
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
        self.menuBtn.setIcon(QIcon("D:/PYTHON/py_project/App_Project1/View/img/icon/sidebar.png"))
        self.menuBtn.setIconSize(QSize(20, 20))
        self.menuBtn.setCheckable(True)
        self.menuBtn.setChecked(False)

        self.mainContent = self.ui.stackedWidget

        self.switch_to_signUp = None
        # Define a list of menu items with name and icon
        self.menuItems = [
            {
                "name": "Home",
                "icon": "Frontend/View/img/icon/home.png"
            },
            {
                "name": "Revenue Info",
                "icon": "Frontend/View/img/icon/revenue_chart.png"
            },
            {
                "name":"Product Sales Info",
                "icon": "Frontend/View/img/icon/productSales.png"
            },
            {
                "name": "Distribution Info",
                "icon": "Frontend/View/img/icon/distributor.png"
            },
            {
                "name": "Setting",
                "icon": "Frontend/View/img/icon/setting.png"
            },
        ]
        # Initialize the main Q
        self.init_ListWidget()
        self.connect_signal_slot()
        self.init_stackWidget()
        self.load_stylesheet()

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
            self.menuBtn.setIcon(QIcon("D:/PYTHON/py_project/App_Project1/View/img/icon/sidebar.png"))
        else:
            self.menuBtn.setIcon(QIcon("D:/PYTHON/py_project/App_Project1/View/img/icon/sidebar.png"))

    def init_stackWidget(self):
        # create content page in stackWidget
        widget_list = self.mainContent.findChildren(QWidget)

        for widgetChild in widget_list:
            self.mainContent.removeWidget(widgetChild)

        try:
            for menu in self.menuItems:
                text = menu.get("name")
                newPage = QWidget()

            #Content trong trang Home
                if text == "Home":
                    general_chart = generalChart()
                    product_chart = ProductChart()
                    fig_G = general_chart.figure
                    fig_P = product_chart.figure
                    canvas_G = FigureCanvas(fig_G)
                    canvas_P = FigureCanvas(fig_P)

                    chartlayout = QGridLayout()
                    chartlayout.addWidget(canvas_G, 0, 0)
                    chartlayout.addWidget(canvas_P, 0, 1)
                    chartWidget = QWidget()
                    chartWidget.setLayout(chartlayout)

                    homeInfoLayout = QGridLayout()
                    # Thêm một số widget vào layout dưới cùng
                    infoLabel = QLabel("Statistic Information")
                    infoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    font = QFont()
                    font.setPixelSize(30)
                    infoLabel.setFont(font)
                    homeInfoLayout.addWidget(infoLabel, 0, 0, 1, 2)  # row, col, rowspan, colspan
                    # Thêm các widget thông tin khác
                    homeInfoLayout.addWidget(QLabel("Revenue total:"), 1, 0)
                    homeInfoLayout.addWidget(QLabel("29,327.00 $USD"), 1, 1)
                    homeInfoLayout.addWidget(QLabel("Best product sale:"), 2, 0)
                    homeInfoLayout.addWidget(QLabel("iPhones (amount: 9.999)"), 2, 1)
                    homeInfoLayout.addWidget(QLabel("Top 1 'branch':"), 3, 0)
                    homeInfoLayout.addWidget(QLabel("ABC (address: number 123, XYZ street,...)"), 3, 1)
                    infoWidget = QWidget()
                    infoWidget.setLayout(homeInfoLayout)

                    contentLayout = QVBoxLayout()
                    contentLayout.addWidget(infoWidget)
                    contentLayout.addWidget(chartWidget)
                    newPage.setLayout(contentLayout)

                #Content trong trang Setting
                elif text == "Setting":
                    settingLayout = QGridLayout()
                    # Thêm một số widget vào layout dưới cùng
                    settingLabel = QLabel("Account Setting")
                    settingLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    font = QFont()
                    font.setPixelSize(50)
                    settingLabel.setFont(font)
                    settingLayout.addWidget(settingLabel, 0, 0, 1, 12)  # row, col, rowspan, colspan
                    # Thêm các widget thông tin khác
                    settingLayout.addWidget(QLabel(), 1, 5)
                    nameSetting = QLabel("☺ Username:")
                    nameSetting.setObjectName("nameSetting")
                    settingLayout.addWidget(nameSetting, 2, 1)
                    settingLayout.addWidget(QLabel("Lecris Ronal Si"), 2, 5)
                    settingLayout.addWidget(QPushButton("Edit"), 2, 10)

                    settingLayout.addWidget(QLabel(), 3, 5)
                    passSetting = QLabel("⛉ Password:")
                    passSetting.setObjectName("passSetting")
                    settingLayout.addWidget(passSetting, 4, 1)
                    settingLayout.addWidget(QLabel("************"), 4, 5)
                    settingLayout.addWidget(QPushButton("Edit"), 4, 10)

                    settingLayout.addWidget(QLabel(), 5, 5)
                    birthdateSetting = QLabel("𝄜 Date birth:")
                    birthdateSetting.setObjectName("birthdateSetting")
                    settingLayout.addWidget(birthdateSetting, 6, 1)
                    settingLayout.addWidget(QLabel("99/99/9999"), 6, 5)
                    settingLayout.addWidget(QPushButton("Edit"), 6, 10)

                    settingLayout.addWidget(QLabel(), 7, 5)
                    gmailSetting = QLabel("🖂 Email:")
                    gmailSetting.setObjectName("emailSetting")
                    settingLayout.addWidget(gmailSetting, 8, 1)
                    settingLayout.addWidget(QLabel("abcdxyz1234@gmail.com"), 8, 5)
                    settingLayout.addWidget(QPushButton("Edit"), 8, 10)

                    settingLayout.addWidget(QLabel(), 9, 5)
                    phoneSetting = QLabel("✆ Phone number: ")
                    phoneSetting.setObjectName("phoneSetting")
                    settingLayout.addWidget(phoneSetting, 10, 1)
                    settingLayout.addWidget(QLabel("(08+) 905-XXX-XXX"), 10, 5)
                    settingLayout.addWidget(QPushButton("Edit"), 10, 10)

                    logoutButton = QPushButton("Log out")
                    logoutButton.setObjectName("logoutButton")
                    settingLayout.addWidget(QLabel(), 11, 5)
                    settingLayout.addWidget(QLabel(), 12, 5)
                    settingLayout.addWidget(logoutButton, 13, 5)

                    # handle cái nút logout
                    logoutButton.clicked.connect(self.handle_logout)
                    newPage.setLayout(settingLayout)
                #Content trong trang Revenue
                elif text == "Revenue Info":
                    general_chart = generalChart()
                    product_chart = ProductChart()
                    fig_G = general_chart.figure
                    fig_P = product_chart.figure
                    canvas_A = FigureCanvas(fig_G)
                    canvas_B = FigureCanvas(fig_G)
                    canvas_C = FigureCanvas(fig_G)
                    canvas_P = FigureCanvas(fig_P)

                    chartlayout = QGridLayout()
                    chartlayout.addWidget(canvas_A, 0, 0)
                    chartlayout.addWidget(canvas_B, 0, 1)
                    chartlayout.addWidget(canvas_C, 0, 2)


                    chartWidget = QWidget()
                    chartWidget.setLayout(chartlayout)

                    # edit revenue part
                    updateDataLayout = QGridLayout()
                    # Thêm một số widget vào layout edit
                    editRevenueLabel = QLabel("Edit Revenue Info")
                    editRevenueLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    editRevenueLabel.setObjectName("editRevenueLabel")
                    updateDataLayout.addWidget(editRevenueLabel, 0, 0, 1, 2)  # row, col, rowspan, colspan
                    # Thêm các widget thông tin khác
                    updateDataLayout.addWidget(QLabel("Branch ID:"), 1, 0)
                    updateDataLayout.addWidget(QLineEdit(), 1, 2)
                    updateDataLayout.addWidget(QPushButton("Edit"), 1, 3)
                    updateDataLayout.addWidget(QLabel("Branch's name:"), 2, 0)
                    updateDataLayout.addWidget(QLineEdit(), 2, 2)
                    updateDataLayout.addWidget(QPushButton("Edit"), 2, 3)
                    updateDataLayout.addWidget(QLabel("Revenue date:"), 3, 0)
                    updateDataLayout.addWidget(QLineEdit(), 3, 2)
                    updateDataLayout.addWidget(QPushButton("Edit"), 3, 3)
                    updateDataLayout.addWidget(QLabel("New revenue total :"), 4, 0)
                    updateDataLayout.addWidget(QLineEdit(), 4, 2)
                    updateDataLayout.addWidget(QPushButton("Edit"), 4, 3)

                    updateDataWidget = QWidget()
                    updateDataWidget.setLayout(updateDataLayout)

                    contentLayout = QVBoxLayout()
                    contentLayout.addWidget(chartWidget)
                    contentLayout.addWidget(updateDataWidget)
                    newPage.setLayout(contentLayout)
                elif text == 'Product Sales Info':
                    general_chart = generalChart()
                    product_chart = ProductChart()
                    fig_G = general_chart.figure
                    fig_P = product_chart.figure
                    canvas_A = FigureCanvas(fig_P)
                    canvas_B = FigureCanvas(fig_P)
                    canvas_C = FigureCanvas(fig_P)

                    productSaleslayout = QGridLayout()
                    productSaleslayout.addWidget(canvas_A, 0, 0)
                    productSaleslayout.addWidget(canvas_B, 0, 1)
                    productSaleslayout.addWidget(canvas_C, 0, 2)

                    chartProductWidget = QWidget()
                    chartProductWidget.setLayout(productSaleslayout)

                    # update revenue part
                    updateDataLayout = QGridLayout()
                    # Thêm một số widget vào layout update
                    update_ProductSaleLabel = QLabel("Product Sales Info")
                    update_ProductSaleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    update_ProductSaleLabel.setObjectName("update_ProductSaleLabel")
                    updateDataLayout.addWidget(update_ProductSaleLabel, 0, 0, 1, 2)  # row, col, rowspan, colspan
                    # Thêm các widget thông tin khác
                    updateDataLayout.addWidget(QLabel("Sale ID:"), 1, 0)
                    updateDataLayout.addWidget(QLineEdit(), 1, 2)
                    updateDataLayout.addWidget(QPushButton("Edit"), 1, 3)
                    updateDataLayout.addWidget(QLabel("Sale date:"), 2, 0)
                    updateDataLayout.addWidget(QLineEdit(), 2, 2)
                    updateDataLayout.addWidget(QPushButton("Edit"), 2, 3)
                    updateDataLayout.addWidget(QLabel("Quantity sold:"), 3, 0)
                    updateDataLayout.addWidget(QLineEdit(), 3, 2)
                    updateDataLayout.addWidget(QPushButton("Edit"), 3, 3)
                    updateDataLayout.addWidget(QLabel("Sale's amount :"), 4, 0)
                    updateDataLayout.addWidget(QLineEdit(), 4, 2)
                    updateDataLayout.addWidget(QPushButton("Edit"), 4, 3)

                    updateDataWidget = QWidget()
                    updateDataWidget.setLayout(updateDataLayout)

                    contentLayout = QVBoxLayout()
                    contentLayout.addWidget(chartProductWidget)
                    contentLayout.addWidget(updateDataWidget)
                    newPage.setLayout(contentLayout)

                elif text == 'Distribution Info':
                    editProductLayout = QVBoxLayout()

                    #Phần layout của table
                    table_layout = QVBoxLayout()
                    table1 = QTableWidget()
                    table1.setColumnCount(3)
                    table1.setHorizontalHeaderLabels(['Name', 'Price', 'Amount'])
                    table_layout.addWidget(table1)

                    #Phần layout của crud
                    form_layout = QFormLayout()
                    name_input = QLineEdit()
                    price_input = QLineEdit()
                    amount_input = QLineEdit()
                    form_layout.addRow("Name:", name_input)
                    form_layout.addRow("Price:", price_input)
                    form_layout.addRow("Amount:", amount_input)

                    add_button = QPushButton("Add")
                    edit_button = QPushButton("Update")
                    remove_button = QPushButton("Remove")

                    form_layout.addRow(add_button)
                    form_layout.addRow(edit_button)
                    form_layout.addRow(remove_button)

                    editProductLayout.addLayout(table_layout)
                    editProductLayout.addLayout(form_layout)

                    newPage.setLayout(editProductLayout)

                else:
                    layout = QGridLayout()
                    label = QLabel(text=text)
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    font = QFont()
                    font.setPixelSize(20)
                    label.setFont(font)
                    layout.addWidget(label, 0, 0)
                    newPage.setLayout(layout)

                self.mainContent.addWidget(newPage)


        except Exception as e:
            import traceback
            print(f"Error:{e}")
            print(traceback.format_exc())

    def handle_logout(self):
        if self.switch_to_signUp:
            self.switch_to_signUp()

    def load_stylesheet(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        css_path = os.path.join(script_dir, 'mainDashboard.css')

        try:
            with open(css_path, 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Error: CSS file not found at {css_path}")
        except Exception as e:
            print(f"Error loading stylesheet: {e}")
