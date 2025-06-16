import traceback

from PyQt6.QtWidgets import QSizePolicy
from matplotlib import pyplot as plt
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from Backend.DAO.DatabaseConnection import get_connection

class RevenueFrom:
    def __init__(self):
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.plot_chart()