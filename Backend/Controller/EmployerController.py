from pyexpat.errors import messages

from Backend.DAO.EmployerDAO import EmployerDAO
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDate

class EmployerController:
	def __init__(self, register_view, login_view,main_view):
		self.register_view = register_view # register
		self.login_view = login_view	# login
		self.main_view = main_view		# dashboard app
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
		success, message, employer_data = self.dao.check_loginUser(data)
		if success:
			# QMessageBox.information(self.login_view, "Success", message)
			self.login_view.handle_switch_to_maindashboard(employer_data)
			self.login_view.passLineEdit.clear()
			self.login_view.identifierLineEdit.clear()
		else:
			QMessageBox.warning(self.login_view, "Error", message)
	def handle_editName(self):
		data = self.main_view.get_employerName_data()
		success, message, employer_data = self.dao.(data)
		if success:
			# QMessageBox.information(self.login_view, "Success", message)
			self.login_view.handle_switch_to_maindashboard(employer_data)
		else:
			QMessageBox.warning(self.login_view, "Error", message)
	def handle_editDateBirth(self):
		data = self.main_view.get_employerDateBirth_data()
		success, message, employer_data = self.dao.(data)
		if success:
			QMessageBox.information(self.login_view, "Success", message)
			self.login_view.handle_switch_to_maindashboard(employer_data)
		else:
			QMessageBox.warning(self.login_view, "Error", message)
	def handle_editEmail(self):
		data = self.main_view.get_employerEmail_data()
		success, message, employer_data = self.dao.(data)
		if success:
			QMessageBox.information(self.login_view, "Success", message)
			self.login_view.handle_switch_to_maindashboard(employer_data)
		else:
			QMessageBox.warning(self.login_view, "Error", message)
	def handle_editEmail(self):
		data = self.main_view.get_employerPhoneNum_data()
		success, message, employer_data = self.dao.(data)
		if success:
			QMessageBox.information(self.login_view, "Success", message)
			self.login_view.handle_switch_to_maindashboard(employer_data)
		else:
			QMessageBox.warning(self.login_view, "Error", message)



