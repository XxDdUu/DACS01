from pyexpat.errors import messages

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
		success, message, employer_data = self.dao.check_loginUser(data)
		if success:
			# QMessageBox.information(self.login_view, "Success", message)
			self.login_view.handle_switch_to_maindashboard(employer_data)
			self.login_view.passLineEdit.clear()
			self.login_view.identifierLineEdit.clear()
		else:
			QMessageBox.warning(self.login_view, "Error", message)
class AccSettingController:
	def __init__(self,main_view):
		self.main_view = main_view  # dashboard app
		self.dao = EmployerDAO()
		self.main_view.btn_edit_username.clicked.connect(self.handle_editName)
		self.main_view.btn_edit_birthdate.clicked.connect(self.handle_editDateBirth)
		self.main_view.btn_edit_email.clicked.connect(self.handle_editEmail)
		self.main_view.btn_edit_phone.clicked.connect(self.handle_editPhoneNum)
	def handle_editName(self):
		data = self.main_view.get_accountSetting_data()
		success, message = self.dao.edit_username(data)
		if success:
			QMessageBox.information(self.main_view, "Success", message)
			# self.main_view.employer_data.username = data["username"]
			# self.main_view.le_username.setText(data["username"])
		else:
			QMessageBox.warning(self.main_view, "Error", message)
	def handle_editDateBirth(self):
		data = self.main_view.get_accountSetting_data()
		success, message = self.dao.edit_dateBirth(data)
		if success:
			QMessageBox.information(self.main_view, "Success", message)
			self.main_view.employer_data.username = data["date_of_birth"]
			self.main_view.le_birthdate.setDate(QDate(data["date_of_birth"].year,
													  data["date_of_birth"].month,
													  data["date_of_birth"].day))
		else:
			QMessageBox.warning(self.main_view, "Error", message)
	def handle_editEmail(self):
		data = self.main_view.get_accountSetting_data()
		success, message = self.dao.edit_email(data)
		if success:
			QMessageBox.information(self.main_view, "Success", message)
			self.main_view.employer_data.username = data["email"]
			self.main_view.le_email.setText(data["email"])
		else:
			QMessageBox.warning(self.main_view, "Error", message)
	def handle_editPhoneNum(self):
		data = self.main_view.get_accountSetting_data()
		success, message = self.dao.edit_phoneNum(data)
		if success:
			QMessageBox.information(self.main_view, "Success", message)
			self.main_view.employer_data.username = data["phone_number"]
			self.main_view.le_phone.setText(data["phone_number"])
		else:
			QMessageBox.warning(self.main_view, "Error", message)



