from PyQt6.QtWidgets import QMessageBox
from Backend.DAO.BranchesDAO import BranchesDAO
from PyQt6.QtCore import QObject, pyqtSignal

class BranchesController(QObject):
    data_changed = pyqtSignal()

    def __init__(self,distribution_view, add_branch_view = None):
        super().__init__()
        self.distribution_view = distribution_view
        self.add_branch_view = add_branch_view
        self.branches_dao = BranchesDAO()
        self.distribution_view.branch_add_btn.clicked.connect(lambda: [self.add_branch_view.show(), self.add_branch_view.main_widget.setCurrentWidget(self.add_branch_view.manage_branches)])
        self.distribution_view.product_add_btn.clicked.connect(lambda: [self.add_branch_view.show(), self.add_branch_view.main_widget.setCurrentWidget(self.add_branch_view.manage_product)])
        self.add_branch_view.update_and_add_button.clicked.connect(self.handle_add_and_update_branch)
        # self.distribution_view.branch_remove_btn.clicked.connect(self.handle_remove_button)
    def handle_add_and_update_branch(self):
        if self.add_branch_view.update_and_add_button.text() == "Add":
            data = self.add_branch_view.get_branchesForm_data()
            enterprise_id = self.distribution_view.employer_data.enterprise_id
            employer_id = self.distribution_view.employer_data.ID
            print("[DEBUG] Form data:", data)  # Kiểm tra lại giá trị thực tế
            success, message = self.branches_dao.insert_branches(data, enterprise_id, employer_id)
            if success:
                QMessageBox.information(self.add_branch_view, "Success", message)
                self.data_changed.emit()
            else:
                QMessageBox.warning(self.add_branch_view, "Error", message)
        else:
            data = self.add_branch_view.get_branchesForm_data()
            print(data)
            success, message = self.branches_dao.update_branches(data)
            if success:
                QMessageBox.information(self.add_branch_view, "Success", message)
                self.data_changed.emit()
            else:
                QMessageBox.warning(self.add_branch_view, "Error", message)

    def handle_remove_button(self):
        data = self.distribution_view.get_branchesForm_data()
        print("[DEBUG] Form data:", data)  # Kiểm tra lại giá trị thực tế
        success, message = self.branches_dao.remove_branches(data)
        if success:
            QMessageBox.information(self.distribution_view, "Success", message)
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
    def refresh_branches_ui(self):
        data = self.get_branches_data(enterprise_id, employer_id)
        self.view.update_branch_table(data)