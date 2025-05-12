import pandas as pd

class Revenue:
    def __init__(self, ID, date, amount, datetime, branch_id):
        self.ID = ID
        self.date = date
        self.amount = amount
        self.datetime = datetime
        self.branch_id = branch_id

class RevenueFormData:
    def __init__(self,revenue_id, revenue_date, amount, branch_id):
        self.revenue_id = revenue_id
        self.revenue_date = revenue_date
        self.amount = amount
        self.branch_id = branch_id
    def get_revenueForm_data(self):
        return {
            "id": self.revenue_id.text().strip(),
            "date": self.revenue_date.date().toString("yyyy-MM-dd"),
            "amount": self.amount.text().strip(),
            "branch_id": self.branch_id.text().strip()
        }