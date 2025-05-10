from PyQt6.QtWidgets import QMessageBox
from Backend.DAO.BranchesDAO import BranchesDAO
from Backend.DAO.ProductDAO import ProductDAO


class ManageProduct:
    def __init__(self,distribution_view):
        self.distribution_view = distribution_view
        self.product_dao = ProductDAO()
        self.distribution_view.add_btn1.clicked.connect(self.handle_add_button)
    def handle_add_button(self):
        data = self.distribution_view.PFD.get_productForm_data()
        self.product_dao.insert_product(data)
        success, message = self.product_dao.insert_product(data)
        if success:
            QMessageBox.information(self.distribution_view, "Success", message)
        else:
            QMessageBox.warning(self.distribution_view, "Error", message)