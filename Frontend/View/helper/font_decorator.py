from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtWidgets import QWidget

def apply_font_to_widgets(font_family="Segoe UI", size=None):
	def decorator(func):
		def wrapper(self, *args, **kwargs):
			func(self, *args, **kwargs)
			if font_family not in QFontDatabase.families():
				print(f"Font {font_family} not found!")
				return
			if size is not None:
				font = QFont(font_family, size)
				_apply_font_recursively_with_font(self, font)
			else:
				_apply_font_recursively_change_family_only(self, font_family)
		return wrapper
	return decorator

def _apply_font_recursively_with_font(widget: QWidget, font: QFont):
    widget.setFont(font)
    for child in widget.findChildren(QWidget):
        child.setFont(font)

def _apply_font_recursively_change_family_only(widget: QWidget, font_family: str):
    font = widget.font()
    font.setFamily(font_family)
    widget.setFont(font)

    for child in widget.findChildren(QWidget):
        child_font = child.font()
        child_font.setFamily(font_family)
        child.setFont(child_font)