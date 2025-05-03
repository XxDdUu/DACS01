import sys
from PyQt6.QtWidgets import QApplication
import sys
from pathlib import Path
from Backend.Controller.Controller import Controller

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    sys.exit(app.exec())