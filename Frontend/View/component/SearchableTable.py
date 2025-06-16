import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QTableView, QHeaderView
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt, QSortFilterProxyModel


class SearchableTable():
    def __init__(self,search_bar,data_table_view, object_model):
        self.search_bar = search_bar
        self.data_table_view = data_table_view
        self.object_model = object_model
        self.proxy_model = QSortFilterProxyModel()
    def search_function(self):
        # Proxy model cho tìm kiếm
        self.proxy_model.setSourceModel(self.object_model)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.proxy_model.setFilterKeyColumn(-1)  # -1 = tìm trong tất cả các cột

        self.data_table_view.setModel(self.proxy_model)
        self.data_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Kết nối thanh tìm kiếm
        self.search_bar.textChanged.connect(self.proxy_model.setFilterFixedString)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SearchableTable()
    window.show()
    sys.exit(app.exec())
