import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


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
        products = ['iPhones', 'iMac', 'AirPods', 'iWatch', 'Tablets']
        quantity_sold = [9999, 7777, 8888, 6666, 5555]

        self.ax.clear()
        self.ax.pie(quantity_sold, labels=products)
        self.ax.set_title("Product Sales 2025")

        self.canvas.draw()
