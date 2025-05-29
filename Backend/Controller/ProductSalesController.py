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
            self.distribution_view.display_branch_table()
            self.distribution_view.display_product_table()
            self.distribution_view.display_revenue_table()
            self.distribution_view.display_top_product_table()
            # self.dashboard_view.saleID_PS_le.clear()
            # self.dashboard_view.branch_id_PS_le.clear()
            # self.dashboard_view.prod_id_PS_le.clear()
            # self.dashboard_view.sale_qdate_edit.clear()
            # self.dashboard_view.quantitySold_PS_le.clear()
            # self.dashboard_view.saleAmount_PS_le.clear()
        else:
            QMessageBox.warning(self.dashboard_view, "Error", message)
    def handle_remove_button(self):
        data = self.dashboard_view.get_PSForm_data()
        success, message = self.PS_dao.remove_ProductSales(data)
        if success:
            QMessageBox.information(self.dashboard_view, "Success", message)
            self.ps_data_changed.emit()
            self.dashboard_view.display_branch_table()
            self.dashboard_view.display_product_table()
            self.dashboard_view.display_revenue_table()
            self.dashboard_view.display_top_product_table()
            # self.dashboard_view.saleID_PS_le.clear()
            # self.dashboard_view.branch_id_PS_le.clear()
            # self.dashboard_view.prod_id_PS_le.clear()
            # self.dashboard_view.sale_qdate_edit.clear()
            # self.dashboard_view.quantitySold_PS_le.clear()
            # self.dashboard_view.saleAmount_PS_le.clear()
        else:
            QMessageBox.warning(self.dashboard_view, "Error", message)
    def handle_update_button(self):
        data = self.dashboard_view.get_PSForm_data()
        success, message = self.PS_dao.update_ProductSales(data)
        if success:
            QMessageBox.information(self.dashboard_view, "Success", message)
            self.ps_data_changed.emit()
            self.dashboard_view.display_branch_table()
            self.dashboard_view.display_product_table()
            self.dashboard_view.display_revenue_table()
            self.dashboard_view.display_top_product_table()
            # self.dashboard_view.saleID_PS_le.clear()
            # self.dashboard_view.branch_id_PS_le.clear()
            # self.dashboard_view.prod_id_PS_le.clear()
            # self.dashboard_view.sale_qdate_edit.clear()
            # self.dashboard_view.quantitySold_PS_le.clear()
            # self.dashboard_view.saleAmount_PS_le.clear()
        else:
            QMessageBox.warning(self.dashboard_view, "Error", message)
    def get_product_sales(self,employer_id,enterprise_id):
        return self.PS_dao.get_product_sales_data(employer_id,enterprise_id)
