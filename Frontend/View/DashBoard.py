import os
import traceback
from itertools import product

from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QApplication, QMainWindow, QAbstractSpinBox, QMessageBox, QFrame, QVBoxLayout
from PyQt6.QtCore import Qt, QPoint, QEvent, QDate, QPropertyAnimation, QEasingCurve, QRect
import sys

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import Frontend.View.resources_rc
import datetime

from Frontend.Chart.Branch_PSChart import PSBranchChart
from Frontend.Chart.RevenueGeneralChart import RevenueGeneralChart
from Frontend.View.SearchableTable import SearchableTable


class DashBoard(QMainWindow):
	def __init__(self, controller ,employer_data = None, enterprise_data = None):
		super().__init__()
		self.controller = controller
		self.employer_data = employer_data
		self.enterprise_data = enterprise_data
		uic.loadUi("Frontend/dashboardUI.ui", self)
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
		self.setWindowIcon(QIcon("Frontend/View/img/logo/dark_pythonLogo.png"))

		self.close_btn.clicked.connect(self.exit_window)
		self.maximize_btn.clicked.connect(self.toggle_maximize)
		self.minimize_btn.clicked.connect(self.showMinimized)
		self.is_maximized = False

		self._drag_active = False
		self._drag_position = QPoint()

		self.fetch_account_info(employer_data)
		self.active_switch_pages()

		self.menu_expanded = False
		self.left_menu_animation = QPropertyAnimation(self.mainMenu, b"minimumWidth")
		self.left_menu_animation.setStartValue(self.mainMenu.width())
		self.left_menu_animation.setDuration(300)
		self.left_menu_animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
		self.btn_toggle_menu.clicked.connect(self.toggle_menu)

		self.logout_label.clicked.connect(self.confirm_logout)
		self.display_PS_table()
		self.canvas_draw_PS_chart()

	def exit_window(self):
		self.close()
	def toggle_maximize(self):
		if self.is_maximized:
			self.showNormal()
		else:
			self.showMaximized()
		self.is_maximized = not self.is_maximized
	def mousePressEvent(self, event):
		focused_widget = self.focusWidget()
		if focused_widget is not None:
			focused_widget.clearFocus()
		super().mousePressEvent(event)

	def fetch_account_info(self, employer_data):
		self.employer_name_lineedit.setText(employer_data.username)

		formatted_str = employer_data.create_at_time.strftime("%H:%M:%S %d/%m/%Y")

		self.display_create_date.setText("Join date: " + formatted_str)
		self.email_line_edit.setText(employer_data.email)
		self.Phone_number_lineedit.setText(employer_data.phone_number)
		self.enterprise_id_line_edit.setText(employer_data.enterprise_id)
		birthdate = self.employer_data.date_of_birth
		qbirthdate = QDate(birthdate.year, birthdate.month, birthdate.day)

		self.dateEdit.setDate(qbirthdate)

	def fetch_enterprise_info(self, enterprise_data):
		self.enterprise_name_line_edit.setText(enterprise_data.name)
		self.enterprise_founder_line_edit.setText(enterprise_data.founder)
		self.enterprise_address_line_edit.setText(enterprise_data.address)
		self.enterprise_phone_num_line_edit.setText(enterprise_data.phone_number)
		self.enterprise_bs_type_text_edit.setText(enterprise_data.type)
		self.enterprise_bs_type_text_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.enterprise_industry_line_edit.setText(enterprise_data.industry)

	def active_switch_pages(self):

		self.main_display_widget.setCurrentWidget(self.Home_page)
		self.home_btn.clicked.connect(lambda: self.main_display_widget.setCurrentWidget(self.Home_page))
		self.account_setting_btn.clicked.connect(lambda: self.main_display_widget.setCurrentWidget(self.Account_setting_page))
		self.revenue_btn.clicked.connect(lambda: self.main_display_widget.setCurrentWidget(self.Revenue_page))
		self.productSales_menu_btn.clicked.connect(lambda: self.main_display_widget.setCurrentWidget(self.Product_sale_page))
		self.distribution_btn.clicked.connect(lambda: self.main_display_widget.setCurrentWidget(self.Distribution_page))

		self.employer_and_enterpriseInfo.setCurrentWidget(self.employer_info)
		self.btn_enterprise_info.clicked.connect(lambda: self.employer_and_enterpriseInfo.setCurrentWidget(self.enterprise_info))
		self.btn_profile.clicked.connect(lambda: self.employer_and_enterpriseInfo.setCurrentWidget(self.employer_info))

	def toggle_menu(self):
		current_width = self.mainMenu.width()
		new_width = 44 if self.menu_expanded else 150
		if self.menu_expanded:
			self.logout_label.setText('<img src="Frontend/View/img/icon/icons8_logout_rounded_down.svg">')
		else:
			self.logout_label.setText('<img src="Frontend/View/img/icon/icons8_logout_rounded_down.svg" style="width:16px; height:16px; vertical-align:middle;"> Log out')

		self.left_menu_animation.setStartValue(current_width)
		self.left_menu_animation.setEndValue(new_width)
		self.left_menu_animation.start()

		self.menu_expanded = not self.menu_expanded

	def handle_logout(self):
		if self.switch_to_login:
			self.switch_to_login()

	def confirm_logout(self):
		qm = QMessageBox
		res = qm.question(self, 'Confirm', 'Are you sure to log out?', qm.StandardButton.Yes | qm.StandardButton.No)
		if res == qm.StandardButton.Yes:
			self.handle_logout()
	def get_PSForm_data(self):
		return {
			"id": self.saleID_PS_le.text().strip(),
			"branch_id": self.branch_id_PS_le.text().strip(),
			"product_id": self.prod_id_PS_le.text().strip(),
			"date": self.sale_qdate_edit.date().toString("yyyy-MM-dd"),
			"quantity_sold": self.quantitySold_PS_le.text().strip(),
			"amount_total": self.saleAmount_PS_le.text().strip()
		}
	def get_AccSetting_data(self):
		return {
			"employer_id": self.employer_data.ID,
			"username": self.employer_name_lineedit.text().strip(),
			"date_of_birth": self.dateEdit.date().toPyDate(),
			"email": self.email_line_edit.text().strip(),
			"phone_number": self.Phone_number_lineedit.text().strip(),
			"enterprise_id": self.enterprise_id_line_edit.text().strip()
		}
	def canvas_draw_PS_chart(self):
		# A, B, C là tên branch trong csdl bên này
		rev_general_chart = RevenueGeneralChart(self.employer_data)
		chartA = PSBranchChart("A",
							   self.employer_data.ID,
							   self.employer_data.enterprise_id)
		chartB = PSBranchChart("B",
							   self.employer_data.ID,
							   self.employer_data.enterprise_id)
		chartC = PSBranchChart("C",
							   self.employer_data.ID,
							   self.employer_data.enterprise_id)
		fig_revenueGeneral_chart = rev_general_chart.figure
		fig_PS_branchA_chart = chartA.figure
		fig_PS_branchB_chart = chartB.figure
		fig_PS_branchC_chart = chartC.figure

		canvas_RevenuePage = FigureCanvas(fig_revenueGeneral_chart)
		canvas_chart_left = FigureCanvas(fig_PS_branchA_chart)
		canvas_chart_center = FigureCanvas(fig_PS_branchB_chart)
		canvas_chart_right = FigureCanvas(fig_PS_branchC_chart)

		for frame in [self.frame_chart_1, self.frame_chart_2, self.frame_chart_3, self.frame_revChart_1]:
			if frame.layout() is None:
				frame.setLayout(QVBoxLayout())

		self.frame_revChart_1.layout().addWidget(canvas_RevenuePage)
		self.frame_chart_1.layout().addWidget(canvas_chart_left)
		self.frame_chart_2.layout().addWidget(canvas_chart_center)
		self.frame_chart_3.layout().addWidget(canvas_chart_right)

	def display_revenue_table(self):
		revenues = []
		if hasattr(self.controller,"revenue_controller") and self.controller.revenue_controller:
			# self.controller.revenue_controller.revenue_data_changed.connect(self.display_revenue_table)
			revenues = self.controller.get_revenues_data(
				self.employer_data.ID,
				self.employer_data.enterprise_id,
			)
		rev_model = QStandardItemModel(len(revenues),5)
		rev_model.setHorizontalHeaderLabels(['Revenue_ID', 'Revenue_date',
												 'Amount', 'Create_at', 'Branch_ID'])
		for row_index, rev in enumerate(revenues):
			try:
				rev_id = str(rev.get("Revenue_ID",""))
				rev_branch_id = str(rev.get("Branch_ID",""))

				rev_date = rev.get("Revenue_date","")
				if hasattr(rev_date,"strftime"):
					rev_date = rev_date.strftime("%Y-%m-%d")
				else:
					rev_date = str(rev_date)

				rev_create_at = rev.get("Create_at","")
				if hasattr(rev_create_at,"strftime"):
					rev_create_at = rev_create_at.strftime("%Y-%m-%d %H:%M:S")
				else:
					rev_create_at = str(rev_create_at)

				rev_amount = rev.get("Amount")
				if hasattr(rev_amount,"__float__"):
					rev_amount = f"{float(rev_amount):.2f}"
				else:
					rev_amount = str(rev_amount)

				rev_model.setItem(row_index,0,QStandardItem(rev_id))
				rev_model.setItem(row_index,1,QStandardItem(rev_date))
				rev_model.setItem(row_index,2,QStandardItem(rev_amount))
				rev_model.setItem(row_index,3,QStandardItem(rev_create_at))
				rev_model.setItem(row_index,4,QStandardItem(rev_branch_id))

			except Exception as e:
				traceback.print_exc()
				print(f"Exception: {e}")
				for row in range(5):
					rev_model.setItem(row_index,row,QStandardItem(""))

			try:
				self.rev_data_table.setModel(rev_model)
				self.rev_data_table.resizeColumnsToContents()
			except Exception as e:
				print(f"ERROR setting model: {e}")

		return self.rev_data_table

	def display_PS_table(self):
		productSale = []
		if hasattr(self.controller, 'productSales_controller') and self.controller.productSales_controller:
			print("DEBUG employer ID:", self.employer_data.ID)
			print("DEBUG enterprise ID:", self.employer_data.enterprise_id)
			self.controller.productSales_controller.ps_data_changed.connect(self.display_PS_table)
			productSale = self.controller.get_PS_data(
				self.employer_data.ID,
				self.employer_data.enterprise_id
			)
			print("DEBUG result from DB:", productSale)

		PS_model = QStandardItemModel(len(productSale), 6)
		PS_model.setHorizontalHeaderLabels(["SALE_ID", "Product_ID", "Branch_ID",
										 "SALE_DATE", "QUANTITY_SOLD", "SALE_AMOUNT"])

		for row_index, prod_sale in enumerate(productSale):
			try:
				# Convert all values to string safely
				sale_id = str(prod_sale.get("SALE_ID", ""))
				product_id = str(prod_sale.get("Product_ID", ""))
				branch_id = str(prod_sale.get("Branch_ID", ""))

				# Handle datetime.date object
				sale_date = prod_sale.get("SALE_DATE", "")
				if hasattr(sale_date, 'strftime'):
					sale_date = sale_date.strftime("%Y-%m-%d")
				else:
					sale_date = str(sale_date)

				quantity_sold = str(prod_sale.get("QUANTITY_SOLD", ""))

				# Handle Decimal object
				sale_amount = prod_sale.get("SALE_AMOUNT", "")
				if hasattr(sale_amount, '__float__'):  # Decimal objects have __float__
					sale_amount = f"{float(sale_amount):.2f}"
				else:
					sale_amount = str(sale_amount)

				# Set items safely
				PS_model.setItem(row_index, 0, QStandardItem(sale_id))
				PS_model.setItem(row_index, 1, QStandardItem(product_id))
				PS_model.setItem(row_index, 2, QStandardItem(branch_id))
				PS_model.setItem(row_index, 3, QStandardItem(sale_date))
				PS_model.setItem(row_index, 4, QStandardItem(quantity_sold))
				PS_model.setItem(row_index, 5, QStandardItem(sale_amount))

				print(f"DEBUG Row {row_index}: {sale_id}, {product_id}, {branch_id}, {sale_date}, {quantity_sold}, {sale_amount}")

			except Exception as e:
				print(f"ERROR processing row {row_index}: {e}")
				print(f"Row data: {prod_sale}")
				# Create empty items for failed row
				for col in range(6):
					PS_model.setItem(row_index, col, QStandardItem(""))

		try:
			self.PS_data_table.setModel(PS_model)
			self.PS_data_table.resizeColumnsToContents()
			print(f"Product Sales data loaded: {len(productSale)} records")
		except Exception as e:
			print(f"ERROR setting model: {e}")

		return self.PS_data_table
	def display_top_product_table(self):
		TopProduct = []
		if hasattr(self.controller, 'product_controller') and self.controller.product_controller:
			self.controller.product_controller.data_changed.connect(self.display_top_product_table)
			TopProduct = self.controller.get_top_products_data(
				self.employer_data.enterprise_id
			)
			print("DEBUG Top Product from DB!!", TopProduct)

		TP_model = QStandardItemModel(len(TopProduct), 6)
		TP_model.setHorizontalHeaderLabels(["Product_ID", "Product_NAME", "Price",
										 "Amount", "Branch_ID", "Total_quantity_sold"])

		for row_index, top_product in enumerate(TopProduct):
			try:
				# Convert all values to string safely
				product_id = str(top_product.get("Product_ID", ""))
				product_name = str(top_product.get("Product_NAME", ""))
				product_price = str(top_product.get("PRICE", ""))

				product_amount = str(top_product.get("AMOUNT", ""))
				branch_id = str(top_product.get("Branch_ID", ""))
				total_quantity_sold = str(top_product.get("total_quantity_sold", ""))

				if hasattr(product_price, '__float__'):  # Decimal objects have __float__
					product_price = f"{float(product_price):.2f}"
				else:
					product_price = str(product_price)

				# Set items safely
				TP_model.setItem(row_index, 0, QStandardItem(product_id))
				TP_model.setItem(row_index, 1, QStandardItem(product_name))
				TP_model.setItem(row_index, 2, QStandardItem(product_price))
				TP_model.setItem(row_index, 3, QStandardItem(product_amount))
				TP_model.setItem(row_index, 4, QStandardItem(branch_id))
				TP_model.setItem(row_index, 5, QStandardItem(total_quantity_sold))

				print(
					f"DEBUG Row {row_index}: {product_id}, {product_name}, {product_price}, {product_amount}, {branch_id}, {total_quantity_sold}")

			except Exception as e:
				print(f"ERROR processing row {row_index}: {e}")
				print(f"Row top products data: {TopProduct}")
				# Create empty items for failed row
				for col in range(6):
					TP_model.setItem(row_index, col, QStandardItem(""))

		try:
			self.top_product_table.setModel(TP_model)
			self.top_product_table.resizeColumnsToContents()
			self.top_product_name_label.setText(product_name)
			self.top_product_date_label.setText(datetime.now().strftime("%d/%m/%Y"))
			print(f"Product Sales data loaded: {len(TopProduct)} records")
		except Exception as e:
			print(f"ERROR setting model: {e}")

		return self.top_product_table

		#setter method
	def set_employer_data(self, employer_data):
		self.employer_data = employer_data
	def set_enterprise_data(self, enterprise_data):
		self.enterprise_data = enterprise_data

	def display_branch_table(self):
		branches = []
		if hasattr(self.controller, 'branches_controller') and self.controller.branches_controller:
			self.controller.branches_controller.data_changed.connect(self.display_branch_table)
			print("DEBUG employer ID:", self.employer_data.ID)
			print("DEBUG enterprise ID:", self.employer_data.enterprise_id)
			branches = self.controller.get_branches_data(
				self.employer_data.enterprise_id,
				self.employer_data.ID
			)
			print("DEBUG result from DB:", branches)
		self.branch_model = QStandardItemModel(len(branches), 7)
		self.branch_model.setHorizontalHeaderLabels(["Branch_ID", "Branch_name", "Branch_address",
										 "Branch_phone_number", "Create_at", "Employer_ID","Enterprise_ID"])

		for row_index, branch in enumerate(branches):
			try:
				# Convert all values to string safely
				branch_id = str(branch.get("Branch_ID", ""))
				employer_id = str(branch.get("Employer_ID", ""))
				enterprise_id = str(branch.get("Enterprise_ID", ""))
				branch_name = str(branch.get("Branch_name", ""))
				branch_address = str(branch.get("Branch_address", ""))
				branch_phone = str(branch.get("Branch_phone_number",""))

				# Handle datetime.date object
				branch_date = branch.get("Create_at", "")
				if hasattr(branch_date, 'strftime'):
					branch_date = branch_date.strftime("%Y-%m-%d")
				else:
					branch_date = str(branch_date)

				# Set items safely
				self.branch_model.setItem(row_index, 0, QStandardItem(branch_id))
				self.branch_model.setItem(row_index, 1, QStandardItem(branch_name))
				self.branch_model.setItem(row_index, 2, QStandardItem(branch_address))
				self.branch_model.setItem(row_index, 3, QStandardItem(branch_phone))
				self.branch_model.setItem(row_index, 4, QStandardItem(branch_date))
				self.branch_model.setItem(row_index, 5, QStandardItem(employer_id))
				self.branch_model.setItem(row_index, 6, QStandardItem(enterprise_id))

				print(
					f"DEBUG Row {row_index}: {branch_id}, {branch_name}, {branch_address}, {branch_phone}, {branch_date}, {employer_id}, {enterprise_id}")

			except Exception as e:
				print(f"ERROR processing row {row_index}: {e}")
				print(f"Row data: {branches}")
				# Create empty items for failed row
				for col in range(7):
					self.branch_model.setItem(row_index, col, QStandardItem(""))

		try:
			self.branch_search_working = SearchableTable(self.search_branch_le, self.branchData_table, self.branch_model)
			self.branch_search_working.search_function()
			self.branchData_table.resizeColumnsToContents()
			branch_ids = []
			for row in range(self.branch_model.rowCount()):
				item = self.branch_model.item(row, 0)
				if item is not None:
					branch_ids.append(item.text())
			self.controller.product_controller.branch_id_list = branch_ids
			self.controller.product_controller.add_branch_id_to_combobox()
			print(f"Branches data loaded: {len(branches)} records")
		except Exception as e:
			print(f"ERROR setting model: {e}")

		return self.branchData_table
	def display_product_table(self):
		products = []
		if hasattr(self.controller, 'product_controller') and self.controller.product_controller:
			self.controller.product_controller.data_changed.connect(self.display_product_table)
			print("DEBUG employer ID:", self.employer_data.ID)
			print("DEBUG enterprise ID:", self.employer_data.enterprise_id)
			products = self.controller.get_products_data(
				self.employer_data.ID,
				self.employer_data.enterprise_id
			)
			print("DEBUG result from DB:", products)

		self.products_model = QStandardItemModel(len(products), 5)
		self.products_model.setHorizontalHeaderLabels(["Product_ID", "Product_NAME", "Price",
										 "Amount", "Branch_ID"])

		for row_index, prod in enumerate(products):
			try:
				# Convert all values to string safely
				product_id = str(prod.get("Product_ID",""))
				product_name = str(prod.get("Product_NAME", ""))
				branch_id = str(prod.get("Branch_ID", ""))
				price = str(prod.get("PRICE", ""))
				amount = str(prod.get("AMOUNT", ""))

				# Set items safely
				self.products_model.setItem(row_index, 0, QStandardItem(product_id))
				self.products_model.setItem(row_index, 1, QStandardItem(product_name))
				self.products_model.setItem(row_index, 2, QStandardItem(price))
				self.products_model.setItem(row_index, 3, QStandardItem(amount))
				self.products_model.setItem(row_index, 4, QStandardItem(branch_id))

				print(
					f"DEBUG Row {row_index}: {product_id}, {product_name}, {price}, {amount}, {branch_id}")

			except Exception as e:
				print(f"ERROR processing row {row_index}: {e}")
				print(f"Row data: {products}")
				# Create empty items for failed row
				for col in range(7):
					self.products_model.setItem(row_index, col, QStandardItem(""))

		try:
			self.products_search_working = SearchableTable(self.search_products_le, self.product_data_table,
														 self.products_model)
			self.products_search_working.search_function()
			self.product_data_table.resizeColumnsToContents()
			print(f"Products data loaded: {len(products)} records")
		except Exception as e:
			print(f"ERROR setting model: {e}")

		return self.product_data_table

