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
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QGridLayout,QGroupBox
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from Interference import Ui_MainWindow
import matplotlib
from mpl_toolkits.mplot3d import Axes3D

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import Function as fun

matplotlib.use("Qt5Agg")


class MyThread(QThread):
    """
    子线程函数
    """

    mySignal = pyqtSignal(dict)  # 主线程向子线程发送数据的信号

    def __init__(self, singal):  # 传递主线程信号变量
        super().__init__()
        self.singal_su = singal

    def HandleImg(self, data):
        print("\r已启用子线程")

        XX,YY,I,xx,Ic=fun.Interference(data["lambda"],data["distance"],data["reflectivity"])

        print(data)
        dic={"label":data["label"],"XX":XX,"YY":YY,"I":I,"xx":xx,"Ic":Ic}
        self.singal_su.emit(dic)

    def run(self):
        count = 1
        while True:

            print("子线程正在等待{}>".format("-" * count), end="")
            if count > 13:
                count = 0
            count += 1
            time.sleep(1)
            print("", end="\r")


class Figure_Canvas(FigureCanvas):
    # 通过继承连接pyqt5与matplot lib

    def __init__(self,parent=None,width=3.9,height=2.7,dpi=100):
        self.fig=Figure(figsize=(width,height),dpi=100)
        super(Figure_Canvas,self).__init__(self.fig)
        # self.ax=self.fig.add_subplot(111)
        self.ax=self.fig.add_subplot(111,projection='3d')









class MainWindow(QMainWindow, Ui_MainWindow):
    finish_sinal = pyqtSignal(dict)  # 子线程向主线程发送数据的信号

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)


        self.setupUi(self)
        self.SurfFigure = Figure_Canvas()
        self.SurfFigureLayout = QGridLayout(self.groupBox)

        self.btn_Show_FP.clicked.connect(self.Click_btn_show)


        self.finish_sinal.connect(self.ShowIm)
        self.thread = MyThread(self.finish_sinal)
        self.thread.mySignal.connect(self.thread.HandleImg)
        self.thread.start()


    @pyqtSlot()
    def Click_btn_show(self):
        label=self.comboBox_SelectImg.currentText()
        mylambda=int(self.et_lambda.text())*1e-6
        distance=int(self.et_distance.text())
        reflectivity=eval(self.et_reflectivity.text())

        datas={"label":label,"lambda":mylambda,"distance":distance,"reflectivity":reflectivity}
        print(datas)
        self.thread.mySignal.emit(datas)

    def ShowIm(self, data):
        print("\r子线程已传回")

        print("Asac")

        self.SurfFigure = Figure_Canvas()
        self.SurfFigureLayout.addWidget(self.SurfFigure)
        self.SurfFigure.ax.plot_surface(data["XX"], data["YY"], data["I"], cmap='rainbow')
        self.SurfFigure.show()
        # Figure = Figure_Canvas()
        # FigureLayout = QGridLayout(self.groupBox)
        # FigureLayout.addWidget(Figure)
        #
        # Figure.ax.plot(data["xx"], data["Ic"])

        # Surf = Figure.ax.plot_surface(XX, YY, I, cmap='rainbow')

        self.SurfFigureLayout.removeWidget(self.SurfFigure)

