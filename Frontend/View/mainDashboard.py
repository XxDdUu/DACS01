import os
import sys

from PyQt6.QtWidgets import QScrollArea, QPushButton, QLineEdit, QDateEdit, QTableWidget, QFormLayout, QHBoxLayout, \
    QTableWidgetItem
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QSizePolicy
from PyQt6.QtWidgets import (QMainWindow, QApplication,
                             QLabel, QListWidgetItem, QWidget)
from PyQt6.QtCore import Qt, QSize, QDate
from PyQt6.QtGui import QPixmap, QFont, QIcon

# from Backend.Model.ProductSales import ProductSalesFormData
from Backend.Model.Revenue import RevenueFormData
from Frontend.Chart.Branch_PSChart import PSBranchChart
from Frontend.Chart.PSGeneralChart import ProductSaleChart
from Frontend.Chart.RevenueGeneralChart import generalChart
from Frontend.View.frameUI import Ui_MainWindow
from Backend.Model.Employer import Employer
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class MainDashboard(QMainWindow):

    def __init__(self, employer_data: Employer, controller):
        super().__init__()
        self.employer_data = employer_data # truyền model
        self.controller = controller
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
        print(">>> init_stackWidget called")
        widget_list = self.mainContent.findChildren(QWidget)

        for widgetChild in widget_list:
            self.mainContent.removeWidget(widgetChild)

        try:
            for menu in self.menuItems:
                text = menu.get("name")
                newPage = QWidget()

                if text == "Home":
                    general_chart = generalChart()
                    product_chart = ProductSaleChart()
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
                    infoHomeLabel = QLabel("Statistic Information")
                    infoHomeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    font = QFont()
                    font.setPixelSize(30)
                    infoHomeLabel.setFont(font)
                    settingLayout.addWidget(infoHomeLabel, 0, 0, 1, 2)  # row, col, rowspan, colspan
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
                    # Khởi tạo biểu đồ tổng quan
                    general_chart = generalChart()
                    fig_general_chart = general_chart.figure

                    canvas_chart_1 = FigureCanvas(fig_general_chart)
                    # canvas_chart_2 = FigureCanvas(fig_general_chart)
                    # canvas_chart_3 = FigureCanvas(fig_general_chart)

                    # Layout chứa 3 biểu đồ
                    chart_layout = QGridLayout()
                    chart_layout.addWidget(canvas_chart_1, 0, 0)
                    # chart_layout.addWidget(canvas_chart_2, 0, 1)
                    # chart_layout.addWidget(canvas_chart_3, 0, 2)

                    chart_widget = QWidget()
                    chart_widget.setLayout(chart_layout)

                    # Layout cập nhật thông tin doanh thu
                    revenue_form_layout = QGridLayout()

                    # Tiêu đề
                    lbl_form_title = QLabel("Edit Revenue Information")
                    lbl_form_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    font = QFont()
                    font.setPixelSize(30)
                    lbl_form_title.setFont(font)
                    revenue_form_layout.addWidget(lbl_form_title, 0, 0, 1, 2)

                    # Branch ID
                    lbl_revenue_id = QLabel("Revenue ID:")
                    self.le_revenue_id = QLineEdit()
                    revenue_form_layout.addWidget(lbl_revenue_id, 1, 0)
                    revenue_form_layout.addWidget(self.le_revenue_id, 1, 1)

                    # Revenue Date
                    lbl_sale_date = QLabel("Revenue Date:")
                    self.le_revenue_date = QDateEdit()
                    revenue_form_layout.addWidget(lbl_sale_date, 2, 0)
                    revenue_form_layout.addWidget(self.le_revenue_date, 2, 1)

                    #Revenue Amount
                    lbl_revenueAmount = QLabel("Revneue Amount:")
                    self.le_revenueAmount = QLineEdit()
                    revenue_form_layout.addWidget(lbl_revenueAmount, 3, 0)
                    revenue_form_layout.addWidget(self.le_revenueAmount, 3, 1)

                    #Branch Id _revenue_
                    lbl_rev_branchId = QLabel("Branch ID:")
                    self.le_rev_branchId = QLineEdit()
                    revenue_form_layout.addWidget(lbl_rev_branchId, 4, 0)
                    revenue_form_layout.addWidget(self.le_rev_branchId, 4, 1)

                    #RFD stand for Revenue Form Data, truyền vào Controller
                    self.RFD = RevenueFormData(
                        self.le_revenue_id,
                        self.le_revenue_date,
                        self.le_revenueAmount,
                        self.le_rev_branchId
                    )

                    # Các nút CRUD
                    self.btn_add_Revenue = QPushButton("Add")
                    self.btn_update_Revenue = QPushButton("Update")
                    self.btn_remove_Revenue = QPushButton("Remove")

                    crud_button_layout = QHBoxLayout()
                    crud_button_layout.addStretch(1)
                    crud_button_layout.addWidget(self.btn_add_Revenue)
                    crud_button_layout.addStretch(0)
                    crud_button_layout.addWidget(self.btn_update_Revenue)
                    crud_button_layout.addStretch(0)
                    crud_button_layout.addWidget(self.btn_remove_Revenue)
                    crud_button_layout.addStretch(1)

                    # Tổng hợp layout
                    form_container_layout = QVBoxLayout()
                    form_container_layout.addLayout(revenue_form_layout)
                    form_container_layout.addLayout(crud_button_layout)

                    form_widget = QWidget()
                    form_widget.setLayout(form_container_layout)

                    # Layout tổng thể
                    main_layout = QVBoxLayout()
                    main_layout.addWidget(chart_widget)
                    main_layout.addWidget(form_widget)

                    newPage.setLayout(main_layout)


                elif text == "Product Sales Info":
                    # Khởi tạo biểu đồ doanh thu sản phẩm theo từng chi nhánh(name: A,B,C)
                    chartA = PSBranchChart("A")
                    chartB = PSBranchChart("B")
                    chartC = PSBranchChart("C")

                    fig_PS_branchA_chart = chartA.figure
                    fig_PS_branchB_chart = chartB.figure
                    fig_PS_branchC_chart = chartC.figure

                    canvas_chart_left = FigureCanvas(fig_PS_branchA_chart)
                    canvas_chart_center = FigureCanvas(fig_PS_branchB_chart)
                    canvas_chart_right = FigureCanvas(fig_PS_branchC_chart)

                    # Layout cho biểu đồ
                    chart_layout = QGridLayout()
                    chart_layout.addWidget(canvas_chart_left, 0, 0)
                    chart_layout.addWidget(canvas_chart_center, 0, 1)
                    chart_layout.addWidget(canvas_chart_right, 0, 2)

                    chart_widget = QWidget()
                    chart_widget.setLayout(chart_layout)

                    # Layout cập nhật thông tin doanh số bán sản phẩm
                    update_PS_layout = QGridLayout()

                    # Tiêu đề
                    lbl_PS_title = QLabel("Manage Product Sales")
                    lbl_PS_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    font = QFont()
                    font.setPixelSize(30)
                    lbl_PS_title.setFont(font)
                    update_PS_layout.addWidget(lbl_PS_title, 0, 0, 1, 2)

                    # Sale ID
                    lbl_saleID = QLabel("Sale ID:")
                    self.le_saleID = QLineEdit()
                    update_PS_layout.addWidget(lbl_saleID, 1, 0)
                    update_PS_layout.addWidget(self.le_saleID, 1, 1)

                    # PS Date
                    lbl_sale_date = QLabel("Sale Date:")
                    self.le_sale_date = QDateEdit()
                    update_PS_layout.addWidget(lbl_sale_date, 2, 0)
                    update_PS_layout.addWidget(self.le_sale_date, 2, 1)

                    # Sale Quantity
                    lbl_quantitySold = QLabel("Quantity Sold:")
                    self.le_quantitySold = QLineEdit()
                    update_PS_layout.addWidget(lbl_quantitySold, 3, 0)
                    update_PS_layout.addWidget(self.le_quantitySold, 3, 1)

                    # Sale amount
                    lbl_saleAmount = QLabel("Sale Amount:")
                    self.le_saleAmount = QLineEdit()
                    update_PS_layout.addWidget(lbl_saleAmount, 4, 0)
                    update_PS_layout.addWidget(self.le_saleAmount, 4, 1)

                    lbl_PS_productId = QLabel("Product ID:")
                    self.le_PS_productId = QLineEdit()
                    update_PS_layout.addWidget(lbl_PS_productId, 5, 0)
                    update_PS_layout.addWidget(self.le_PS_productId, 5, 1)

                    lbl_PS_branchId = QLabel("Branch ID:")
                    self.le_PS_branchId = QLineEdit()
                    update_PS_layout.addWidget(lbl_PS_branchId, 6, 0)
                    update_PS_layout.addWidget(self.le_PS_branchId, 6, 1)

                    # self.PSFD = ProductSalesFormData(
                    #     self.le_saleID,
                    #     self.le_PS_productId,
                    #     self.le_PS_branchId,
                    #     self.le_sale_date,
                    #     self.le_quantitySold,
                    #     self.le_saleAmount
                    # )

                    # Các nút CRUD
                    self.btn_add_PS = QPushButton("Add")
                    self.btn_update_PS = QPushButton("Update")
                    self.btn_remove_PS = QPushButton("Remove")

                    crud_btn_layout = QHBoxLayout()
                    crud_btn_layout.addStretch(1)
                    crud_btn_layout.addWidget(self.btn_add_PS)
                    crud_btn_layout.addStretch(0)
                    crud_btn_layout.addWidget(self.btn_update_PS)
                    crud_btn_layout.addStretch(0)
                    crud_btn_layout.addWidget(self.btn_remove_PS)
                    crud_btn_layout.addStretch(1)

                    # Tổng hợp layout form
                    form_revenue_layout = QVBoxLayout()
                    form_revenue_layout.addLayout(update_PS_layout)
                    form_revenue_layout.addLayout(crud_btn_layout)

                    form_revenue_widget = QWidget()
                    form_revenue_widget.setLayout(form_revenue_layout)

                    # Layout cuối cùng
                    content_layout = QVBoxLayout()
                    content_layout.addWidget(chart_widget)
                    content_layout.addWidget(form_revenue_widget)

                    newPage.setLayout(content_layout)


                elif text == "Distribution Info":
                    # Initialize two empty tables
                    prod_table = QTableWidget()
                    prod_table.setRowCount(0)
                    prod_table.setColumnCount(4)
                    prod_table.setHorizontalHeaderLabels(["Name", "Price", "Amount", "Branch ID"])
                    prod_table.resizeColumnsToContents()

                    branch_table = self.load_branches()

                    # Form for Product Table
                    prod_form_layout = QVBoxLayout()
                    prod_title = QLabel("Manage Product Data")
                    prod_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    font = QFont()
                    font.setPixelSize(20)
                    prod_title.setFont(font)
                    prod_form_layout.addWidget(prod_title)

                    prod_input_layout = QGridLayout()
                    prod_input_layout.addWidget(QLabel("Product ID:"), 0, 0)
                    self.prod_id_input = QLineEdit()
                    prod_input_layout.addWidget(self.prod_id_input, 0, 1)
                    prod_form_layout.addLayout(prod_input_layout)
                    prod_input_layout.addWidget(QLabel("Name:"), 1, 0)
                    self.prod_name_input = QLineEdit()
                    prod_input_layout.addWidget(self.prod_name_input, 1, 1)
                    prod_input_layout.addWidget(QLabel("Price:"), 2, 0)
                    self.prod_price_input = QLineEdit()
                    prod_input_layout.addWidget(self.prod_price_input, 2, 1)
                    prod_input_layout.addWidget(QLabel("Amount:"), 3, 0)
                    self.prod_amount_input = QLineEdit()
                    prod_input_layout.addWidget(self.prod_amount_input, 3, 1)
                    prod_input_layout.addWidget(QLabel("Branch ID:"), 4, 0)
                    self.prod_branch_id_input = QLineEdit()
                    prod_input_layout.addWidget(self.prod_branch_id_input, 4, 1)
                    prod_form_layout.addLayout(prod_input_layout)

                    # Horizontal button layout for Product
                    prod_button_layout = QHBoxLayout()
                    prod_button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.prod_add_btn = QPushButton("Add")
                    self.prod_add_btn.setFixedSize(80, 30)
                    self.prod_remove_btn = QPushButton("Remove")
                    self.prod_remove_btn.setFixedSize(80, 30)
                    self.prod_update_btn = QPushButton("Update")
                    self.prod_update_btn.setFixedSize(80, 30)
                    prod_button_layout.addWidget(self.prod_add_btn)
                    prod_button_layout.addWidget(self.prod_remove_btn)
                    prod_button_layout.addWidget(self.prod_update_btn)
                    prod_button_widget = QWidget()
                    prod_button_widget.setLayout(prod_button_layout)
                    prod_form_layout.addWidget(prod_button_widget)
                    prod_form_layout.addStretch()
                    prod_form_widget = QWidget()
                    prod_form_widget.setLayout(prod_form_layout)

                    # Form for Branch Table
                    branch_form_layout = QVBoxLayout()
                    branch_title = QLabel("Manage Branches Info")
                    branch_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    branch_title.setFont(font)
                    branch_form_layout.addWidget(branch_title)

                    branch_input_layout = QGridLayout()
                    branch_input_layout.addWidget(QLabel("Branch ID:"), 0, 0)
                    self.branch_id_input = QLineEdit()
                    branch_input_layout.addWidget(self.branch_id_input, 0, 1)
                    branch_input_layout.addWidget(QLabel("Name:"), 1, 0)
                    self.branch_name_input = QLineEdit()
                    branch_input_layout.addWidget(self.branch_name_input, 1, 1)
                    branch_input_layout.addWidget(QLabel("Address:"), 2, 0)
                    self.branch_address_input = QLineEdit()
                    branch_input_layout.addWidget(self.branch_address_input, 2, 1)
                    branch_input_layout.addWidget(QLabel("Phone Number:"), 3, 0)
                    self.branch_phone_input = QLineEdit()
                    branch_input_layout.addWidget(self.branch_phone_input, 3, 1)
                    branch_form_layout.addLayout(branch_input_layout)

                    # Branch and Product Form Data
                    # self.BFD = BranchesFormData(self.branch_id_input,branch_name_input, branch_address_input,
                    #                                          branch_phone_input)
                    # self.PFD = ProductFormData(prod_id_input,prod_name_input, prod_price_input, prod_amount_input,
                    #                                       prod_branch_id_input)

                    # Horizontal button layout for Branch
                    branch_button_layout = QHBoxLayout()
                    branch_button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.branch_add_btn = QPushButton("Add")
                    self.branch_add_btn.setFixedSize(80, 30)
                    self.branch_remove_btn = QPushButton("Remove")
                    self.branch_remove_btn.setFixedSize(80, 30)
                    self.branch_update_btn = QPushButton("Update")
                    self.branch_update_btn.setFixedSize(80, 30)
                    branch_button_layout.addWidget(self.branch_add_btn)
                    branch_button_layout.addWidget(self.branch_remove_btn)
                    branch_button_layout.addWidget(self.branch_update_btn)
                    branch_button_widget = QWidget()
                    branch_button_widget.setLayout(branch_button_layout)
                    branch_form_layout.addWidget(branch_button_widget)
                    branch_form_layout.addStretch()
                    branch_form_widget = QWidget()
                    branch_form_widget.setLayout(branch_form_layout)

                    # Slot methods for Product Table
                    def add_row_prod():
                        row = prod_table.rowCount()
                        prod_table.insertRow(row)
                        prod_table.setItem(row, 0, QTableWidgetItem(self.prod_name_input.text()))
                        prod_table.setItem(row, 1, QTableWidgetItem(self.prod_price_input.text()))
                        prod_table.setItem(row, 2, QTableWidgetItem(self.prod_amount_input.text()))
                        prod_table.setItem(row, 3, QTableWidgetItem(self.prod_branch_id_input.text()))

                    def remove_row_prod():
                        row = prod_table.currentRow()
                        if row >= 0:
                            prod_table.removeRow(row)

                    def update_row_prod():
                        row = prod_table.currentRow()
                        if row >= 0:
                            prod_table.setItem(row, 0, QTableWidgetItem(self.prod_name_input.text()))
                            prod_table.setItem(row, 1, QTableWidgetItem(self.prod_price_input.text()))
                            prod_table.setItem(row, 2, QTableWidgetItem(self.prod_amount_input.text()))
                            prod_table.setItem(row, 3, QTableWidgetItem(self.prod_branch_id_input.text()))
                            # prod_name_input.clear()
                            # prod_price_input.clear()
                            # prod_amount_input.clear()
                            # prod_branch_id_input.clear()

                    # Slot methods for Branch Table
                    def add_row_branch():
                        row = branch_table.rowCount()
                        branch_table.insertRow(row)
                        branch_table.setItem(row, 0, QTableWidgetItem(self.branch_id_input.text()))
                        branch_table.setItem(row, 1, QTableWidgetItem(self.branch_name_input.text()))
                        branch_table.setItem(row, 2, QTableWidgetItem(self.branch_address_input.text()))
                        branch_table.setItem(row, 3, QTableWidgetItem(self.branch_phone_input.text()))

                    def remove_row_branch():
                        row = branch_table.currentRow()
                        if row >= 0:
                            branch_table.removeRow(row)

                    def update_row_branch():
                        row = branch_table.currentRow()
                        if row >= 0:
                            branch_table.setItem(row, 0, QTableWidgetItem(self.branch_id_input.text()))
                            branch_table.setItem(row, 1, QTableWidgetItem(self.branch_name_input.text()))
                            branch_table.setItem(row, 2, QTableWidgetItem(self.branch_address_input.text()))
                            branch_table.setItem(row, 3, QTableWidgetItem(self.branch_phone_input.text()))
                            self.branch_id_input.clear()
                            self.branch_name_input.clear()
                            self.branch_address_input.clear()
                            self.branch_phone_input.clear()
                    # Connect buttons to slots
                    self.prod_add_btn.clicked.connect(add_row_prod)
                    self.prod_remove_btn.clicked.connect(remove_row_prod)
                    self.prod_update_btn.clicked.connect(update_row_prod)
                    self.branch_add_btn.clicked.connect(add_row_branch)
                    self.branch_remove_btn.clicked.connect(remove_row_branch)
                    self.branch_update_btn.clicked.connect(update_row_branch)

                    # Layout for tables and forms
                    content_layout = QHBoxLayout()
                    prod_layout = QVBoxLayout()
                    prod_layout.addWidget(QLabel("Product Data"))
                    prod_layout.addWidget(prod_table)
                    prod_layout.addWidget(prod_form_widget)

                    branch_layout = QVBoxLayout()
                    branch_layout.addWidget(QLabel("Branches Info"))
                    branch_layout.addWidget(branch_table)
                    branch_layout.addWidget(branch_form_widget)

                    content_layout.addLayout(prod_layout)
                    content_layout.addLayout(branch_layout)
                    newPage.setLayout(content_layout)


                elif text == "Setting":
                    settingLayout = QGridLayout()

                    # Tiêu đề
                    infoLabel = QLabel("Account Setting")
                    infoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    font = QFont()
                    font.setPixelSize(50)
                    infoLabel.setFont(font)
                    settingLayout.addWidget(infoLabel, 0, 0, 1, 12)

                    # Spacer hàng 1
                    settingLayout.addWidget(QLabel(), 1, 5)

                    # Username
                    lbl_username = QLabel("☺ Username:")
                    lbl_username.setObjectName("nameSetting")
                    self.le_username = QLineEdit(self.employer_data.username)
                    self.btn_edit_username = QPushButton("Edit")
                    settingLayout.addWidget(lbl_username, 2, 1)
                    settingLayout.addWidget(self.le_username, 2, 5)
                    settingLayout.addWidget(self.btn_edit_username, 2, 10)

                    # Spacer hàng 3
                    settingLayout.addWidget(QLabel(), 3, 5)

                    # Enterprise_ID
                    lbl_enterprise_id = QLabel("Enterprise_ID:")
                    lbl_enterprise_id.setObjectName("enterpriseSetting")
                    self.le_enterprise_id = QLineEdit(self.employer_data.enterprise_id)
                    self.btn_view_enterprise_data = QPushButton("Get")
                    settingLayout.addWidget(lbl_enterprise_id, 4, 1)
                    settingLayout.addWidget(self.le_enterprise_id, 4, 5)
                    settingLayout.addWidget(self.btn_view_enterprise_data, 4, 10)

                    # Spacer hàng 5
                    settingLayout.addWidget(QLabel(), 5, 5)

                    # Birthdate
                    birthdate = self.employer_data.date_of_birth
                    qbirthdate = QDate(birthdate.year, birthdate.month, birthdate.day)

                    lbl_birthdate = QLabel("𝄜 Date birth:")
                    lbl_birthdate.setObjectName("birthdateSetting")
                    self.le_birthdate = QDateEdit(qbirthdate)
                    # Set format of qdateedit
                    self.le_birthdate.setDisplayFormat("dd-MM-yyyy")
                    self.btn_edit_birthdate = QPushButton("Edit")
                    settingLayout.addWidget(lbl_birthdate, 6, 1)
                    settingLayout.addWidget(self.le_birthdate, 6, 5)
                    settingLayout.addWidget(self.btn_edit_birthdate, 6, 10)

                    # Spacer hàng 7
                    settingLayout.addWidget(QLabel(), 7, 5)

                    # Email
                    lbl_email = QLabel("🖂 Email:")
                    lbl_email.setObjectName("emailSetting")
                    self.le_email = QLineEdit(self.employer_data.email)
                    self.btn_edit_email = QPushButton("Edit")
                    settingLayout.addWidget(lbl_email, 8, 1)
                    settingLayout.addWidget(self.le_email, 8, 5)
                    settingLayout.addWidget(self.btn_edit_email, 8, 10)

                    # Spacer hàng 9
                    settingLayout.addWidget(QLabel(), 9, 5)

                    # Phone Number
                    lbl_phone = QLabel("✆ Phone number:")
                    lbl_phone.setObjectName("phoneSetting")
                    self.le_phone = QLineEdit(self.employer_data.phone_number)
                    self.btn_edit_phone = QPushButton("Edit")
                    settingLayout.addWidget(lbl_phone, 10, 1)
                    settingLayout.addWidget(self.le_phone, 10, 5)
                    settingLayout.addWidget(self.btn_edit_phone, 10, 10)

                    # Logout Button
                    logoutButtonLayout = QGridLayout()
                    logoutButton = QPushButton("Log out")
                    logoutButton.setObjectName("logoutButton")
                    #Spacer
                    logoutButtonLayout.addWidget(QLabel(), 0, 0, 1, 9)
                    #Set nut theo gridlayout
                    logoutButtonLayout.addWidget(logoutButton, 1, 4)
                    # Sự kiện cho nút logout
                    logoutButton.clicked.connect(self.handle_logout)

                    #lấy dữ liệu từ lineEdit


                    settingContainer = QVBoxLayout()
                    settingContainer.addLayout(settingLayout)
                    settingContainer.addLayout(logoutButtonLayout)
                    # Set layout cho trang mới
                    newPage.setLayout(settingContainer)

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
        if self.switch_to_login:
            self.switch_to_login()

    def load_branches(self):
        branches = []
        if hasattr(self.controller, "branches_controller") and self.controller.branches_controller:
            branches = self.controller.get_branches_data(
            self.employer_data.enterprise_id,
            self.employer_data.employer_id
            )
        else:
            print("⚠!!! BranchesController chưa sẵn sàng.")

        branch_table = QTableWidget()
        branch_table.setColumnCount(4)
        branch_table.setHorizontalHeaderLabels(["Branch ID", "Name", "Address", "Phone Number"])
        branch_table.setRowCount(len(branches))

        for row_index, branch in enumerate(branches):
            branch_table.setItem(row_index, 0, QTableWidgetItem(str(branch["Branch_ID"])))
            branch_table.setItem(row_index, 1, QTableWidgetItem(branch["Branch_name"]))
            branch_table.setItem(row_index, 2, QTableWidgetItem(branch["Branch_address"]))
            branch_table.setItem(row_index, 3, QTableWidgetItem(branch["Branch_phone_number"]))

        branch_table.resizeColumnsToContents()
        return branch_table



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
    def get_branchesForm_data(self):
        return {
            "id": self.branch_id_input.text().strip(),
            "name": self.branch_name_input.text().strip(),
            "address": self.branch_address_input.text().strip(),
            "phone_number": self.branch_phone_input.text().strip(),
            "employer_id": str(self.employer_data.ID).strip(),
            "enterprise_id": str(self.employer_data.enterprise_id).strip()
        }
    def get_accountSetting_data(self):
        return {
            "employer_id": self.employer_data.ID,
            "username": self.le_username.text().strip(),
            "date_of_birth": self.le_birthdate.date().toPyDate(),
            "email": self.le_email.text().strip(),
            "phone_number": self.le_phone.text().strip(),
            "enterprise_id": self.le_enterprise_id.text().strip()
        }
    def get_productForm_data(self):
        return {
            "id": self.prod_id_input.text().strip(),
            "name": self.prod_name_input.text().strip(),
            "price": self.prod_price_input.text().strip(),
            "amount": self.prod_amount_input.text().strip(),
            "branch_id": self.prod_branch_id_input.text().strip()
        }
