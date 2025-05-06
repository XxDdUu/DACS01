from Frontend.View.Login import Login
from Frontend.View.register import Register
from Backend.Controller.EmployerController import EmployerController
class MainController:
    def __init__(self):
        self.login_window = Login()
        self.register_window = Register()

        self.login_window.switch_to_register = self.show_register
        self.register_window.switch_to_login = self.show_login

        self.show_login()
        self.employer_controller = EmployerController(self.register_window)

    def show_login(self):
        self.register_window.hide()
        self.login_window.show()

    def show_register(self):
        self.login_window.hide()
        self.register_window.show() 
