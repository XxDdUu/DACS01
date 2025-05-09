from PyQt6.QtWidgets import QMessageBox
from Backend.DAO.BranchesDAO import BranchesDAO


class ManageBranches:
    def __init__(self,distribution_view):
        self.distribution_view = distribution_view
        self.branches_dao = BranchesDAO()
        self.distribution_view.add_btn2.clicked.connect(self.handle_add_button)
    def handle_add_button(self):
        data = self.distribution_view.BFD.get_branchesForm_data()
        self.branches_dao.insert_branches(data)
        success, message = self.branches_dao.insert_branches(data)
        if success:
            QMessageBox.information(self.distribution_view, "Success", message)
        else:
            QMessageBox.warning(self.distribution_view, "Error", message)