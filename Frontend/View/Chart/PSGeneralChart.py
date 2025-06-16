import traceback

import pandas as pd
from PyQt6.QtWidgets import QSizePolicy
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from Backend.DAO.DatabaseConnection import get_connection

class ProductSaleChart:
    def __init__(self,emp_id = None , ent_id = None):
        self.emp_id = emp_id
        self.ent_id = ent_id
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.plot_chart()

    def plot_chart(self):
        try:
            conn = get_connection()
            if not conn:
                return False, "Failed to connect to DB"

            product_sale_query = """
                            SELECT ps.* FROM PRODUCT_SALES ps
                            JOIN BRANCHES b ON b.Branch_ID = ps.Branch_ID
                            WHERE Employer_ID = %s AND Enterprise_ID = %s
                        """

            product_query = """
                            SELECT p.* FROM PRODUCT p
                            JOIN BRANCHES b ON p.Branch_ID = b.Branch_ID 
                            WHERE Employer_ID = %s AND Enterprise_ID = %s
                        """

            branch_query = """
                            SELECT * FROM BRANCHES 
                            WHERE Employer_ID = %s AND Enterprise_ID = %s
                        """

            # Debug: In ra để kiểm tra
            print(f"DEBUG - emp_id: {self.emp_id}, ent_id: {self.ent_id}")

            # Lấy dữ liệu với parameters
            df_product_sale = pd.read_sql(product_sale_query, conn, params=[self.emp_id, self.ent_id])
            df_product = pd.read_sql(product_query, conn, params=[self.emp_id, self.ent_id])
            df_branch = pd.read_sql(branch_query, conn, params=[self.emp_id, self.ent_id])

            # Loại bỏ Branch_ID khỏi df_product để tránh bị đè
            df_merge1 = pd.merge(df_product_sale, df_product.drop(columns=["Branch_ID"]), on="Product_ID", how="left")

            # Bây giờ merge sẽ hoạt động bình thường
            df_merge2 = pd.merge(df_merge1, df_branch, on="Branch_ID", how="left")

            # Group by Product & Branch (bỏ SALE_DATE nếu không dùng theo ngày)
            df_groupby = df_merge2.groupby(['Product_NAME'])['SALE_AMOUNT'].sum().reset_index(name="Sale amount")

            # Lọc theo chi nhánh tên "A"
            # df_filtered = df_groupby[df_groupby['Branch_name'] == "A"]

            name = df_groupby['Product_NAME']
            amount = df_groupby['Sale amount']

            self.ax.clear()

            if df_groupby.empty or amount.sum() == 0:
                self.ax.text(0.5, 0.5, "Không có dữ liệu", ha='center', va='center')
            else:
                self.ax.pie(amount, labels=name, autopct='%1.1f%%', startangle=90)
                self.ax.axis('equal')
                self.ax.set_title("Product Sales 2025")
                self.figure.savefig("D:/PYTHON/DACS01/Frontend/View/img/PS_general.png")
            self.canvas.draw()

        except Exception as e:
            traceback.print_exc()
            print(f"Exception: {e}")

# if __name__ == '__main__':
#     x = ProductSaleChart(emp_id=3,ent_id='ENT_2UL4KYS')
#     x.plot_chart()