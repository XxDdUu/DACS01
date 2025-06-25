import os
import traceback
from itertools import product

from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QApplication, QMainWindow, QAbstractSpinBox, QMessageBox, QFrame, QVBoxLayout
from PyQt6.QtCore import Qt, QPoint, QEvent, QDate, QPropertyAnimation, QEasingCurve, QRect
import sys

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import Frontend.View.resource.resources_rc
from datetime import datetime

from Frontend.View.Chart.Branch_PSChart import PSBranchChart
from Frontend.View.Chart.RevenueGeneralChart import RevenueGeneralChart
from Frontend.View.component.SearchableTable import SearchableTable
from Frontend.View.helper.EventFilter import HoverEventFilter
from Frontend.View.Chart.ProductAmountChart import ProductAmountChart
from Frontend.View.component.DisplayTableInDashBoard import DisplayTableInDashBoard

class DashBoard(QMainWindow):
	def __init__(self, controller,employer_data = None, enterprise_data = None):
		super().__init__()
		self.controller = controller
		self.employer_data = employer_data
		self.enterprise_data = enterprise_data
		uic.loadUi("Frontend/View/ui/dashboardUI.ui", self)
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
		self.setWindowIcon(QIcon("Frontend/View/img/logo/dark_pythonLogo.png"))

		self.close_btn.clicked.connect(self.exit_window)
		self.maximize_btn.clicked.connect(self.toggle_maximize)
		self.minimize_btn.clicked.connect(self.showMinimized)
		self.is_maximized = False

		self._drag_active = False
		self._drag_position = QPoint()

		self.fetch_account_info(employer_data)
		self.active_switch_pages()

		self.product_amount_chart = ProductAmountChart()

		self.menu_expanded = False
		self.left_menu_animation = QPropertyAnimation(self.mainMenu, b"minimumWidth")
		self.left_menu_animation.setStartValue(self.mainMenu.width())
		self.left_menu_animation.setDuration(300)
		self.left_menu_animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
		self.btn_toggle_menu.clicked.connect(self.toggle_menu)
		self.sale_qdate_edit.setDate(QDate.currentDate())

		self.logout_label.clicked.connect(self.confirm_logout)
		self.canvas_draw_PS_chart()

		widgets_for_add_ps = {
			"sale_qdate": self.sale_qdate_edit,
			"quantity": self.quantitySold_PS_le,
			"prod_id": self.prod_id_PS_le,
			"branch_id": self.branch_id_PS_le
		}

		widgets_for_update_ps = {
			"sale_id" : self.saleID_PS_le,
			"sale_qdate": self.sale_qdate_edit,
			"quantity": self.quantitySold_PS_le,
			"prod_id": self.prod_id_PS_le,
			"branch_id": self.branch_id_PS_le
		}
		widgets_for_remove_ps = {
			"sale_id" : self.saleID_PS_le,
			"prod_id": self.prod_id_PS_le,
			"branch_id": self.branch_id_PS_le
		}

		self.hover_filter_add_ps = HoverEventFilter(widgets_for_add_ps)
		self.hover_filter_update_ps = HoverEventFilter(widgets_for_update_ps)
		self.hover_filter_remove_ps = HoverEventFilter(widgets_for_remove_ps)

		self.add_PS_btn.installEventFilter(self.hover_filter_add_ps)
		self.update_PS_btn.installEventFilter(self.hover_filter_update_ps)
		self.remove_PS_btn.installEventFilter(self.hover_filter_remove_ps)

		self.table_display = DisplayTableInDashBoard(self.controller, self, self.employer_data)

	def exit_window(self):
		self.close()
	def toggle_maximize(self):
		if self.is_maximized:
			self.showNormal()
		else:
			self.showMaximized()
		self.is_maximized = not self.is_maximized
	def mousePressEvent(self, event):
		focused_widget = self.focusWidget()
		if focused_widget is not None:
			focused_widget.clearFocus()
		super().mousePressEvent(event)

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

	def fetch_enterprise_info(self, enterprise_data):
		self.enterprise_name_line_edit.setText(enterprise_data.name)
		self.enterprise_founder_line_edit.setText(enterprise_data.founder)
		self.enterprise_address_line_edit.setText(enterprise_data.address)
		self.enterprise_phone_num_line_edit.setText(enterprise_data.phone_number)
		self.enterprise_bs_type_text_edit.setText(enterprise_data.type)
		self.enterprise_bs_type_text_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.enterprise_industry_line_edit.setText(enterprise_data.industry)

	def active_switch_pages(self):

		self.main_display_widget.setCurrentWidget(self.Home_page)
		self.home_btn.clicked.connect(lambda: self.main_display_widget.setCurrentWidget(self.Home_page))
		self.account_setting_btn.clicked.connect(lambda: self.main_display_widget.setCurrentWidget(self.Account_setting_page))
		self.revenue_btn.clicked.connect(lambda: self.main_display_widget.setCurrentWidget(self.Revenue_page))
		self.productSales_menu_btn.clicked.connect(lambda: self.main_display_widget.setCurrentWidget(self.Product_sale_page))
		self.distribution_btn.clicked.connect(lambda: self.main_display_widget.setCurrentWidget(self.Distribution_page))

		self.employer_and_enterpriseInfo.setCurrentWidget(self.employer_info)
		self.btn_enterprise_info.clicked.connect(lambda: self.employer_and_enterpriseInfo.setCurrentWidget(self.enterprise_info))
		self.btn_profile.clicked.connect(lambda: self.employer_and_enterpriseInfo.setCurrentWidget(self.employer_info))

	def toggle_menu(self):
		current_width = self.mainMenu.width()
		new_width = 44 if self.menu_expanded else 150
		if self.menu_expanded:
			self.logout_label.setText('<img src="Frontend/View/img/icon/icons8_logout_rounded_down.svg">')
		else:
			self.logout_label.setText('<img src="Frontend/View/img/icon/icons8_logout_rounded_down.svg" style="width:16px; height:16px; vertical-align:middle;"> Log out')

		self.left_menu_animation.setStartValue(current_width)
		self.left_menu_animation.setEndValue(new_width)
		self.left_menu_animation.start()

		self.menu_expanded = not self.menu_expanded

	def handle_logout(self):
		if self.switch_to_login:
			self.switch_to_login()

	def confirm_logout(self):
		qm = QMessageBox
		res = qm.question(self, 'Confirm', 'Are you sure to log out?', qm.StandardButton.Yes | qm.StandardButton.No)
		if res == qm.StandardButton.Yes:
			self.handle_logout()
	def get_PSForm_data(self):
		return {
			"id": self.saleID_PS_le.text().strip(),
			"branch_id": self.branch_id_PS_le.text().strip(),
			"product_id": self.prod_id_PS_le.text().strip(),
			"date": self.sale_qdate_edit.date().toString("yyyy-MM-dd"),
			"quantity_sold": self.quantitySold_PS_le.text().strip(),
		}
	def get_AccSetting_data(self):
		return {
			"employer_id": self.employer_data.ID,
			"username": self.employer_name_lineedit.text().strip(),
			"date_of_birth": self.dateEdit.date().toPyDate(),
			"email": self.email_line_edit.text().strip(),
			"phone_number": self.Phone_number_lineedit.text().strip(),
			"enterprise_id": self.enterprise_id_line_edit.text().strip()
		}
	def canvas_draw_PS_chart(self):
		# A, B, C là tên branch trong csdl bên này
		rev_general_chart = RevenueGeneralChart(self.employer_data)
		chartA = PSBranchChart("A",
							   self.employer_data.ID,
							   self.employer_data.enterprise_id)
		chartB = PSBranchChart("B",
							   self.employer_data.ID,
							   self.employer_data.enterprise_id)
		chartC = PSBranchChart("C",
							   self.employer_data.ID,
							   self.employer_data.enterprise_id)
		fig_revenueGeneral_chart = rev_general_chart.figure
		fig_PS_branchA_chart = chartA.figure
		fig_PS_branchB_chart = chartB.figure
		fig_PS_branchC_chart = chartC.figure

		canvas_RevenuePage = FigureCanvas(fig_revenueGeneral_chart)
		canvas_chart_left = FigureCanvas(fig_PS_branchA_chart)
		canvas_chart_center = FigureCanvas(fig_PS_branchB_chart)
		canvas_chart_right = FigureCanvas(fig_PS_branchC_chart)

		for frame in [self.frame_chart_1, self.frame_chart_2, self.frame_chart_3, self.frame_revenue_chart1]:
			if frame.layout() is None:
				frame.setLayout(QVBoxLayout())

		self.frame_revenue_chart1.layout().addWidget(canvas_RevenuePage)
		self.frame_chart_1.layout().addWidget(canvas_chart_left)
		self.frame_chart_2.layout().addWidget(canvas_chart_center)
		self.frame_chart_3.layout().addWidget(canvas_chart_right)

	def display_amount_product_chart(self):
		layout = QVBoxLayout()
		layout.addWidget(self.product_amount_chart)
		self.amount_product_chart_frame.setLayout(layout)
		self.controller.product_controller.update_amount_product_chart()
		if hasattr(self.controller, 'product_controller') and self.controller.product_controller:
			self.controller.product_controller.product_data_changed.connect(self.display_amount_product_chart)

		#setter method
	def set_employer_data(self, employer_data):
		self.employer_data = employer_data
	def set_enterprise_data(self, enterprise_data):
		self.enterprise_data = enterprise_data
