from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QDateEdit
from PyQt6.QtCore import QEvent, QDate, QObject
import sys
class HoverEventFilter(QObject):
	def __init__(self, target_widget: list):
		super().__init__()
		self.target_widget = target_widget
	def eventFilter(self, source, event):
		if source.objectName() == "add_PS_btn" or "update_PS_btn":
			if event.type() == QEvent.Type.Enter:
				for widget in self.target_widget.values():
					widget.setStyleSheet("background-color: rgb(245, 245, 245); border-radius: 5px; border: 2px solid black;")
			elif event.type() == QEvent.Type.Leave:
				for widget in self.target_widget.values():
					widget.setStyleSheet("background-color: rgb(255, 255, 255); border-radius: 5px; border: 2px solid black;")
			return False