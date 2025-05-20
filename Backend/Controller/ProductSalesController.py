from PyQt6.QtWidgets import QMessageBox

from Backend.DAO.ProductSalesDao import ProductSalesDAO
from Backend.Model.ProductSales import ProductSalesFormData


class ProductSalesController:
    def __init__(self, PS_view):
        self.PS_view = PS_view
        self.PS_dao = ProductSalesDAO()
        # self.PS_view.btn_add_PS.clicked.connect(self.handle_add_button)
        # self.PS_view.btn_remove_PS.clicked.connect(self.handle_remove_button)
        # self.PS_view.btn_update_PS.clicked.connect(self.handle_update_button)
    def handle_add_button(self):
        data = self.PS_view.PSFD.get_PSForm_data()
        success, message = self.PS_dao.add_ProductSales(data)
        if success:
            QMessageBox.information(self.PS_view, "Success", message)
        else:
            QMessageBox.warning(self.PS_view, "Error", message)
    def handle_remove_button(self):
        data = self.PS_view.PSFD.get_PSForm_data()
        success, message = self.PS_dao.remove_ProductSales(data)
        if success:
            QMessageBox.information(self.PS_view, "Success", message)
        else:
            QMessageBox.warning(self.PS_view, "Error", message)
    def handle_update_button(self):
        data = self.PS_view.PSFD.get_PSForm_data()
        success, message = self.PS_dao.update_ProductSales(data)
        if success:
            QMessageBox.information(self.PS_view, "Success", message)
        else:
            QMessageBox.warning(self.PS_view, "Error", message)
