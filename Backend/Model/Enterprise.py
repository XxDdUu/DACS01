import pandas as pd

class Enterprise:
    def __init__(self, ID, name, founder, address, phone_number, type, industry):
        self.ID = ID
        self.name = name
        self.founder = founder
        self.address = address
        self.phone_number = phone_number
        self.type = type
        self.industry = industry