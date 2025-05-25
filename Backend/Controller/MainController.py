from pyexpat.errors import messages

from Backend.Controller.BranchesController import BranchesController
from Backend.Controller.ProductController import ProductController
from Backend.Controller.ProductSalesController import ProductSalesController
from Backend.Controller.RevenueController import RevenueController
from Backend.Model.Employer import Employer
from Frontend.View.Login import Login
from Frontend.View.DashBoard import DashBoard
from Frontend.View.register import Register
from Backend.Controller.EmployerController import EmployerController, EmployerAccountSettingController
from Backend.Controller.EnterpriseController import EnterpriseController


class MainController:

    def __init__(self):
        self.login_window = Login()
        self.register_window = Register()

        self.login_window.switch_to_register = self.show_register
        self.register_window.switch_to_login = self.show_login
        self.login_window.switch_to_dashboardApp = self.show_dashboardApp

        self.show_login()
        self.employer_controller = EmployerController(self.register_window, self.login_window)
        self.enterprise_controller = EnterpriseController(self.register_window)
        self.branches_controller = None
        self.productSales_controller = None

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

            self.employer_controller = EmployerController(self.register_window, self.login_window)
            self.enterprise_controller = EnterpriseController(self.register_window)
            self.branches_controller = BranchesController(self.dashboard_window)
            self.product_controller = ProductController(self.dashboard_window)
            self.revenue_controller = RevenueController(self.dashboard_window)
            self.productSales_controller = ProductSalesController(self.dashboard_window)
            self.EmployerAccountSettingController = EmployerAccountSettingController(self.dashboard_window)

            self.enterprise_controller.set_dashboard(self.dashboard_window, employer_data)

            self.dashboard_window.switch_to_login = self.show_login

            try:
                print("Attempting to load Product Sales table...")
                self.dashboard_window.display_PS_table()
                print("Product Sales table loaded successfully")
            except Exception as e:
                print(f"ERROR loading Product Sales table: {e}")
                import traceback
                traceback.print_exc()

            self.login_window.hide()
            self.register_window.hide()
            self.dashboard_window.show()

        except Exception as e:
            print(f"ERROR in show_dashboardApp: {e}")
            import traceback
            traceback.print_exc()

    def get_branches_data(self, enterprise_id, employer_id):
        if self.branches_controller:
            return self.branches_controller.get_branches(enterprise_id, employer_id)

    def get_PS_data(self, employer_id, enterprise_id):
        if self.productSales_controller:
            return self.productSales_controller.get_product_sales(employer_id, enterprise_id)
        return []