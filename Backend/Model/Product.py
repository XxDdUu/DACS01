import pandas as pd

class Product:
    def __init__(self, ID, name, price, amount, branch_id):
        self.Id = ID
        self.name = name
        self.price = price
        self.amount = amount
        self.branch_id = branch_id