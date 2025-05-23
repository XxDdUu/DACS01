import traceback
from functools import partial
from operator import index

from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtCore import Qt, QPoint, QEvent, QDate
import sys
import Frontend.View.resources_rc
from datetime import datetime

class DashBoard(QMainWindow):
	def __init__(self, employer_data, controller):
		super().__init__()
		self.controller = controller
		self.employer_data = employer_data
		uic.loadUi("Frontend/dashboardUI.ui", self)
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
		self.setWindowIcon(QIcon("Frontend/View/img/logo/dark_pythonLogo.png"))

		self.close_btn.clicked.connect(self.exit_window)
		self.maximize_btn.clicked.connect(self.toggle_maximize)
		self.minimize_btn.clicked.connect(self.showMinimized)
		self.is_maximized = False

		self._drag_active = False
		self._drag_position = QPoint()

		self.header.mouseMoveEvent = self.mouse_move_event
		self.header.mousePressEvent = self.mouse_press_event
		self.header.mouseReleaseEvent = self.mouse_release_event

		self.fetch_account_info(employer_data)
		self.switch_stackWidget()
		self.switch_to_login = None
		self.logout_label.clicked.connect(self.handle_to_logoutLabel)

	def handle_to_logoutLabel(self):
		if self.switch_to_login:
			self.switch_to_login()

	def switch_stackWidget(self):
		try:
			print(">>> switch_stackWidget() called")
			self.stackedWidget.setCurrentIndex(5)  # Page xuất hiện ban đầu sau khi login
			menuButton_list = [self.account_setting_btn,
							   self.revenue_btn,
							   self.productSales_menu_btn,
							   self.distribution_btn,
							   self.report_btn,
							   self.home_btn]

			for i,menu_btn in enumerate(menuButton_list):
				menu_btn.clicked.connect(lambda checked, index=i: self.stackedWidget.setCurrentIndex(index))
		except Exception as e:
			traceback.print_exc()
			print(f"Exception: {e}")

	def exit_window(self):
		self.close()
	def toggle_maximize(self):
		if self.is_maximized:
			self.showNormal()
		else:
			self.showMaximized()
		self.is_maximized = True
	def mouse_press_event(self, event):
		if event.button() == Qt.MouseButton.LeftButton:
			self._drag_active = True
			self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
			event.accept()
	def mouse_release_event(self, event):
		self._drag_active = False
	def mouse_move_event(self, event):
		if self._drag_active and event.buttons() == Qt.MouseButton.LeftButton:
			self.move(event.globalPosition().toPoint() - self._drag_position)
			event.accept()

	def fetch_account_info(self, employer_data):
		self.employer_name_lineedit.setText(employer_data.username)

		formatted_str = employer_data.create_at_time.strftime("%H:%M:%S %d/%m/%Y")

		self.display_create_date.setText("Join date: " + formatted_str)
		self.email_line_edit.setText(employer_data.email)
		self.Phone_number_lineedit.setText(employer_data.phone_number)
		self.enterprise_id_line_edit.setText(employer_data.enterprise_id)
		birthdate = self.employer_data.date_of_birth
		qbirthdate = QDate(birthdate.year, birthdate.month, birthdate.day)
		self.dateEdit.setDate(qbirthdate)