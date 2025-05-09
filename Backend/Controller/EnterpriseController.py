from Backend.DAO.EnterpriseDAO import EnterpriseDao
from PyQt6.QtWidgets import QMessageBox

class EnterpriseController:
	def __init__(self, register_view):
		self.register_view = register_view
		self.dao = EnterpriseDao()
		self.register_view.create_enterprise_btn.clicked.connect(self.handle_create_enterprise)
	def handle_create_enterprise(self):
		data = self.register_view.get_enterprise_form_data()
		self.dao.insert_enterprise(data)
		success, message = self.dao.insert_enterprise(data)
		if success:
			QMessageBox.information(self.register_view, "Success", message)
		else:
			QMessageBox.warning(self.register_view, "Error", message)