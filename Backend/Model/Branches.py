
import pandas as pd

class Branches:
    def __init__(self, ID, name, address, phone_number, create_at_time):
        self.ID = ID
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.createTime = create_at_time

class BranchesFormData:
    def __init__(self,id ,name, address, phone_num):
        self.id = id
        self.name = name
        self.address = address
        self.phone_num = phone_num

    def get_branchesForm_data(self):
        return {
            "id": self.id.text().strip(),
            "name": self.name.text().strip(),
            "address": self.address.text().strip(),
            "phone_number": self.phone_num.text().strip()
        }
