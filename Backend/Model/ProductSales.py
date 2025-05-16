import pandas as pd

class Product_Sales:
    def __init__(self, ID, product_id, branch_id, sale_date, quantity_sold, sale_amount):
        self.ID = ID
        self.product_id = product_id
        self.branch_id = branch_id
        self.sale_date = sale_date
        self.quantity_sold = quantity_sold
        self.sale_amount = sale_amount
class ProductSalesFormData:
    def __init__(self, ID, product_id, branch_id, sale_date, quantity_sold, sale_amount):
        self.ID = ID
        self.product_id = product_id
        self.branch_id = branch_id
        self.sale_date = sale_date
        self.quantity_sold = quantity_sold
        self.sale_amount = sale_amount
    def get_PSForm_data(self):
        return {
            "id": self.ID.text().strip(),
            "branch_id": self.branch_id.text().strip(),
            "product_id": self.product_id.text().strip(),
            "date": self.sale_date.date().toString("yyyy-MM-dd"),
            "quantity_sold": self.quantity_sold.text().strip(),
            "amount_total": self.sale_amount.text().strip()
        }