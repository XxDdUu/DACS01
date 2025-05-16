from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.QtWidgets import QApplication
import sys
import Frontend.View.resources_rc

class DashBoard(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		uic.loadUi("Frontend/dashboardUI.ui", self)
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
