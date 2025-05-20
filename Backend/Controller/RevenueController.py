from PyQt6.QtWidgets import QMessageBox

from Backend.DAO.RevenueDAO import RevenueDAO


class RevenueController:
    def __init__(self,revenue_view):
        self.revenue_view = revenue_view
        self.revenue_dao = RevenueDAO()
        # self.revenue_view.btn_add_Revenue.clicked.connect(self.handle_add_button)
        # self.revenue_view.btn_remove_Revenue.clicked.connect(self.handle_remove_button)
        # self.revenue_view.btn_update_Revenue.clicked.connect(self.handle_update_button)
    def handle_add_button(self):
        data = self.revenue_view.RFD.get_revenueForm_data()
        success, message = self.revenue_dao.create_revenue(data)
        if success:
            QMessageBox.information(self.revenue_view, "Success", message)
        else:
            QMessageBox.warning(self.revenue_view, "Error", message)
    def handle_remove_button(self):
        data = self.revenue_view.PFD.get_productForm_data()
        success, message = self.revenue_dao.remove_revenue(data)
        if success:
            QMessageBox.information(self.revenue_view, "Success", message)
        else:
            QMessageBox.warning(self.revenue_view, "Error", message)
    def handle_update_button(self):
        data = self.revenue_view.PFD.get_productForm_data()
        success, message = self.revenue_dao.update_revenue(data)
        if success:
            QMessageBox.information(self.revenue_view, "Success", message)
        else:
            QMessageBox.warning(self.revenue_view, "Error", message)
