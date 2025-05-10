import pandas as pd

class ProductFormData:
    def __init__(self, name, price, amount, branch_Id):
        self.name = name
        self.price = price
        self.amount = amount
        self.branch_Id = branch_Id

    def get_productForm_data(self):
        return {
            "name": self.name.text().strip(),
            "price": self.price.text().strip(),
            "amount": self.amount.text().strip(),
            "branch_id": self.branch_Id.text().strip()
        }



