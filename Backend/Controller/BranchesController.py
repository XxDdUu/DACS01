from PyQt6.QtWidgets import QMessageBox
from Backend.DAO.BranchesDAO import BranchesDAO


class BranchesController:
    def __init__(self,distribution_view):
        self.distribution_view = distribution_view
        self.branches_dao = BranchesDAO()
        self.distribution_view.branch_add_btn.clicked.connect(self.handle_add_button)
        self.distribution_view.branch_remove_btn.clicked.connect(self.handle_remove_button)
    def handle_add_button(self):
        data = self.distribution_view.get_branchesForm_data()
        enterprise_id = self.distribution_view.employer_data.enterprise_id
        employer_id = self.distribution_view.employer_data.ID
        print("[DEBUG] Form data:", data)  # Kiểm tra lại giá trị thực tế
        success, message = self.branches_dao.insert_branches(data, enterprise_id, employer_id)
        if success:
            QMessageBox.information(self.distribution_view, "Success", message)
        else:
            QMessageBox.warning(self.distribution_view, "Error", message)
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
        return self.branches_dao.get_branches(enterprise_id, employer_id)