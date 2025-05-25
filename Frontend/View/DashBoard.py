from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QApplication, QMainWindow, QAbstractSpinBox, QMessageBox
from PyQt6.QtCore import Qt, QPoint, QEvent, QDate, QPropertyAnimation, QEasingCurve, QRect
import sys
import Frontend.View.resources_rc
from datetime import datetime

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

		self.header.mouseMoveEvent = self.mouse_move_event
		self.header.mousePressEvent = self.mouse_press_event
		self.header.mouseReleaseEvent = self.mouse_release_event

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

	def exit_window(self):
		self.close()
	def toggle_maximize(self):
		if self.is_maximized:
			self.showNormal()
		else:
			self.showMaximized()
		self.is_maximized = True
	def mouse_press_event(self, event):
		if event.button() == Qt.MouseButton.LeftButton:
			self._drag_active = True
			self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
			event.accept()
	def mouse_release_event(self, event):
		self._drag_active = False
	def mouse_move_event(self, event):
		if self._drag_active and event.buttons() == Qt.MouseButton.LeftButton:
			self.move(event.globalPosition().toPoint() - self._drag_position)
			event.accept()

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
		self.report_btn.clicked.connect(lambda: self.main_display_widget.setCurrentWidget(self.Report_page))
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

	def display_PS_table(self):
		productSale = []
		if hasattr(self.controller, 'productSales_controller') and self.controller.productSales_controller:
			print("DEBUG employer ID:", self.employer_data.ID)
			print("DEBUG enterprise ID:", self.employer_data.enterprise_id)
			productSale = self.controller.get_PS_data(
				self.employer_data.ID,
				self.employer_data.enterprise_id
			)
			print("DEBUG result from DB:", productSale)

		model = QStandardItemModel(len(productSale), 6)
		model.setHorizontalHeaderLabels(["SALE_ID", "Product_ID", "Branch_ID",
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
				model.setItem(row_index, 0, QStandardItem(sale_id))
				model.setItem(row_index, 1, QStandardItem(product_id))
				model.setItem(row_index, 2, QStandardItem(branch_id))
				model.setItem(row_index, 3, QStandardItem(sale_date))
				model.setItem(row_index, 4, QStandardItem(quantity_sold))
				model.setItem(row_index, 5, QStandardItem(sale_amount))

				print(
					f"DEBUG Row {row_index}: {sale_id}, {product_id}, {branch_id}, {sale_date}, {quantity_sold}, {sale_amount}")

			except Exception as e:
				print(f"ERROR processing row {row_index}: {e}")
				print(f"Row data: {prod_sale}")
				# Create empty items for failed row
				for col in range(6):
					model.setItem(row_index, col, QStandardItem(""))

		try:
			self.PS_data_table.setModel(model)
			self.PS_data_table.resizeColumnsToContents()
			print(f"Product Sales data loaded: {len(productSale)} records")
		except Exception as e:
			print(f"ERROR setting model: {e}")

		return self.PS_data_table

		#setter method
		def set_employer_data(self, employer_data):
			self.employer_data = employer_data
		def set_enterprise_data(self, enterprise_data):
			self.enterprise_data = enterprise_data