from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QApplication, QMainWindow, QAbstractSpinBox, QTableView
from PyQt6.QtCore import Qt, QPoint, QEvent, QDate, QPropertyAnimation, QEasingCurve, QRect
import sys
import Frontend.View.resources_rc
from datetime import datetime


class DashBoard(QMainWindow):
	def __init__(self, employer_data, controller):
		super().__init__()
		self.controller = controller
		self.employer_data = employer_data
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
		self.sale_qdate_edit.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons) #làm mất nút up-down của qDateEdit

		self.fetch_account_info(employer_data)
		self.active_switch_pages()

		self.menu_expanded = False
		self.left_menu_animation = QPropertyAnimation(self.mainMenu, b"minimumWidth")
		self.left_menu_animation.setStartValue(self.mainMenu.width())
		self.left_menu_animation.setDuration(300)
		self.left_menu_animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
		self.btn_toggle_menu.clicked.connect(self.toggle_menu)

		self.switch_to_login = None
		self.logout_label.clicked.connect(self.handle_logOut_btn)
		# self.display_PS_table()
		#Xử lý sự kiện các crud row vào table
		self.add_PS_btn.clicked.connect(self.add_row)
		self.remove_PS_btn.clicked.connect(self.delete_row)
		self.update_PS_btn.clicked.connect(self.update_row)

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
	def active_switch_pages(self):
		self.main_display_widget.setCurrentWidget(self.Home_page)
		self.home_btn.clicked.connect(lambda: self.main_display_widget.setCurrentWidget(self.Home_page))
		self.account_setting_btn.clicked.connect(lambda: self.main_display_widget.setCurrentWidget(self.Account_setting_page))
		self.revenue_btn.clicked.connect(lambda: self.main_display_widget.setCurrentWidget(self.Revenue_page))
		self.report_btn.clicked.connect(lambda: self.main_display_widget.setCurrentWidget(self.Report_page))
		self.productSales_menu_btn.clicked.connect(lambda: self.main_display_widget.setCurrentWidget(self.Product_sale_page))
		self.distribution_btn.clicked.connect(lambda: self.main_display_widget.setCurrentWidget(self.Distribution_page))

	def toggle_menu(self):
		current_width = self.mainMenu.width()
		new_width = 44 if self.menu_expanded else 150

		self.left_menu_animation.setStartValue(current_width)
		self.left_menu_animation.setEndValue(new_width)
		self.left_menu_animation.start()

		self.menu_expanded = not self.menu_expanded

	def handle_logOut_btn(self):
		if self.switch_to_login:
			self.switch_to_login()

	def get_PSForm_data(self):
		return {
			"id": self.saleID_PS_le.text().strip(),
			"branch_id": self.branch_id_PS_le.text().strip(),
			"product_id": self.prod_id_PS_le.text().strip(),
			"date": self.sale_qdate_edit.date().toString("yyyy-MM-dd"),
			"quantity_sold": self.quantitySold_PS_le.text().strip(),
			"amount_total": self.saleAmount_PS_le.text().strip()
		}
	# def display_PS_table(self):
	# 	productSale = []
	# 	if hasattr(self.controller,'productSales_controller') and self.controller.productSales_controller:
	# 		print("DEBUG employer ID:", self.employer_data.ID)
	# 		print("DEBUG enterprise ID:", self.employer_data.enterprise_id)
	# 		productSale = self.controller.get_PS_data(
	# 			self.employer_data.ID,
	# 			self.employer_data.enterprise_id
	# 		)
	# 		print("DEBUG result from DB:", productSale)
	#
	# 	model = QStandardItemModel(len(productSale),6)
	# 	model.setHorizontalHeaderLabels(["SALE_ID", "Product_ID", "Branch_ID",
	# 												  "SALE_DATE", "QUANTITY_SOLD", "SALE_AMOUNT"])
	# 	for row_index, prod_sale in enumerate(productSale):
	# 		model.setItem(row_index, 0, QStandardItem(prod_sale["SALE_ID"]))
	# 		model.setItem(row_index, 1, QStandardItem(str(prod_sale["Product_ID"])))
	# 		model.setItem(row_index, 2, QStandardItem(str(prod_sale["Branch_ID"])))
	# 		model.setItem(row_index, 3, QStandardItem(prod_sale["SALE_DATE"]))
	# 		model.setItem(row_index, 4, QStandardItem(prod_sale["QUANTITY_SOLD"]))
	# 		model.setItem(row_index, 5, QStandardItem(prod_sale["SALE_AMOUNT"]))
	# 	self.PS_data_table.setModel(model)
	# 	self.PS_data_table.resizeColumnsToContents()
	# 	print("Product Sales:", productSale)
	#
	# 	return self.PS_data_table

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

		self.model = QStandardItemModel(len(productSale), 6)
		self.model.setHorizontalHeaderLabels(["SALE_ID", "Product_ID", "Branch_ID",
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
				self.model.setItem(row_index, 0, QStandardItem(sale_id))
				self.model.setItem(row_index, 1, QStandardItem(product_id))
				self.model.setItem(row_index, 2, QStandardItem(branch_id))
				self.model.setItem(row_index, 3, QStandardItem(sale_date))
				self.model.setItem(row_index, 4, QStandardItem(quantity_sold))
				self.model.setItem(row_index, 5, QStandardItem(sale_amount))

				print(
					f"DEBUG Row {row_index}: {sale_id}, {product_id}, {branch_id}, {sale_date}, {quantity_sold}, {sale_amount}")

			except Exception as e:
				print(f"ERROR processing row {row_index}: {e}")
				print(f"Row data: {prod_sale}")
				# Create empty items for failed row
				for col in range(6):
					self.model.setItem(row_index, col, QStandardItem(""))

		try:
			self.PS_data_table.setModel(self.model)
			self.PS_data_table.resizeColumnsToContents()
			print(f"Product Sales data loaded: {len(productSale)} records")
		except Exception as e:
			print(f"ERROR setting model: {e}")

		return self.PS_data_table

	def add_row(self):
		row = self.model.rowCount()
		self.model.insertRow(row)
		self.model.setItem(row, 0, QStandardItem(self.saleID_PS_le.text()))
		self.model.setItem(row, 1, QStandardItem(self.prod_id_PS_le.text()))
		self.model.setItem(row, 2, QStandardItem(self.branch_id_PS_le.text()))
		self.model.setItem(row, 3, QStandardItem(self.sale_qdate_edit.text()))
		self.model.setItem(row, 4, QStandardItem(self.quantitySold_PS_le.text()))
		self.model.setItem(row, 5, QStandardItem(self.saleAmount_PS_le.text()))

	def delete_row(self):
		ps_id_delete = self.saleID_PS_le.text().strip()
		for row in range(self.model.rowCount()):
			item = self.model.item(row, 0)
			if item and item.text() == ps_id_delete:
				self.model.removeRow(row)
				print(f"Đã xóa dòng có SALE_ID: {ps_id_delete}")
				return
		print(f"Không tìm thấy SALE_ID: {ps_id_delete}")

	def update_row(self):
		index = self.PS_data_table.currentIndex()
		row = index.row()

		if row >= 0:
			# Nếu có dòng được chọn → cập nhật luôn
			self.model.setItem(row, 0, QStandardItem(self.saleID_PS_le.text()))
			self.model.setItem(row, 1, QStandardItem(self.prod_id_PS_le.text()))
			self.model.setItem(row, 2, QStandardItem(self.branch_id_PS_le.text()))
			self.model.setItem(row, 3, QStandardItem(self.sale_qdate_edit.text()))
			self.model.setItem(row, 4, QStandardItem(self.quantitySold_PS_le.text()))
			self.model.setItem(row, 5, QStandardItem(self.saleAmount_PS_le.text()))
			print("Cập nhật thành công dòng được chọn!")
		else:
			# Nếu không chọn dòng → tìm dòng theo SALE_ID từ input
			ps_id_update = self.saleID_PS_le.text().strip()
			if not ps_id_update:
				print("Vui lòng nhập SALE_ID để cập nhật!")
				return

			for row in range(self.model.rowCount()):
				item = self.model.item(row, 0)
				if item and item.text() == ps_id_update:
					self.model.setItem(row, 1, QStandardItem(self.prod_id_PS_le.text()))
					self.model.setItem(row, 2, QStandardItem(self.branch_id_PS_le.text()))
					self.model.setItem(row, 3, QStandardItem(self.sale_qdate_edit.text()))
					self.model.setItem(row, 4, QStandardItem(self.quantitySold_PS_le.text()))
					self.model.setItem(row, 5, QStandardItem(self.saleAmount_PS_le.text()))
					print(f"Đã cập nhật dòng có SALE_ID: {ps_id_update}")
					return
			print(f"Không tìm thấy SALE_ID: {ps_id_update}")




