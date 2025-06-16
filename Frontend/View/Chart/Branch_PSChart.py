import traceback

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from Backend.DAO.DatabaseConnection import get_connection


class PSBranchChart:
    def __init__(self, branch_name: str, emp_id, ent_id):
        self.branch_name = branch_name
        self.emp_id = emp_id
        self.ent_id = ent_id
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.plot_chart()

    def plot_chart(self):
        try:
            conn = get_connection()
            if not conn:
                self.show_no_data()
                return

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

            conn.close()

            # Kiểm tra dữ liệu trống
            if df_product_sale.empty or df_product.empty or df_branch.empty:
                print("One or more dataframes are empty")
                self.show_no_data()
                return

            # Merge dữ liệu
            df_merge1 = pd.merge(df_product_sale,
                                 df_product.drop(columns=["Branch_ID"], errors='ignore'),
                                 on="Product_ID",
                                 how="left")

            df_merge2 = pd.merge(df_merge1, df_branch, on="Branch_ID", how="left")

            if not df_merge2.empty:
                print(f"DEBUG - Branch names available: {df_merge2['Branch_name'].unique()}")

            # Group theo Product + Branch
            df_groupby = df_merge2.groupby(['Product_NAME', 'Branch_name'])['SALE_AMOUNT'].sum().reset_index(
                name="Sale_amount")

            # Lọc theo branch được yêu cầu
            df_filtered = df_groupby[df_groupby['Branch_name'] == self.branch_name]

            print(f"DEBUG - Filtered data for branch '{self.branch_name}': {len(df_filtered)} rows")

            self.ax.clear()

            if df_filtered.empty:
                self.show_no_data()
            else:
                name = df_filtered['Product_NAME']
                amount = df_filtered['Sale_amount']

                if amount.sum() == 0:
                    self.show_no_data()
                else:
                    # Vẽ pie chart
                    self.ax.pie(amount, labels=name, autopct='%1.1f%%', startangle=90)
                    self.ax.axis('equal')
                    self.ax.set_title(f"- Branch {self.branch_name} -")

                    # Lưu file (tùy chọn - có thể bỏ nếu không cần)
                    try:
                        self.figure.savefig(f"Frontend/View/img/PS_branch{self.branch_name}.png",
                                            bbox_inches='tight', dpi=100)
                    except Exception as save_error:
                        print(f"Could not save chart image: {save_error}")

            self.canvas.draw()

        except Exception as e:
            traceback.print_exc()
            print(f"Exception in plot_chart: {e}")
            self.show_no_data()

    def show_no_data(self):
        self.ax.clear()
        self.ax.text(0.5, 0.5, f"No data available\nfor Branch {self.branch_name}",
                     ha='center', va='center', fontsize=12)
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.axis('off')
        self.canvas.draw()