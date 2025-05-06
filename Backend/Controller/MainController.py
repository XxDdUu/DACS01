from Frontend.View.Login import Login
from Frontend.View.mainDashboard import MainDashboard
from Frontend.View.register import Register
from Backend.Controller.EmployerController import EmployerController
class MainController:
    def __init__(self):
        self.login_window = Login()
        self.register_window = Register()
        self.dashboard_window = MainDashboard()

        self.login_window.switch_to_register = self.show_register
        self.register_window.switch_to_login = self.show_login
        self.login_window.switch_to_dashboardApp = self.show_dashboardApp

        self.show_login()
        self.employer_controller = EmployerController(self.register_window)

    def show_login(self):
        self.register_window.hide()
        self.login_window.show()
        self.dashboard_window.hide()

    def show_register(self):
        self.login_window.hide()
        self.register_window.show()
        self.dashboard_window.hide()

    def show_dashboardApp(self):
        self.login_window.hide()
        self.register_window.hide()
        self.dashboard_window.show()
