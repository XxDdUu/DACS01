import pandas as pd

class BranchesFormData:
    def __init__(self, name, address, phone_num):
        self.name = name
        self.address = address
        self.phone_num = phone_num

    def get_branchesForm_data(self):
        return {
            "name": self.name.text().strip(),
            "address": self.address.text().strip(),
            "phone_number": self.phone_num.text().strip()
        }