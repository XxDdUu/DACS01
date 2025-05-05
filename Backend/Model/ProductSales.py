import pandas as pd

class Product_Sales:
    def __init__(self, ID, product_id, branch_id, sale_date, quantity_sold, sale_amount):
        self.ID = ID
        self.product_id = product_id
        self.branch_id = branch_id
        self.sale_date = sale_date
        self.quantity_sold = quantity_sold
        self.sale_amount = sale_amount