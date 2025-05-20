from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt, QPoint, QEvent
import sys
import Frontend.View.resources_rc

class DashBoard(QMainWindow):
	def __init__(self, employer_data, controller):
		super().__init__()
		self.controller = controller
		self.employer_data = employer_data
		uic.loadUi("Frontend/dashboardUI.ui", self)
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
