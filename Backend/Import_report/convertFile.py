import traceback

import pandas as pd
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from docxtpl import DocxTemplate, InlineImage
from matplotlib.backends.backend_template import FigureCanvas

from Backend.DAO.DatabaseConnection import get_connection
from Frontend.Chart.Branch_PSChart import PSBranchChart
from Frontend.Chart.PSGeneralChart import ProductSaleChart
from Frontend.Chart.RevenueGeneralChart import generalChart


class ExportReportFile:
    def __init__(self, main_view):
        self.main_view = main_view
        self.main_view.export_report_btn.clicked.connect(self.export_file)
    def export_file(self):
        try:
            conn = get_connection()
            if not conn:
                print("Failed to connect DB!")

            query = """
        SELECT
            p.Product_NAME AS product_name,
            p.PRICE AS cost_per_unit,
            b.Branch_name AS branch_name,
            ps.SALE_DATE AS sale_date,
            ps.QUANTITY_SOLD AS units_sold,
            SUM(ps.SALE_AMOUNT) AS total_revenue
        FROM
            PRODUCT_SALES ps
        JOIN
            PRODUCT p ON ps.Product_ID = p.Product_ID
        JOIN
            BRANCHES b ON ps.Branch_ID = b.Branch_ID
        GROUP BY
            p.Product_NAME, b.Branch_name, p.PRICE, ps.QUANTITY_SOLD, ps.SALE_DATE
        ORDER BY
            total_revenue DESC;
            """
            df = pd.read_sql(query, conn)
            print(df)

            doc = DocxTemplate("Backend/Import_report/reportTmpl.docx")

            sales_rows = []
            for i, row in df.iterrows():
                sales_rows.append({"sNo": i,
                                   "name": row["product_name"],
                                   "cPu": row["cost_per_unit"],
                                   "nUnits": row["units_sold"],
                                   "revenue": row["total_revenue"],
                                   "bName": row["branch_name"]
                                   })

            top_df = df.sort_values("total_revenue", ascending=False).head(3)
            top_items = [row["product_name"] for _, row in top_df.iterrows()]

            figure, ax = plt.subplots()
            canvas = FigureCanvas(figure)
            ax.bar([x['name'] for x in sales_rows], [x['revenue'] for x in sales_rows], color='skyblue')
            ax.set_xlabel("Product")
            ax.set_ylabel("Revenue")
            figure.tight_layout()
            figure.savefig("D:/PYTHON/DACS01/Frontend/View/img/PS_chart.png")

            context = {
                "reportDtStr": "29, Oct 2025",
                "salesTblRows": sales_rows,
                "topItemsRows": top_items,
                "trendImg": InlineImage(doc, "D:/PYTHON/DACS01/Frontend/View/img/PS_chart.png")
            }
            doc.render(context)
            file_path, _ = QFileDialog.getSaveFileName(
                self.main_view,
                "Save Report File",
                "report.docx",
                "Word Document (*.docx);;All Files (*)"
            )

            if file_path:
                doc.save(file_path)
                QMessageBox.information(self.main_view, "Success", f"Save report at:\n{file_path}")

        except Exception as e:
            traceback.print_exc()
            print(f"Exception: {e}")

# class SaveChartImg:
#     def __init__(self):
#         self.figure, self.ax = plt.subplots()
#         self.save_revenue_general_chart()
#     def save_revenue_general_chart(self):
#         try:
#             conn = get_connection()
#             if not conn:
#                 return False, "Failed to connect to DB"
#             query = """
#                    SELECT b.Branch_name, SUM(r.Amount) AS total_revenue
#                    FROM REVENUE r
#                    JOIN BRANCHES b ON r.Branch_ID = b.Branch_ID
#                    GROUP BY b.Branch_name;
#                    """
#             df = pd.read_sql(query, conn)
#             if df.empty or df['total_revenue'].sum() == 0:
#                 self.ax.text(0.5, 0.5, "Không có dữ liệu", ha='center', va='center')
#             else:
#                 self.ax.set_title("Revenue General 2025")
#                 self.ax.bar(df['Branch_name'], df['total_revenue'], color='skyblue')
#                 self.ax.set_xlabel("Branch")
#                 self.ax.set_ylabel("Revenue (unit: million$)")
#                 self.figure.tight_layout()
#                 self.figure.savefig("D:/PYTHON/DACS01/Frontend/View/img/revenue_general_chart.png")
#         except Exception as e:
#             traceback.print_exc()
#             print(f"Exception: {e}")





