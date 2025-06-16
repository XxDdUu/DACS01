from Frontend.View.component.SearchableTable import SearchableTable
class DisplayTableInDashBoard():
	def __init__(self):
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
				self.revenue_data_table.setModel(rev_model)
				self.revenue_data_table.resizeColumnsToContents()
			except Exception as e:
				print(f"ERROR setting model: {e}")

		return self.revenue_data_table
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
			self.controller.product_controller.product_data_changed.connect(self.display_top_product_table)
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
			if TopProduct:
				first_product_name = str(TopProduct[0].get("Product_NAME", ""))
				self.top_product_name_label.setText(first_product_name)
			else:
				self.top_product_name_label.setText("No top products found.")
			self.top_product_date_label.setText(datetime.now().strftime("%d/%m/%Y"))
			print(f"Product Top data loaded: {len(TopProduct)} records")
		except Exception as e:
			print(f"ERROR setting model: {e}")

		return self.top_product_table