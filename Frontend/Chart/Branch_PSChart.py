import traceback

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_template import FigureCanvas

from Backend.DAO.DatabaseConnection import get_connection


class PSBranchChart:
    def __init__(self, branch_name: str):
        self.branch_name = branch_name
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.plot_chart()

    def plot_chart(self):
        try:
            conn = get_connection()
            if not conn:
                return False, "Failed to connect to DB"

            df_product_sale = pd.read_sql("SELECT * FROM PRODUCT_SALES", conn)
            df_product = pd.read_sql("SELECT * FROM PRODUCT", conn)
            df_branch = pd.read_sql("SELECT * FROM BRANCHES", conn)

            df_merge1 = pd.merge(df_product_sale, df_product.drop(columns=["Branch_ID"]), on="Product_ID", how="left")
            df_merge2 = pd.merge(df_merge1, df_branch, on="Branch_ID", how="left")

            # Group theo cả Product + Branch để đảm bảo giữ Branch_name
            df_groupby = df_merge2.groupby(['Product_NAME', 'Branch_name'])['SALE_AMOUNT'].sum().reset_index(name="Sale amount")

            # Lọc đúng branch được yêu cầu
            df_filtered = df_groupby[df_groupby['Branch_name'] == self.branch_name]

            name = df_filtered['Product_NAME']
            amount = df_filtered['Sale amount']

            self.ax.clear()
            if df_filtered.empty or amount.sum() == 0:
                self.ax.text(0.5, 0.5, "Không có dữ liệu", ha='center', va='center')
            else:
                self.ax.pie(amount, labels=name, autopct='%1.1f%%', startangle=90)
                self.ax.axis('equal')
                self.ax.set_title(f" - Branch {self.branch_name} -")
                self.figure.savefig(f"D:/PYTHON/DACS01/Frontend/View/img/PS_branch{self.branch_name}.png")
            self.canvas.draw()

        except Exception as e:
            traceback.print_exc()
            print(f"Exception: {e}")
