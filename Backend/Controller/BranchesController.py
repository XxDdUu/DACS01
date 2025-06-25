from PyQt6.QtWidgets import QMessageBox
from Backend.DAO.BranchesDAO import BranchesDAO
from PyQt6.QtCore import QObject, pyqtSignal, QSortFilterProxyModel


class BranchesController(QObject):
    branch_data_changed = pyqtSignal()

    def __init__(self,distribution_view, add_branch_view = None):
        super().__init__()
        self.distribution_view = distribution_view
        self.add_branch_view = add_branch_view
        self.branches_dao = BranchesDAO()
        self.branch_data = []
        self.distribution_view.branch_add_btn.clicked.connect(lambda: [self.add_branch_view.show(), self.add_branch_view.main_widget.setCurrentWidget(self.add_branch_view.manage_branches)])    
        self.add_branch_view.branch_update_and_add_button.clicked.connect(self.handle_add_and_update_branch)
        self.distribution_view.branch_remove_btn.clicked.connect(self.handle_remove_branch)
    def handle_add_and_update_branch(self):
        if self.add_branch_view.branch_update_and_add_button.text() == "Add":
            data = self.add_branch_view.get_branchesForm_data()
            enterprise_id = self.distribution_view.employer_data.enterprise_id
            employer_id = self.distribution_view.employer_data.ID
            success, message = self.branches_dao.insert_branches(data, enterprise_id, employer_id)
            if success:
                QMessageBox.information(self.add_branch_view, "Success", message)
                self.branch_data_changed.emit()
                self.distribution_view.display_product_table()
                self.distribution_view.display_PS_table()
                self.distribution_view.display_revenue_table()
                self.distribution_view.display_top_product_table()
            else:
                QMessageBox.warning(self.add_branch_view, "Error", message)
        else:
            data = self.add_branch_view.get_branchesForm_data()
            success, message = self.branches_dao.update_branches(data)
            if success:
                QMessageBox.information(self.add_branch_view, "Success", message)
                self.branch_data_changed.emit()
                self.distribution_view.display_product_table()
                self.distribution_view.display_PS_table()
                self.distribution_view.display_revenue_table()
                self.distribution_view.display_top_product_table()
            else:
                QMessageBox.warning(self.add_branch_view, "Error", message)

    def handle_remove_branch(self):
        # Lấy dữ liệu từ distribution_view hoặc bảng được chọn
        selected_indexes = self.distribution_view.branchData_table.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.warning(self.distribution_view, "Warning", "Please select a product to delete")
            return

        row = selected_indexes[0].row()
        model = self.distribution_view.branchData_table.model()

        # Tạo dictionary dữ liệu
        data = {}
        if isinstance(model, QSortFilterProxyModel):
            # Sử dụng index() và data() cho QSortFilterProxyModel
            data = {
                "id": str(model.data(model.index(row, 0))),
                "employer_id": str(model.data(model.index(row, 5))),
                "enterprise_id": str(model.data(model.index(row, 6)))
            }
        else:
            # Sử dụng item() cho QStandardItemModel
            data = {
                "id": model.item(row, 0).text(),
                "employer_id": model.item(row, 5).text(),
                "enterprise_id": model.item(row, 6).text()
            }
        success, message = self.branches_dao.remove_branches(data)
        if success:
            QMessageBox.information(self.distribution_view, "Success", message)
            self.branch_data_changed.emit()
            self.distribution_view.display_product_table()
            self.distribution_view.display_PS_table()
            self.distribution_view.display_revenue_table()
            self.distribution_view.display_top_product_table()
        else:
            QMessageBox.warning(self.distribution_view, "Error", message)
    def handle_update_button(self):
        data = self.distribution_view.get_branchesForm_data()
        success, message = self.branches_dao.update_branches(data)
        if success:
            QMessageBox.information(self.distribution_view, "Success", message)
        else:
            QMessageBox.warning(self.distribution_view, "Error", message)
    def get_branches(self, enterprise_id, employer_id):
        return self.branches_dao.get_branches_by_enterprise_employer(enterprise_id, employer_id)
    def display_top_branch(self):
        pass
    def refresh_branches_ui(self):
        data = self.get_branches_data(enterprise_id, employer_id)
        self.view.update_branch_table(data)