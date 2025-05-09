from Backend.DAO.EmployerDAO import EmployerDAO
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDate

class EmployerController:
	def __init__(self, register_view, login_view):
		self.register_view = register_view # register
		self.login_view = login_view	# login
		self.dao = EmployerDAO()
		self.register_view.register_btn.clicked.connect(self.handle_register)
		self.login_view.login_button.clicked.connect(self.handle_loginCheck)
	def handle_register(self):
		data = self.register_view.get_employer_form_data()
		success, message = self.dao.insert_employer(data)
		if success:
			QMessageBox.information(self.register_view, "Success", message)
			# clear tất cả khi register thanh cong
			self.register_view.Username.clear()
			self.register_view.Email.clear()
			self.register_view.Phone_Num.clear()
			self.register_view.Enterprise_id.clear()
			self.register_view.enterprise_password_employer.clear()
			self.register_view.Password.clear()
			self.register_view.Confirm_password.clear()
			self.register_view.DateOfBirth.setDate(QDate.currentDate())
		else:
			QMessageBox.warning(self.register_view, "Error", message)
	def handle_loginCheck(self):
		data = self.login_view.check_loginForm_data()
		success, message = self.dao.check_loginUser(data)
		if success:
			QMessageBox.information(self.login_view, "Success", message)
			self.login_view.handle_login_enter()
		else:
			QMessageBox.warning(self.login_view, "Error", message)
