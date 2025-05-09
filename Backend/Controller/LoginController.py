from Backend.DAO.EmployerDAO import EmployerDAO
from Frontend.View.register import Register
from PyQt6.QtWidgets import QMessageBox, QMainWindow

class LoginController:
    def __init__(self,view):
        self.view = view
        self.dao = EmployerDAO()
        self.view.login_button.clicked.connect(self.handle_loginCheck)
    def handle_loginCheck(self):
        data = self.view.check_loginForm_data()
        success, message = self.dao.insert_employer(data)
        if success:
            QMessageBox.information(self.view, "Success", message)
        else:
            QMessageBox.warning(self.view, "Error", message)