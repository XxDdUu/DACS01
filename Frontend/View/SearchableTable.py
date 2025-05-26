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
        # super().__init__()
        # self.setWindowTitle("QTableView + Search Example")
        # self.resize(600, 400)
        #
        # layout = QVBoxLayout(self)
        #
        # # Thanh tìm kiếm
        # self.search_bar = QLineEdit()
        # self.search_bar.setPlaceholderText("Nhập từ khóa để tìm kiếm...")
        # layout.addWidget(self.search_bar)
        #
        # # Table View
        # self.table_view = QTableView()
        # layout.addWidget(self.table_view)
        #
        # # Dữ liệu mẫu
        # self.model = QStandardItemModel()
        # self.model.setHorizontalHeaderLabels(["Họ", "Tên", "Tuổi"])
        #
        # data = [
        #     ["Nguyễn", "An", "25"],
        #     ["Trần", "Bình", "30"],
        #     ["Lê", "Cường", "22"],
        #     ["Phạm", "Dũng", "35"],
        #     ["Vũ", "Hà", "28"],
        # ]
        #
        # for row in data:
        #     items = [QStandardItem(field) for field in row]
        #     self.model.appendRow(items)
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
