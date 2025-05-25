import traceback

import pandas as pd
from PyQt6.QtWidgets import QSizePolicy
from matplotlib import pyplot as plt
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from Backend.DAO.DatabaseConnection import get_connection


class generalChart:
    def __init__(self):
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.plot_chart()

    def plot_chart(self):
        try:
            conn = get_connection()
            if not conn:
                return False, "Failed to connect to DB"
            query = """
                   SELECT b.Branch_name, SUM(r.Amount) AS total_revenue
                   FROM REVENUE r
                   JOIN BRANCHES b ON r.Branch_ID = b.Branch_ID
                   GROUP BY b.Branch_name;
                   """

            df = pd.read_sql(query, conn)
            if df.empty or df['total_revenue'].sum() == 0:
                self.ax.text(0.5, 0.5, "Không có dữ liệu", ha='center', va='center')
            else:
                self.ax.clear()
                self.figure.set_size_inches(7,6)
                self.ax.set_title("Revenue General 2025")
                self.ax.bar(df['Branch_name'], df['total_revenue'], color='skyblue')
                self.ax.set_xlabel("Branch")
                self.ax.set_ylabel("Amount (unit: million$)")
                self.figure.savefig("D:/PYTHON/DACS01/Frontend/View/img/revenue_general_chart.png")
            self.canvas.draw()
        except Exception as e:
            traceback.print_exc()
            print(f"Exception: {e}")