from Backend.DAO.EmployerDAO import EmployerDAO
from Frontend.View.register import Register
from PyQt6.QtWidgets import QMessageBox

class EmployerController:
	def __init__(self, view):
		self.view = view
		self.dao = EmployerDAO()
		self.view.register_btn.clicked.connect(self.handle_register)
	def handle_register(self):
		data = self.view.get_form_data()
		success, message = self.dao.insert_employer(data)
		if success:
			QMessageBox.information(self.view, "Success", message)
		else:
			QMessageBox.warning(self.view, "Error", message)