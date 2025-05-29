from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import QMessageBox

from Backend.DAO.RevenueDAO import RevenueDAO


class RevenueController(QObject):
    revenue_data_changed = pyqtSignal()
    def __init__(self,revenue_view):
        super().__init__()
        self.revenue_view = revenue_view
        self.revenue_dao = RevenueDAO()
        self.revenue_view.revenue_btn.clicked.connect(self.get_rev_triggered)
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
    def get_rev_triggered(self):
        emp_id = self.revenue_view.employer_data.ID
        ent_id = self.revenue_view.employer_data.enterprise_id
        success = self.get_revenues(emp_id,ent_id)
        if success:
            self.revenue_data_changed.emit()
        else:
            print("Can't run pyqtSignal")
    def get_revenues(self,employer_id,enterprise_id):
        return self.revenue_dao.get_revenue_data(employer_id,enterprise_id)


