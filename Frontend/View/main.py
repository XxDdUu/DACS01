from PyQt6 import uic, QtWidgets
import sys

from PyQt6.QtWidgets import QApplication

app = QtWidgets.QApplication(sys.argv)

window = uic.loadUi("dashboardUI.ui")
window.show()

sys.exit(app.exec())