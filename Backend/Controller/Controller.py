from Frontend.View.Login import Login
from Frontend.View.mainDashboard import MainDashboard
from Frontend.View.register import Register

class Controller:
    def __init__(self):
        self.login_window = Login()
        self.register_window = Register()
        self.Dashboard_window = MainDashboard()

        self.login_window.switch_to_register = self.show_register
        self.register_window.switch_to_login = self.show_login
        self.login_window.switch_to_dashboardApp = self.showDashboard
        self.Dashboard_window.switch_to_login = self.show_login()

        self.show_login()
    def showDashboard(self):
        print("Chuyển qua Dashboard")
        self.Dashboard_window.show()
        self.Dashboard_window.activateWindow()
        self.login_window.hide()
        self.register_window.hide()

    def show_login(self):
        self.register_window.hide()
        self.login_window.show()
        self.Dashboard_window.hide()

    def show_register(self):
        self.login_window.hide()
        self.register_window.show()
        self.Dashboard_window.hide()
