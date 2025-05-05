import pandas as pd

class Branches:
    def __init__(self, ID, name, address, phone_number, create_at_time):
        self.ID = ID
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.createTime = create_at_time