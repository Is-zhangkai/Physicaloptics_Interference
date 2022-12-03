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
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QGridLayout, QGroupBox

from matplotlib.figure import Figure
from Interference import Ui_MainWindow
import matplotlib


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

        XX, YY, I, xx, Ic = fun.Interference(data["lambda"], data["distance"], data["reflectivity"])

        print(data)
        dic = {"label": data["label"], "XX": XX, "YY": YY, "I": I, "xx": xx, "Ic": Ic}
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

    def __init__(self, parent=None, axis=2,width=5.2, height=5.2, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=100)
        super(Figure_Canvas, self).__init__(self.fig)

        if axis==2:
            self.ax=self.fig.add_subplot(111)
        else:
            self.ax3 = self.fig.add_subplot(111,projection='3d')


class MainWindow(QMainWindow, Ui_MainWindow):
    finish_sinal = pyqtSignal(dict)  # 子线程向主线程发送数据的信号

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)

        self.SurfFigureLayout = QGridLayout(self.groupBox)

        self.btn_Show_FP.clicked.connect(self.Click_btn_show)
        self.btn_Show_FS.clicked.connect(self.Click_show_FS)
        # self.checkBox_defects.clicked.connect(self.Clicked_defects)

        self.finish_sinal.connect(self.ShowIm)
        self.thread = MyThread(self.finish_sinal)
        self.thread.mySignal.connect(self.thread.HandleImg)
        self.thread.start()

    @pyqtSlot()
    def Click_btn_show(self):
        label = self.comboBox_SelectImg.currentText()
        mylambda = int(self.et_lambda.text()) * 1e-6
        distance = int(self.et_distance.text())
        reflectivity = eval(self.et_reflectivity.text())

        datas = {"label": label, "lambda": mylambda, "distance": distance, "reflectivity": reflectivity}
        print(datas)
        self.thread.mySignal.emit(datas)


    def ShowIm(self, data):
        print("\r子线程已传回")
        if data["label"]=="干涉平面图":
            self.groupBox.setHidden(True)
            self.graphicsView.setHidden(False)
            I=data["I"]
            I = 255 * (I - np.min(I)) / (np.max(I) - np.min(I))
            I = np.uint8(I)
            self.show_image(I,self.graphicsView)

        elif data["label"]=="干涉三维图":
            self.graphicsView.setHidden(True)
            self.groupBox.setHidden(False)
            self.SurfFigure = Figure_Canvas(axis=3)
            self.SurfFigureLayout.addWidget(self.SurfFigure)
            self.SurfFigure.ax3.plot_surface(data["XX"], data["YY"], data["I"], rstride=9, cstride=9, antialiased=True,cmap='rainbow')
            self.SurfFigure.show()
            self.SurfFigureLayout.removeWidget(self.SurfFigure)
        else:
            self.groupBox.setHidden(True)
            self.graphicsView.setHidden(False)

            figture=Figure_Canvas()
            figture.ax.plot(data["xx"], data["Ic"], color='blue', linewidth=0.5, label="signalSrc")
            graphicscene = QGraphicsScene()
            graphicscene.addWidget(figture)
            self.graphicsView.setScene(graphicscene)
            self.graphicsView.show()




    def Click_show_FS(self):
        try:
            mylambda=int(self.et_lambda_fs.text())*1E-6
            A_A=float(self.et_AA_fs.text())
            Alpha_A=float(self.et_AAlpha_fs.text())
            Beta_A=float(self.et_ABeta_fs.text())
            z_A=float(self.et_Adistance_fs.text())
            A_B = float(self.et_BA_fs.text())
            Alpha_B = float(self.et_BAlpha_fs.text())
            Beta_B = float(self.et_BBeta_fs.text())
            z_B = float(self.et_Bdistance_fs.text())

            L = 3  # 接收屏
            dd = 2e-3  # 像素大小
            xx = np.arange(-L / 2, (L / 2), dd)
            XX, YY = np.meshgrid(xx, xx)
            if self.checkBox_defects.isChecked():

                sigma=0.16
                gaussian=np.exp(-((XX)**2+(YY)**2)/(2*sigma**2))/(2*np.pi*sigma**2)
                gaussian=gaussian*5E-5
                z_B=z_B+gaussian
                print(np.max(z_B))



            E1 = fun.plane_wave(mylambda, A_A, Alpha_A, Beta_A, z_A)
            E2 = fun.plane_wave(mylambda, A_B, Alpha_B, Beta_B, z_B)

            E = E1 + E2

            I = np.abs(E ** 2)
            I = 255 * (I - np.min(I)) / (np.max(I) - np.min(I))  # 调整范围
            I = np.uint8(I)

            if self.comboBox_SelectImg_fs.currentText()=="干涉平面图":
                self.groupBox.setHidden(True)
                self.graphicsView.setHidden(False)
                self.show_image(I,self.graphicsView)

            elif self.comboBox_SelectImg_fs.currentText()=="干涉三维图":
                self.graphicsView.setHidden(True)
                self.groupBox.setHidden(False)
                print("Sdfghs")
                self.SurfFigure = Figure_Canvas(axis=3)
                self.SurfFigureLayout.addWidget(self.SurfFigure)
                self.SurfFigure.ax3.plot_surface(XX,YY,I, rstride=9, cstride=9, antialiased=True,
                                                 cmap='rainbow')
                self.SurfFigure.show()
                self.SurfFigureLayout.removeWidget(self.SurfFigure)
            else:
                self.groupBox.setHidden(True)
                self.graphicsView.setHidden(False)

                ic=I[:,int(np.size(I,1)/2)]
                figture = Figure_Canvas()
                figture.ax.plot(xx,ic , color='blue', linewidth=0.5, label="signalSrc")
                graphicscene = QGraphicsScene()
                graphicscene.addWidget(figture)
                self.graphicsView.setScene(graphicscene)
                self.graphicsView.show()
        except:
            print("error:Click_show_FS")
    def show_image(self, img, view):
        flag = len(img.shape)
        if flag == 2:
            height, width = img.shape
            bytesPer = width
            imgQ = QImage(img.data, width, height, bytesPer, QImage.Format_Indexed8)
        else:
            height, width, ans = img.shape
            bytesPer = width * 3
            imgQ = QImage(img.data, width, height, bytesPer, QImage.Format_RGB888)

        imgQPixmap = QPixmap.fromImage(imgQ).scaledToWidth(view.width()-4)
        scene = QGraphicsScene()
        scene.addPixmap(imgQPixmap)
        view.setScene(scene)
        view.show()


    # def Clicked_defects(self):
    #     if self.checkBox_defects.isChecked():
    #         self.et_Bdistance_fs.setEnabled(False)
    #     else:
    #         self.et_Bdistance_fs.setEnabled(True)