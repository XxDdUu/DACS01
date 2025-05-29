from itertools import product

from PyQt6.QtWidgets import QMessageBox
from Backend.DAO.BranchesDAO import BranchesDAO
from Backend.DAO.ProductDAO import ProductDAO
from PyQt6.QtCore import QObject, pyqtSignal, QSortFilterProxyModel


class ProductController(QObject):
    product_data_changed = pyqtSignal()
    def __init__(self,distribution_view, add_product_view = None):
        super().__init__()
        self.add_product_view = add_product_view
        self.distribution_view = distribution_view
        self.branch_id_list = []
        self.product_dao = ProductDAO()
        self.distribution_view.product_add_btn.clicked.connect(lambda: [self.add_product_view.show(), self.add_product_view.main_widget.setCurrentWidget(self.add_product_view.manage_product)])
        self.add_product_view.product_update_and_add_button.clicked.connect(self.handle_add_and_update_product)
        self.distribution_view.product_remove_btn.clicked.connect(self.handle_remove_product)
        # self.distribution_view.prod_update_btn.clicked.connect(self.handle_update_button)
    def handle_add_and_update_product(self):
        if self.add_product_view.product_update_and_add_button.text() == "Add":
            data = self.add_product_view.get_productForm_data()
            success, message = self.product_dao.insert_product(data)
            if success:
                QMessageBox.information(self.add_product_view, "Success", message)
                self.product_data_changed.emit()
                self.distribution_view.display_branch_table()
                self.distribution_view.display_PS_table()
                self.distribution_view.display_revenue_table()
                self.distribution_view.display_top_product_table()
            else:
                QMessageBox.warning(self.add_product_view, "Error", message)
        else:
            data = self.add_product_view.get_productForm_data()
            print(data)
            success, message = self.product_dao.update_product(data)
            if success:
                QMessageBox.information(self.add_product_view, "Success", message)
                self.product_data_changed.emit()
                self.distribution_view.display_branch_table()
                self.distribution_view.display_PS_table()
                self.distribution_view.display_revenue_table()
                self.distribution_view.display_top_product_table()
            else:
                QMessageBox.warning(self.add_product_view, "Error", message)

    def handle_remove_product(self):
        # Lấy dữ liệu từ distribution_view hoặc bảng được chọn
        selected_indexes = self.distribution_view.product_data_table.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.warning(self.distribution_view, "Warning", "Please select a product to delete")
            return

        row = selected_indexes[0].row()
        model = self.distribution_view.product_data_table.model()

        # Tạo dictionary dữ liệu
        data = {}
        if isinstance(model, QSortFilterProxyModel):
            # Sử dụng index() và data() cho QSortFilterProxyModel
            data = {
                "id": str(model.data(model.index(row, 0))),
                "name": str(model.data(model.index(row, 1))),
                "price": str(model.data(model.index(row, 2))),
                "amount": str(model.data(model.index(row, 3))),
                "branch_id": str(model.data(model.index(row, 4)))
            }
        else:
            # Sử dụng item() cho QStandardItemModel
            data = {
                "id": model.item(row, 0).text(),
                "name": model.item(row, 1).text(),
                "price": model.item(row, 2).text(),
                "amount": model.item(row, 3).text(),
                "branch_id": model.item(row, 4).text()
            }
        print("DEBUG: Data passed to remove_product:", data)

        # Gọi DAO để xóa
        success, message = self.product_dao.remove_product(data)
        if success:
            QMessageBox.information(self.distribution_view, "Success", message)
            self.product_data_changed.emit()
            self.distribution_view.display_branch_table()
            self.distribution_view.display_PS_table()
            self.distribution_view.display_revenue_table()
            self.distribution_view.display_top_product_table()
        else:
            QMessageBox.warning(self.distribution_view, "Error", message)
    def add_branch_id_to_combobox(self): 
        if self.branch_id_list:
            self.add_product_view.branch_id_combo_box.clear()
            self.add_product_view.branch_id_combo_box.addItems(self.branch_id_list)
    def get_products(self,employer_id, enterprise_id):
        return self.product_dao.get_product_by_account(employer_id,enterprise_id)
    def get_top_products(self, enterprise_id):
        return self.product_dao.get_top_product_table_by_account(enterprise_id)
