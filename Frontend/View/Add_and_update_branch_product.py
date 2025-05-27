from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QApplication, QMainWindow, QAbstractSpinBox, QMessageBox
from PyQt6.QtCore import Qt, QPoint, QEvent, QDate, QPropertyAnimation, QEasingCurve, QRect
import sys
import Frontend.View.resources_rc
from datetime import datetime
import traceback

class Add_and_update_branch_product(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		uic.loadUi("Frontend/add_branch_and_product.ui", self)
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

		self.close_btn.clicked.connect(self.confirm_exit)
		self.maximize_btn.clicked.connect(self.toggle_maximize)
		self.minimize_btn.clicked.connect(self.showMinimized)
		self.is_maximized = False

		self._drag_active = False
		self._drag_position = QPoint()

		self.branch_id_line_edit.setMaximumHeight(0)
		self.branch_id_expanded = False
		try:
			self.update_and_add_label.clicked.disconnect()
		except TypeError:
				pass
		print("Connecting clicked signal now")
		self.update_and_add_label.clicked.connect(self.on_update_and_add_label_clicked)

	def toggle_maximize(self):
		if self.is_maximized:
			self.showNormal()
		else:
			self.showMaximized()
		self.is_maximized = not self.is_maximized
	def confirm_exit(self):
		qm = QMessageBox
		res = qm.question(self, 'Confirm', 'Are you sure to exit?', qm.StandardButton.Yes | qm.StandardButton.No)
		if res == qm.StandardButton.Yes:
			self.close()

	def on_update_and_add_label_clicked(self):
		print("label clicked")
		self.toggle_branch_id()
		self.switch_add_and_update()

	def toggle_branch_id(self):
		print("toggle_branch_id triggered")

		current_height = self.branch_id_line_edit.maximumHeight()
		new_height = 0 if self.branch_id_expanded else 40

		self.branch_id_line_edit.setMinimumHeight(new_height)
		self.branch_id_line_edit.setMaximumHeight(new_height)

		self.branch_id_expanded = not self.branch_id_expanded

	def switch_add_and_update(self):
		if self.update_and_add_label.text() == "Update branch info? Click here":
			# Currently in ADD mode, switch to UPDATE
			self.update_and_add_label.setText("Add branch info")
			self.Manage_branch_info_label.setText("Update branch info")
			self.update_and_add_button.setText("Update")
		else:
			# Currently in UPDATE mode, switch to ADD
			self.update_and_add_label.setText("Update branch info? Click here")
			self.Manage_branch_info_label.setText("Add branch info")
			self.update_and_add_button.setText("Add")
	def get_branchesForm_data(self):
		return {
			"id": self.branch_id_line_edit.text().strip(),
			"name": self.branch_name_line_edit.text().strip(),
			"address": self.branch_address_line_edit.text().strip(),
			"phone_number": self.branch_phone_num_line_edit.text().strip(),
		}