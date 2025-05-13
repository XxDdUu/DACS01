import traceback

import matplotlib.pyplot as plt
import pandas as pd
from PyQt6.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from Backend.DAO.DatabaseConnection import get_connection


class generalChart:
    def __init__(self):
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding,
                                   QSizePolicy.Policy.Expanding)

        self.plot_chart()

    def plot_chart(self):
        # test data
        branches = ['A', 'B', 'C', 'D', 'E']
        revenue = [2000.0, 4203.0, 10000.0, 9909.0, 3215.0]

        self.ax.clear()
        self.ax.bar(branches, revenue, color='skyblue')
        self.ax.set_title("Năm 2025")
        self.ax.set_xlabel("Chi nhánh")
        self.ax.set_ylabel("Doanh thu")

        self.canvas.draw()


class ProductChart:
    def __init__(self):
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.plot_chart()

    def plot_chart(self):
        # test data:
        try:
            conn = get_connection()
            if not conn:
                return False, "Failed to connect to DB"
            query =  "SELECT * FROM PRODUCT"
            product = pd.read_sql(query,conn)
            name = product['Product_NAME']
            amount = product['AMOUNT']

            self.ax.clear()
            self.ax.pie(amount, labels=name)
            self.ax.set_title("Product Sales 2025")

            self.canvas.draw()
        except Exception as e:
            traceback.print_exc()
            print(f"Exception: {e}")
