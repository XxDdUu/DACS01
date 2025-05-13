class Employer:
    def __init__(self, ID, username, email, phone_number, date_of_birth, enterprise_id):
        self.ID = ID
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.date_of_birth = date_of_birth
        self.enterprise_id = enterprise_id

class AccountSettingData:
    def __init__(self, username, email, phone_number, date_of_birth):
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.date_of_birth = date_of_birth
    def get_employerName_data(self):
        return {
            "username": self.ID.text().strip(),
        }
    def get_employerDateBirth_data(self):
        return {
            "date_of_birth": self.ID.date().toString("YYYY-MM-DD"),
        }
    def get_employerEmail_data(self):
        return {
            "email": self.ID.text().strip(),
        }
    def get_employerPhoneNum_data(self):
        return {
            "phone_number": self.ID.text().strip(),
        }
