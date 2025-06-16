import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class ProductAmountChart(FigureCanvas):
    def __init__(self):
        self.figure, self.ax = plt.subplots()
        super().__init__(self.figure)

    def plot(self, data):
        self.ax.clear()

        names = [row[0] for row in data]
        amounts = [row[1] for row in data]

        bars = self.ax.bar(names, amounts, color='#7BAFD4', edgecolor='black')  # màu dễ nhìn

        self.ax.set_title("📦 Amount of product by name", fontsize=10, fontweight='bold')
        self.ax.set_xlabel("Product name", fontsize=9)
        self.ax.set_ylabel("Amount", fontsize=9)
        self.ax.tick_params(axis='x', rotation=30, labelsize=8)
        self.ax.grid(True, axis='y', linestyle='--', alpha=0.6)

        # Hiển thị nhãn số lượng trên từng cột
        for bar in bars:
            height = bar.get_height()
            self.ax.annotate(f'{int(height)}',
                             xy=(bar.get_x() + bar.get_width() / 2, height),
                             xytext=(0, 3),  # khoảng cách giữa nhãn và cột
                             textcoords="offset points",
                             ha='center', va='bottom', fontsize=9, color='black')

        self.figure.tight_layout(pad=1.5)
        self.draw()