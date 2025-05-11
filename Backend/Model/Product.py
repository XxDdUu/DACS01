import pandas as pd

class Product:
    def __init__(self, ID, name, price, amount, branch_id):
        self.Id = ID
        self.name = name
        self.price = price
        self.amount = amount
        self.branch_id = branch_id
class ProductFormData:
    def __init__(self,product_id , name, price, amount, branch_id):
        self.name = name
        self.price = price
        self.amount = amount
        self.branch_id = branch_id
        self.product_id = product_id

    def get_productForm_data(self):
        return {
            "id": self.product_id.text().strip(),
            "name": self.name.text().strip(),
            "price": self.price.text().strip(),
            "amount": self.amount.text().strip(),
            "branch_id": self.branch_id.text().strip()
        }