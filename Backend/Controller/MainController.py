from pyexpat.errors import messages

from Backend.Controller.BranchesController import BranchesController
from Backend.Controller.ProductController import ProductController
from Backend.Controller.ProductSalesController import ProductSalesController
from Backend.Controller.RevenueController import RevenueController
from Backend.Import_report.convertFile import ExportReportFile
from Backend.Model.Employer import Employer
from Frontend.View.window.Login import Login
from Frontend.View.window.DashBoard import DashBoard
from Frontend.View.window.register import Register
from Backend.Controller.EmployerController import EmployerController, EmployerAccountSettingController
from Backend.Controller.EnterpriseController import EnterpriseController
from Frontend.View.window.Add_and_update_branch_product import Add_and_update_branch_product
from Frontend.View.window.LoadingWindow import LoadingWindow

class MainController:

    def __init__(self):
        self.login_window = Login()
        self.register_window = Register()

        self.login_window.switch_to_register = self.show_register
        self.register_window.switch_to_login = self.show_login
        self.login_window.switch_to_dashboardApp = self.switch_with_loading

        self.show_login()
        self.employer_controller = EmployerController(self.register_window, self.login_window)
        self.enterprise_controller = EnterpriseController(self.register_window)
        self.branches_controller = None
        self.productSales_controller = None
        self.product_controller = None
        self.revenue_controller = None

    def show_login(self):
        self.register_window.hide()
        self.login_window.show()

        if hasattr(self, "dashboard_window"):
            self.dashboard_window.hide()

    def show_register(self):
        self.login_window.hide()
        self.register_window.show()

    def show_dashboardApp(self, employer_data, enterprise_data):
        try:
            self.dashboard_window = DashBoard(self, employer_data)
            self.add_and_update_branch_product_window = Add_and_update_branch_product()

            self.employer_controller = EmployerController(self.register_window, self.login_window, self.switch_with_loading)
            self.enterprise_controller = EnterpriseController(self.register_window)
            self.branches_controller = BranchesController(self.dashboard_window, self.add_and_update_branch_product_window)
            self.product_controller = ProductController(self.dashboard_window, self.add_and_update_branch_product_window)
            self.revenue_controller = RevenueController(self.dashboard_window)
            self.productSales_controller = ProductSalesController(self.dashboard_window)
            self.EmployerAccountSettingController = EmployerAccountSettingController(self.dashboard_window)
            self.export_report_file = ExportReportFile(self.dashboard_window)

            self.enterprise_controller.set_dashboard(self.dashboard_window, employer_data)

            self.dashboard_window.switch_to_login = self.show_login

            self.login_window.hide()
            self.register_window.hide()
            self.dashboard_window.show()

            # Safely call display_data_table after controllers are set up
            try:
                self.dashboard_window.table_display.display_PS_table()
                self.dashboard_window.table_display.display_branch_table()
                self.dashboard_window.table_display.display_product_table()
                self.dashboard_window.table_display.display_top_product_table()
                self.dashboard_window.table_display.display_revenue_table()
                self.dashboard_window.display_amount_product_chart()
            except Exception as e:
                import traceback
                traceback.print_exc()

        except Exception as e:
            import traceback
            traceback.print_exc()
    def switch_with_loading(self, target, employer_data, enterprise_data):
        self.login_window.hide()
        self.register_window.hide()

        self.loading_window = LoadingWindow()
        self.loading_window.show()
        def after_loading():
            if target == "dashboard":
                self.show_dashboardApp(employer_data, enterprise_data)
                self.loading_window.hide()

        self.loading_window.start_loading(after_loading)

    def get_branches_data(self, enterprise_id, employer_id):
        if self.branches_controller:
            return self.branches_controller.get_branches(enterprise_id, employer_id)
        return []
    def get_PS_data(self, employer_id, enterprise_id):
        if self.productSales_controller:
            return self.productSales_controller.get_product_sales(employer_id, enterprise_id)
        return []
    def get_products_data(self, employer_id, enterprise_id):
        if self.product_controller:
            return self.product_controller.get_products(employer_id, enterprise_id)
        return []
    def get_revenues_data(self, employer_id, enterprise_id):
        if self.revenue_controller:
            return self.revenue_controller.get_revenues(employer_id,enterprise_id)
        return []
    def get_top_products_data(self, enterprise_id):
        if self.product_controller:
            return self.product_controller.get_top_products(enterprise_id)
        return []