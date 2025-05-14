import traceback

import pandas as pd
from PyQt6.QtWidgets import QSizePolicy
from matplotlib import pyplot as plt
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from Backend.DAO.DatabaseConnection import get_connection

class PS_branchA_chart:
    def __init__(self):
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.plot_chart()

    def plot_chart(self):
        try:
            conn = get_connection()
            if not conn:
                return False, "Failed to connect to DB"

            # Đọc dữ liệu
            df_product_sale = pd.read_sql("SELECT * FROM PRODUCT_SALES", conn)
            df_product = pd.read_sql("SELECT * FROM PRODUCT", conn)
            df_branch = pd.read_sql("SELECT * FROM BRANCHES", conn)

            # Loại bỏ Branch_ID khỏi df_product để tránh bị đè
            df_merge1 = pd.merge(df_product_sale, df_product.drop(columns=["Branch_ID"]), on="Product_ID", how="left")

            # Bây giờ merge sẽ hoạt động bình thường
            df_merge2 = pd.merge(df_merge1, df_branch, on="Branch_ID", how="left")

            # Group by Product & Branch (bỏ SALE_DATE nếu không dùng theo ngày)
            df_groupby = df_merge2.groupby(['Product_NAME','Branch_NAME'])['SALE_AMOUNT'].sum().reset_index(name="Sale amount")

            # Lọc theo chi nhánh tên "A"
            df_filtered = df_groupby[df_groupby['Branch_name'] == "A"]

            name = df_groupby['Product_NAME']
            amount = df_groupby['Sale amount']

            self.ax.clear()

            if df_filtered.empty or amount.sum() == 0:
                self.ax.text(0.5, 0.5, "Không có dữ liệu", ha='center', va='center')
            else:
                self.ax.pie(amount, labels=name, autopct='%1.1f%%', startangle=90)
                self.ax.axis('equal')
                self.ax.set_title("Product Sales 2025")

            self.canvas.draw()

        except Exception as e:
            traceback.print_exc()
            print(f"Exception: {e}")
class PS_branchB_chart:
    def __init__(self):
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.plot_chart()

    def plot_chart(self):
        try:
            conn = get_connection()
            if not conn:
                return False, "Failed to connect to DB"

            # Đọc dữ liệu
            df_product_sale = pd.read_sql("SELECT * FROM PRODUCT_SALES", conn)
            df_product = pd.read_sql("SELECT * FROM PRODUCT", conn)
            df_branch = pd.read_sql("SELECT * FROM BRANCHES", conn)

            # Loại bỏ Branch_ID khỏi df_product để tránh bị đè
            df_merge1 = pd.merge(df_product_sale, df_product.drop(columns=["Branch_ID"]), on="Product_ID", how="left")

            # Bây giờ merge sẽ hoạt động bình thường
            df_merge2 = pd.merge(df_merge1, df_branch, on="Branch_ID", how="left")

            # Group by Product & Branch (bỏ SALE_DATE nếu không dùng theo ngày)
            df_groupby = df_merge2.groupby(['Product_NAME','Branch_NAME'])['SALE_AMOUNT'].sum().reset_index(name="Sale amount")

            # Lọc theo chi nhánh tên "A"
            df_filtered = df_groupby[df_groupby['Branch_name'] == "B"]

            name = df_groupby['Product_NAME']
            amount = df_groupby['Sale amount']

            self.ax.clear()

            if df_filtered.empty or amount.sum() == 0:
                self.ax.text(0.5, 0.5, "Không có dữ liệu", ha='center', va='center')
            else:
                self.ax.pie(amount, labels=name, autopct='%1.1f%%', startangle=90)
                self.ax.axis('equal')
                self.ax.set_title("Product Sales 2025")

            self.canvas.draw()

        except Exception as e:
            traceback.print_exc()
            print(f"Exception: {e}")
class PS_branchC_chart:
    def __init__(self):
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.plot_chart()

    def plot_chart(self):
        try:
            conn = get_connection()
            if not conn:
                return False, "Failed to connect to DB"

            # Đọc dữ liệu
            df_product_sale = pd.read_sql("SELECT * FROM PRODUCT_SALES", conn)
            df_product = pd.read_sql("SELECT * FROM PRODUCT", conn)
            df_branch = pd.read_sql("SELECT * FROM BRANCHES", conn)

            # Loại bỏ Branch_ID khỏi df_product để tránh bị đè
            df_merge1 = pd.merge(df_product_sale, df_product.drop(columns=["Branch_ID"]), on="Product_ID", how="left")

            # Bây giờ merge sẽ hoạt động bình thường
            df_merge2 = pd.merge(df_merge1, df_branch, on="Branch_ID", how="left")

            # Group by Product & Branch (bỏ SALE_DATE nếu không dùng theo ngày)
            df_groupby = df_merge2.groupby(['Product_NAME','Branch_NAME'])['SALE_AMOUNT'].sum().reset_index(name="Sale amount")

            # Lọc theo chi nhánh tên "A"
            df_filtered = df_groupby[df_groupby['Branch_name'] == "C"]

            name = df_groupby['Product_NAME']
            amount = df_groupby['Sale amount']

            self.ax.clear()

            if df_filtered.empty or amount.sum() == 0:
                self.ax.text(0.5, 0.5, "Không có dữ liệu", ha='center', va='center')
            else:
                self.ax.pie(amount, labels=name, autopct='%1.1f%%', startangle=90)
                self.ax.axis('equal')
                self.ax.set_title("Product Sales 2025")

            self.canvas.draw()

        except Exception as e:
            traceback.print_exc()
            print(f"Exception: {e}")