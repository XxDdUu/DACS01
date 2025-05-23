from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt, QPoint, QEvent, QDate, QPropertyAnimation, QEasingCurve, QRect
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
		self.active_switch_pages()

		self.menu_expanded = False
		self.left_menu_animation = QPropertyAnimation(self.mainMenu, b"minimumWidth")
		self.left_menu_animation.setStartValue(self.mainMenu.width())
		self.left_menu_animation.setDuration(300)
		self.left_menu_animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
		self.btn_toggle_menu.clicked.connect(self.toggle_menu)

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
	def active_switch_pages(self):
		self.main_display_widget.setCurrentWidget(self.Home_page)
		self.home_btn.clicked.connect(lambda: self.main_display_widget.setCurrentWidget(self.Home_page))
		self.account_setting_btn.clicked.connect(lambda: self.main_display_widget.setCurrentWidget(self.Account_setting_page))
		self.revenue_btn.clicked.connect(lambda: self.main_display_widget.setCurrentWidget(self.Revenue_page))
		self.report_btn.clicked.connect(lambda: self.main_display_widget.setCurrentWidget(self.Report_page))
		self.productSales_menu_btn.clicked.connect(lambda: self.main_display_widget.setCurrentWidget(self.Product_sale_page))
		self.distribution_btn.clicked.connect(lambda: self.main_display_widget.setCurrentWidget(self.Distribution_page))
	
	def toggle_menu(self):
		current_width = self.mainMenu.width()
		new_width = 44 if self.menu_expanded else 150

		self.left_menu_animation.setStartValue(current_width)
		self.left_menu_animation.setEndValue(new_width)
		self.left_menu_animation.start()

		self.menu_expanded = not self.menu_expanded