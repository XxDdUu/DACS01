from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMessageBox

from Backend.DAO.ProductSalesDao import ProductSalesDAO

class ProductSalesController(QObject):
    ps_data_changed = pyqtSignal()
    def __init__(self,dashboard_view):
        super().__init__()
        self.PS_dao = ProductSalesDAO()
        self.dashboard_view = dashboard_view
        self.dashboard_view.add_PS_btn.clicked.connect(self.handle_add_button)
        self.dashboard_view.remove_PS_btn.clicked.connect(self.handle_remove_button)
        self.dashboard_view.update_PS_btn.clicked.connect(self.handle_update_button)
    def handle_add_button(self):
        data = self.dashboard_view.get_PSForm_data()
        success, message = self.PS_dao.add_ProductSales(data)
        if success:
            QMessageBox.information(self.dashboard_view, "Success", message)
            self.ps_data_changed.emit()
        else:
            QMessageBox.warning(self.dashboard_view, "Error", message)
    def handle_remove_button(self):
        data = self.dashboard_view.get_PSForm_data()
        success, message = self.PS_dao.remove_ProductSales(data)
        if success:
            QMessageBox.information(self.dashboard_view, "Success", message)
            self.ps_data_changed.emit()
        else:
            QMessageBox.warning(self.dashboard_view, "Error", message)
    def handle_update_button(self):
        data = self.dashboard_view.get_PSForm_data()
        success, message = self.PS_dao.update_ProductSales(data)
        if success:
            QMessageBox.information(self.dashboard_view, "Success", message)
            self.ps_data_changed.emit()
        else:
            QMessageBox.warning(self.dashboard_view, "Error", message)
    def get_product_sales(self,employer_id,enterprise_id):
        return self.PS_dao.get_product_sales_data(employer_id,enterprise_id)
