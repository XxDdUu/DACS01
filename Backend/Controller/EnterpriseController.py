from Backend.DAO.EnterpriseDAO import EnterpriseDao
from PyQt6.QtWidgets import QMessageBox

class EnterpriseController:
	def __init__(self, register_view):
		self.register_view = register_view
		self.dao = EnterpriseDao()
		self.register_view.create_enterprise_btn.clicked.connect(self.handle_create_enterprise)
	def handle_create_enterprise(self):
		data = self.register_view.get_enterprise_form_data()
		success, message = self.dao.insert_enterprise(data)
		if success:
			QMessageBox.information(self.register_view, "Success", message)
			# clear tất cả khi register thanh cong
			self.register_view.enterprise_name.clear()
			self.register_view.enterprise_founder.clear()
			self.register_view.enterprise_address.clear()
			self.register_view.enterprise_phone_number.clear()
			self.register_view.enterprise_industry.clear()
			self.register_view.enterprise_password.clear()
			self.register_view.confirm_enterprise_password.clear()
			self.register_view.enterprise_name.clear()
			self.register_view.business_type.setCurrentText("Partnership (Hợp tác xã)")
		else:
			QMessageBox.warning(self.register_view, "Error", message)