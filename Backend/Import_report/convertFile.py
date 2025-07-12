import traceback

import pandas as pd
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from docxtpl import DocxTemplate, InlineImage
from matplotlib.backends.backend_template import FigureCanvas

from Backend.DAO.DatabaseConnection import get_connection
from Frontend.View.Chart.Branch_PSChart import PSBranchChart
from Frontend.View.Chart.PSGeneralChart import ProductSaleChart
from Frontend.View.Chart.RevenueGeneralChart import RevenueGeneralChart


class ExportReportFile:
    def __init__(self, main_view):
        self.main_view = main_view
        self.emp_id = main_view.employer_data.ID
        self.ent_id = main_view.employer_data.enterprise_id
        self.main_view.export_word_btn.clicked.connect(self.export_file)
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
        WHERE 
            b.Employer_ID = %s AND b.Enterprise_ID = %s
        GROUP BY
            p.Product_NAME, b.Branch_name, p.PRICE, ps.QUANTITY_SOLD, ps.SALE_DATE
        ORDER BY
            total_revenue DESC;
            """
            df = pd.read_sql(query, conn, params=[self.emp_id,self.ent_id])
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
            figure.savefig("Frontend/View/img/PS_chart.png")

            context = {
                "reportDtStr": "29, Oct 2025",
                "salesTblRows": sales_rows,
                "topItemsRows": top_items,
                "trendImg": InlineImage(doc, "Frontend/View/img/PS_chart.png")
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
