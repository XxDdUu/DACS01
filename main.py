print("App starting...")
import sys
from PyQt6.QtWidgets import QApplication
from Backend.Controller.MainController import MainController
if __name__ == "__main__":
    def main():
        try:
            app = QApplication(sys.argv)
            controller = MainController()
            sys.exit(app.exec())
        except Exception as e:
            print(f"{e}")   
    main()

