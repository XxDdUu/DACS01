from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QApplication, QMainWindow, QAbstractSpinBox, QMessageBox, QFrame, QVBoxLayout
from PyQt6.QtCore import Qt, QPoint, QEvent, QDate, QPropertyAnimation, QEasingCurve, QRect
from Frontend.View.component.SearchableTable import SearchableTable
import traceback
from datetime import datetime
class DisplayTableInDashBoard:
	def __init__(self, controller, dashboard_ui, employer_data):
		self.controller = controller
		self.dashboard_ui = dashboard_ui
		self.employer_data = employer_data
	def display_revenue_table(self):
		revenues = []
		if hasattr(self.controller,"revenue_controller") and self.controller.revenue_controller:
			self.controller.revenue_controller.revenue_data_changed.connect(self.display_revenue_table)
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
			self.dashboard_ui.revenue_data_table.setModel(rev_model)
			self.dashboard_ui.revenue_data_table.resizeColumnsToContents()
		except Exception as e:
			traceback.print_exc()
		return self.dashboard_ui.revenue_data_table
	def display_PS_table(self):
		productSale = []
		if hasattr(self.controller, 'productSales_controller') and self.controller.productSales_controller:
			self.controller.productSales_controller.ps_data_changed.connect(self.display_PS_table)
			productSale = self.controller.get_PS_data(
				self.employer_data.ID,
				self.employer_data.enterprise_id
			)

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

			except Exception as e:
				for col in range(6):
					PS_model.setItem(row_index, col, QStandardItem(""))
		try:
			self.dashboard_ui.PS_data_table.setModel(PS_model)
			self.dashboard_ui.PS_data_table.resizeColumnsToContents()
		except Exception as e:
			traceback.print_exc()
		return self.dashboard_ui.PS_data_table
	def display_top_product_table(self):
		TopProduct = []
		if hasattr(self.controller, 'product_controller') and self.controller.product_controller:
			self.controller.product_controller.product_data_changed.connect(self.display_top_product_table)
			TopProduct = self.controller.get_top_products_data(
				self.employer_data.enterprise_id
			)

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

			except Exception as e:
				traceback.print_exc()
				# Create empty items for failed row
				for col in range(6):
					TP_model.setItem(row_index, col, QStandardItem(""))

		try:
			self.dashboard_ui.top_product_table.setModel(TP_model)
			self.dashboard_ui.top_product_table.resizeColumnsToContents()
			if TopProduct:
				first_product_name = str(TopProduct[0].get("Product_NAME", ""))
				self.dashboard_ui.top_product_name_label.setText(first_product_name)
			else:
				self.dashboard_ui.top_product_name_label.setText("No top products found.")
			self.dashboard_ui.top_product_date_label.setText(datetime.now().strftime("%d/%m/%Y"))
		except Exception as e:
			traceback.print_exc()
		return self.dashboard_ui.top_product_table
	def display_branch_table(self):
		branches = []
		if hasattr(self.controller, 'branches_controller') and self.controller.branches_controller:
			self.controller.branches_controller.branch_data_changed.connect(self.display_branch_table)
			branches = self.controller.get_branches_data(
				self.employer_data.enterprise_id,
				self.employer_data.ID
			)

		self.branch_model = QStandardItemModel(len(branches), 7)
		self.branch_model.setHorizontalHeaderLabels(["Branch_ID", "Branch_name", "Branch_address",
										 "Branch_phone_number", "Create_at", "Employer_ID","Enterprise_ID"])

		for row_index, branch in enumerate(branches):
			try:

				branch_id = str(branch.get("Branch_ID", ""))
				employer_id = str(branch.get("Employer_ID", ""))
				enterprise_id = str(branch.get("Enterprise_ID", ""))
				branch_name = str(branch.get("Branch_name", ""))
				branch_address = str(branch.get("Branch_address", ""))
				branch_phone = str(branch.get("Branch_phone_number",""))

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

			except Exception as e:
				for col in range(7):
					self.branch_model.setItem(row_index, col, QStandardItem(""))

		try:
			self.branch_search_working = SearchableTable(self.dashboard_ui.search_branch_le, self.dashboard_ui.branchData_table, self.branch_model)
			self.branch_search_working.search_function()
			self.dashboard_ui.branchData_table.resizeColumnsToContents()
			branch_ids = []
			for row in range(self.branch_model.rowCount()):
				item = self.branch_model.item(row, 0)
				if item is not None:
					branch_ids.append(item.text())
			self.controller.product_controller.branch_id_list = branch_ids
			self.controller.product_controller.add_branch_id_to_combobox()

		except Exception as e:
			traceback.print_exc()
		return self.dashboard_ui.branchData_table
	def display_product_table(self):
		products = []
		if hasattr(self.controller, 'product_controller') and self.controller.product_controller:
			self.controller.product_controller.product_data_changed.connect(self.display_product_table)
			products = self.controller.get_products_data(
				self.employer_data.ID,
				self.employer_data.enterprise_id
			)

		self.products_model = QStandardItemModel(len(products), 5)
		self.products_model.setHorizontalHeaderLabels(["Product_ID", "Product_NAME", "Price",
										 "Amount", "Branch_ID"])

		for row_index, prod in enumerate(products):
			try:
				product_id = str(prod.get("Product_ID",""))
				product_name = str(prod.get("Product_NAME", ""))
				branch_id = str(prod.get("Branch_ID", ""))
				price = str(prod.get("PRICE", ""))
				amount = str(prod.get("AMOUNT", ""))

				self.products_model.setItem(row_index, 0, QStandardItem(product_id))
				self.products_model.setItem(row_index, 1, QStandardItem(product_name))
				self.products_model.setItem(row_index, 2, QStandardItem(price))
				self.products_model.setItem(row_index, 3, QStandardItem(amount))
				self.products_model.setItem(row_index, 4, QStandardItem(branch_id))

			except Exception as e:
				for col in range(7):
					self.products_model.setItem(row_index, col, QStandardItem(""))

		try:
			self.products_search_working = SearchableTable(self.dashboard_ui.search_products_le, self.dashboard_ui.product_data_table,
														 self.products_model)
			self.products_search_working.search_function()
			self.dashboard_ui.product_data_table.resizeColumnsToContents()

		except Exception as e:
			traceback.print_exc()
		return self.dashboard_ui.product_data_table