
import pandas as pd

from Backend.Model import Employer


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

