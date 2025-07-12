from PyQt6.QtWidgets import QMenu, QWidget, QPushButton, QVBoxLayout, QApplication
from PyQt6.QtGui import QAction
def create_main_menu(parent=None):
    menu = QMenu("☰ Menu", parent)

    profile = QAction("👤 Profile", parent)
    logout = QAction("🚪 Logout", parent)

    settings = QMenu("⚙ Settings", parent)
    
    theme = QMenu("🎨 Theme", parent)
    theme.addAction("🌙 Dark Mode")
    theme.addAction("☀️ Light Mode")

    settings.addMenu(theme)
    settings.addAction("🔐 Account")

    menu.addAction(profile)
    menu.addMenu(settings)
    menu.addSeparator()
    menu.addAction(logout)

    return menu
