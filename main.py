import sys
from PyQt6.QtWidgets import QApplication
from Backend.Controller.MainController import MainController
print("App starting...")
if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        controller = MainController()
        sys.exit(app.exec())
    except Exception as e:
        print("{e}")