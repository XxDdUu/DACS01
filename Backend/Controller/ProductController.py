from PyQt6.QtWidgets import QMessageBox
from Backend.DAO.BranchesDAO import BranchesDAO
from Backend.DAO.ProductDAO import ProductDAO


class ManageProduct:
    def __init__(self,distribution_view):
        self.distribution_view = distribution_view
        self.product_dao = ProductDAO()
        self.distribution_view.prod_add_btn.clicked.connect(self.handle_add_button)
        self.distribution_view.prod_remove_btn.clicked.connect(self.handle_remove_button)
        self.distribution_view.prod_update_btn.clicked.connect(self.handle_update_button)
    def handle_add_button(self):
        data = self.distribution_view.PFD.get_productForm_data()
        success, message = self.product_dao.insert_product(data)
        if success:
            QMessageBox.information(self.distribution_view, "Success", message)
        else:
            QMessageBox.warning(self.distribution_view, "Error", message)
    def handle_remove_button(self):
        data = self.distribution_view.PFD.get_productForm_data()
        success, message = self.product_dao.remove_product(data)
        if success:
            QMessageBox.information(self.distribution_view, "Success", message)
        else:
            QMessageBox.warning(self.distribution_view, "Error", message)
    def handle_update_button(self):
        data = self.distribution_view.PFD.get_productForm_data()
        success, message = self.product_dao.update_product(data)
        if success:
            QMessageBox.information(self.distribution_view, "Success", message)
        else:
            QMessageBox.warning(self.distribution_view, "Error", message)
