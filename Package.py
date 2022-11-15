# -*- coding: utf-8 -*-
# @Time    : 2022/9/19 20:53
# @Author  : zhangkai
# @File    : Package.py
# @Software: PyCharm

"""



"""
import time

import numpy as np
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene
from matplotlib.figure import Figure
from Interference import Ui_MainWindow
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import matplotlib.ticker as tck

matplotlib.use("Qt5Agg")


class MyThread(QThread):
    """
    子线程函数
    """

    mySignal = pyqtSignal(str)  # 主线程向子线程发送数据的信号

    def __init__(self, singal):  # 传递主线程信号变量
        super().__init__()
        self.singal_su = singal

    def HandleImg(self, str):
        print("\r已启用子线程")
        print(str)

        time.sleep(1)
        self.singal_su.emit("success")

    def run(self):
        count = 1
        while True:

            print("子线程正在等待{}>".format("-" * count), end="")
            if count > 13:
                count = 0
            count += 1
            time.sleep(1)
            print("", end="\r")


class myFigureCanvas(FigureCanvas):
    # 通过继承连接pyqt5与matplot lib

    def __init__(self, parent=None, width=6, height=6):
        fig = Figure(figsize=(width, height), dpi=106)
        # 注意：Figure为matplotlib下的figure,导入from matplotlib.figure import Figure

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.axes = fig.add_subplot(111)


class MainWindow(QMainWindow, Ui_MainWindow):
    finish_sinal = pyqtSignal(str)  # 子线程向主线程发送数据的信号

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)
        self.pushButton.clicked.connect(self.Click_btn_display)
        self.finish_sinal.connect(self.ShowIm)
        self.thread = MyThread(self.finish_sinal)

        self.thread.mySignal.connect(self.thread.HandleImg)
        self.thread.start()

    @pyqtSlot()
    def Click_btn_display(self):
        self.thread.mySignal.emit("sdfgh")

    def ShowIm(self, success_info):
        print("\r子线程已传回")
        print(success_info)
