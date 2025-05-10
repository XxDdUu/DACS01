import os
import sys

from PyQt6.QtWidgets import QScrollArea, QPushButton, QLineEdit, QTableWidget, QFormLayout, QHBoxLayout, \
    QTableWidgetItem
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
        self.setWindowIcon(QIcon("Frontend/View/img/logo/dark_pythonLogo.png"))

        # Initialize UI elements
        self.titleLabel = self.ui.title_label
        self.titleLabel.setText("PyMe")

        self.titleLogo = self.ui.iconTitle_label
        self.titleLogo.setText("")
        self.titleLogo.setPixmap(QPixmap("Frontend/View/img/logo/dark_pythonLogo.png"))
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
        self.menuBtn.setIcon(QIcon("Frontend/View/img/icon/sidebar.png"))
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
            self.menuBtn.setIcon(QIcon("Frontend/View/img/icon/sidebar.png"))
        else:
            self.menuBtn.setIcon(QIcon("Frontend/View/img/icon/sidebar.png"))

    def init_stackWidget(self):
        # create content page in stackWidget
        widget_list = self.mainContent.findChildren(QWidget)

        for widgetChild in widget_list:
            self.mainContent.removeWidget(widgetChild)

        try:
            for menu in self.menuItems:
                text = menu.get("name")
                newPage = QWidget()

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

                    settingLayout = QGridLayout()
                    # Thêm một số widget vào layout dưới cùng
                    infoLabel = QLabel("Statistic Information")
                    infoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    font = QFont()
                    font.setPixelSize(30)
                    infoLabel.setFont(font)
                    settingLayout.addWidget(infoLabel, 0, 0, 1, 2)  # row, col, rowspan, colspan
                    # Thêm các widget thông tin khác
                    settingLayout.addWidget(QLabel("Revenue total:"), 1, 0)
                    settingLayout.addWidget(QLabel("29,327.00 $USD"), 1, 1)
                    settingLayout.addWidget(QLabel("Best product sale:"), 2, 0)
                    settingLayout.addWidget(QLabel("iPhones (amount: 9.999)"), 2, 1)
                    settingLayout.addWidget(QLabel("Top 1 'branch':"), 3, 0)
                    settingLayout.addWidget(QLabel("ABC (address: number 123, XYZ street,...)"), 3, 1)
                    infoWidget = QWidget()
                    infoWidget.setLayout(settingLayout)

                    contentLayout = QVBoxLayout()
                    contentLayout.addWidget(infoWidget)
                    contentLayout.addWidget(chartWidget)
                    newPage.setLayout(contentLayout)
                elif text == "Revenue Info":
                    general_chart = generalChart()
                    fig_G = general_chart.figure
                    canvas_1 = FigureCanvas(fig_G)
                    canvas_2 = FigureCanvas(fig_G)
                    canvas_3 = FigureCanvas(fig_G)

                    chartRLayout = QGridLayout()
                    chartRLayout.addWidget(canvas_1,0,0)
                    chartRLayout.addWidget(canvas_2,0,1)
                    chartRLayout.addWidget(canvas_3,0,2)
                    chartRWidget = QWidget()
                    chartRWidget.setLayout(chartRLayout)

                    updateR_Layout = QGridLayout()
                    # Thêm một số widget vào layout dưới cùng
                    infoLabel = QLabel("Edit Revenue Information")
                    infoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    font = QFont()
                    font.setPixelSize(30)
                    infoLabel.setFont(font)
                    updateR_Layout.addWidget(infoLabel, 0, 0, 1, 1)  # row, col, rowspan, colspan
                    # Thêm các widget thông tin khác
                    updateR_Layout.addWidget(QLabel("Branch ID:"), 1, 0)
                    updateR_Layout.addWidget(QLineEdit(), 1, 1)
                    updateR_Layout.addWidget(QLabel("Revenue Date:"), 2, 0)
                    updateR_Layout.addWidget(QLineEdit(), 2, 1)
                    updateR_Layout.addWidget(QLabel("Update new revenue :"), 3, 0)
                    updateR_Layout.addWidget(QLineEdit(), 3, 1)

                    updateBtn_layout = QGridLayout()
                    updateBtn_layout.addWidget(QLabel(),4,0,1,12)
                    updateBtn_layout.addWidget(QPushButton('Update'),5,7)

                    updateForm_layout = QVBoxLayout()
                    updateForm_layout.addLayout(updateR_Layout)
                    updateForm_layout.addLayout(updateBtn_layout)

                    updateR_Widget = QWidget()
                    updateR_Widget.setLayout(updateForm_layout)

                    contentLayout = QVBoxLayout()
                    contentLayout.addWidget(chartRWidget)
                    contentLayout.addWidget(updateR_Widget)
                    newPage.setLayout(contentLayout)

                elif text == "Product Sales Info":
                    PS_chart = ProductChart()
                    fig_PS = PS_chart.figure
                    canvas_4 = FigureCanvas(fig_PS)
                    canvas_5 = FigureCanvas(fig_PS)
                    canvas_6 = FigureCanvas(fig_PS)

                    chartPSLayout = QGridLayout()
                    chartPSLayout.addWidget(canvas_4, 0, 0)
                    chartPSLayout.addWidget(canvas_5, 0, 1)
                    chartPSLayout.addWidget(canvas_6, 0, 2)
                    chartPSWidget = QWidget()
                    chartPSWidget.setLayout(chartPSLayout)

                    updatePS_Layout = QGridLayout()
                    # Thêm một số widget vào layout dưới cùng
                    infoPSLabel = QLabel("Edit Revenue Information")
                    infoPSLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    font = QFont()
                    font.setPixelSize(30)
                    infoPSLabel.setFont(font)
                    updatePS_Layout.addWidget(infoPSLabel, 0, 0, 1, 1)  # row, col, rowspan, colspan
                    # Thêm các widget thông tin khác
                    updatePS_Layout.addWidget(QLabel("Branch ID:"), 1, 0)
                    updatePS_Layout.addWidget(QLineEdit(), 1, 1)
                    updatePS_Layout.addWidget(QLabel("Revenue Date:"), 2, 0)
                    updatePS_Layout.addWidget(QLineEdit(), 2, 1)
                    updatePS_Layout.addWidget(QLabel("Update new revenue :"), 3, 0)
                    updatePS_Layout.addWidget(QLineEdit(), 3, 1)

                    updateBtn_layout = QGridLayout()
                    updateBtn_layout.addWidget(QLabel(), 4, 0, 1, 12)
                    updateBtn_layout.addWidget(QPushButton('Update'), 5, 7)

                    updateForm_layout = QVBoxLayout()
                    updateForm_layout.addLayout(updatePS_Layout)
                    updateForm_layout.addLayout(updateBtn_layout)

                    updatePS_Widget = QWidget()
                    updatePS_Widget.setLayout(updateForm_layout)

                    contentLayout = QVBoxLayout()
                    contentLayout.addWidget(chartPSWidget)
                    contentLayout.addWidget(updatePS_Widget)
                    newPage.setLayout(contentLayout)

                elif text == "Distribution Info":
                    # Initialize two empty tables
                    table1 = QTableWidget()
                    table1.setRowCount(0)
                    table1.setColumnCount(4)
                    table1.setHorizontalHeaderLabels(["Name", "Price", "Amount", "Branch ID"])
                    table1.resizeColumnsToContents()

                    table2 = QTableWidget()
                    table2.setRowCount(0)
                    table2.setColumnCount(4)
                    table2.setHorizontalHeaderLabels(["Branch ID", "Name", "Address", "Phone Number"])
                    table2.resizeColumnsToContents()

                    # Form for Table 1
                    form1_layout = QVBoxLayout()
                    form1_label = QLabel("Manage Product Data")
                    form1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    font = QFont()
                    font.setPixelSize(20)
                    form1_label.setFont(font)
                    form1_layout.addWidget(form1_label)

                    input_layout1 = QGridLayout()
                    input_layout1.addWidget(QLabel("Name:"), 0, 0)
                    name1 = QLineEdit()
                    input_layout1.addWidget(name1, 0, 1)
                    input_layout1.addWidget(QLabel("Price:"), 1, 0)
                    price1 = QLineEdit()
                    input_layout1.addWidget(price1, 1, 1)
                    input_layout1.addWidget(QLabel("Amount:"), 2, 0)
                    amount1 = QLineEdit()
                    input_layout1.addWidget(amount1, 2, 1)
                    input_layout1.addWidget(QLabel("Branch ID:"), 3, 0)
                    branch_id1 = QLineEdit()
                    input_layout1.addWidget(branch_id1, 3, 1)
                    form1_layout.addLayout(input_layout1)

                    # Horizontal button layout for Table 1
                    button_layout1 = QHBoxLayout()
                    button_layout1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    add_btn1 = QPushButton("Add")
                    add_btn1.setFixedSize(80, 30)
                    remove_btn1 = QPushButton("Remove")
                    remove_btn1.setFixedSize(80, 30)
                    update_btn1 = QPushButton("Update")
                    update_btn1.setFixedSize(80, 30)
                    button_layout1.addWidget(add_btn1)
                    button_layout1.addWidget(remove_btn1)
                    button_layout1.addWidget(update_btn1)
                    button_widget1 = QWidget()
                    button_widget1.setLayout(button_layout1)
                    form1_layout.addWidget(button_widget1)
                    form1_layout.addStretch()
                    form1_widget = QWidget()
                    form1_widget.setLayout(form1_layout)

                    # Form for Table 2
                    form2_layout = QVBoxLayout()
                    form2_label = QLabel("Manage Branches Info")
                    form2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    form2_label.setFont(font)
                    form2_layout.addWidget(form2_label)

                    input_layout2 = QGridLayout()
                    input_layout2.addWidget(QLabel("Branch ID:"), 0, 0)
                    branch_id2 = QLineEdit()
                    input_layout2.addWidget(branch_id2, 0, 1)
                    input_layout2.addWidget(QLabel("Name:"), 1, 0)
                    name2 = QLineEdit()
                    input_layout2.addWidget(name2, 1, 1)
                    input_layout2.addWidget(QLabel("Address:"), 2, 0)
                    address2 = QLineEdit()
                    input_layout2.addWidget(address2, 2, 1)
                    input_layout2.addWidget(QLabel("Phone Number:"), 3, 0)
                    phone_number2 = QLineEdit()
                    input_layout2.addWidget(phone_number2, 3, 1)
                    form2_layout.addLayout(input_layout2)

                    # BFD viết tắt BranchesFormData
                    self.BFD = BranchesFormData(branch_id2,name2,address2,phone_number2)
                    #PFD viet tat ProductFormData
                    self.PFD = ProductFormData(name1,price1,amount1,branch_id1)

                    # Horizontal button layout for Table 2
                    button_layout2 = QHBoxLayout()
                    button_layout2.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.add_btn2 = QPushButton("Add")
                    self.add_btn2.setFixedSize(80, 30)
                    self.remove_btn2 = QPushButton("Remove")
                    self.remove_btn2.setFixedSize(80, 30)
                    self.update_btn2 = QPushButton("Update")
                    self.update_btn2.setFixedSize(80, 30)
                    button_layout2.addWidget(self.add_btn2)
                    button_layout2.addWidget(self.remove_btn2)
                    button_layout2.addWidget(self.update_btn2 )
                    button_widget2 = QWidget()
                    button_widget2.setLayout(button_layout2)
                    form2_layout.addWidget(button_widget2)
                    form2_layout.addStretch()
                    form2_widget = QWidget()
                    form2_widget.setLayout(form2_layout)

                    # Slot methods for Table 1
                    def add_row_table1():
                        row_count = table1.rowCount()
                        table1.insertRow(row_count)
                        table1.setItem(row_count, 0, QTableWidgetItem(name1.text()))
                        table1.setItem(row_count, 1, QTableWidgetItem(price1.text()))
                        table1.setItem(row_count, 2, QTableWidgetItem(amount1.text()))
                        table1.setItem(row_count, 3, QTableWidgetItem(branch_id1.text()))
                        name1.clear()
                        price1.clear()
                        amount1.clear()
                        branch_id1.clear()

                    def remove_row_table1():
                        current_row = table1.currentRow()
                        if current_row >= 0:
                            table1.removeRow(current_row)

                    def update_row_table1():
                        current_row = table1.currentRow()
                        if current_row >= 0:
                            table1.setItem(current_row, 0, QTableWidgetItem(name1.text()))
                            table1.setItem(current_row, 1, QTableWidgetItem(price1.text()))
                            table1.setItem(current_row, 2, QTableWidgetItem(amount1.text()))
                            table1.setItem(current_row, 3, QTableWidgetItem(branch_id1.text()))
                            name1.clear()
                            price1.clear()
                            amount1.clear()
                            branch_id1.clear()

                    # Slot methods for Table 2
                    def add_row_table2():
                        row_count = table2.rowCount()
                        table2.insertRow(row_count)
                        table2.setItem(row_count, 0, QTableWidgetItem(branch_id2.text()))
                        table2.setItem(row_count, 1, QTableWidgetItem(name2.text()))
                        table2.setItem(row_count, 2, QTableWidgetItem(address2.text()))
                        table2.setItem(row_count, 3, QTableWidgetItem(phone_number2.text()))
                        branch_id2.clear()
                        name2.clear()
                        address2.clear()
                        phone_number2.clear()

                    def remove_row_table2():
                        current_row = table2.currentRow()
                        if current_row >= 0:
                            table2.removeRow(current_row)

                    def update_row_table2():
                        current_row = table2.currentRow()
                        if current_row >= 0:
                            table2.setItem(current_row, 0, QTableWidgetItem(branch_id2.text()))
                            table2.setItem(current_row, 1, QTableWidgetItem(name2.text()))
                            table2.setItem(current_row, 2, QTableWidgetItem(address2.text()))
                            table2.setItem(current_row, 3, QTableWidgetItem(phone_number2.text()))
                            branch_id2.clear()
                            name2.clear()
                            address2.clear()
                            phone_number2.clear()

                    # Connect buttons to slots
                    add_btn1.clicked.connect(add_row_table1)
                    remove_btn1.clicked.connect(remove_row_table1)
                    update_btn1.clicked.connect(update_row_table1)
                    self.add_btn2.clicked.connect(add_row_table2)
                    self.remove_btn2.clicked.connect(remove_row_table2)
                    self.update_btn2.clicked.connect(update_row_table2)

                    # Layout for tables and forms
                    content_layout = QHBoxLayout()
                    table1_layout = QVBoxLayout()
                    table1_layout.addWidget(QLabel("Product Data"))
                    table1_layout.addWidget(table1)
                    table1_layout.addWidget(form1_widget)
                    table2_layout = QVBoxLayout()
                    table2_layout.addWidget(QLabel("Branches Info"))
                    table2_layout.addWidget(table2)
                    table2_layout.addWidget(form2_widget)
                    content_layout.addLayout(table1_layout)
                    content_layout.addLayout(table2_layout)
                    newPage.setLayout(content_layout)

                elif text == "Setting":
                    settingLayout = QGridLayout()
                    # Thêm một số widget vào layout dưới cùng
                    infoLabel = QLabel("Account Setting")
                    infoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    font = QFont()
                    font.setPixelSize(50)
                    infoLabel.setFont(font)
                    settingLayout.addWidget(infoLabel, 0, 0, 1, 12)  # row, col, rowspan, colspan
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


class BranchesFormData:
    def __init__(self, Id, name, address, phone_num):
        self.Id = Id
        self.name = name
        self.address = address
        self.phone_num = phone_num

    def get_branchesForm_data(self):
        return {
            "id": self.Id.text().strip(),
            "name": self.name.text().strip(),
            "address": self.address.text().strip(),
            "phone_number": self.phone_num.text().strip()
        }

class ProductFormData:
    def __init__(self, name, price, amount, branch_Id):
        self.name = name
        self.price = price
        self.amount = amount
        self.branch_Id = branch_Id

    def get_ProductForm_data(self):
        return {
            "name": self.name.text().strip(),
            "price": self.price.text().strip(),
            "amount": self.amount.text().strip(),
            "branch_id": self.branch_Id.text().strip()
        }