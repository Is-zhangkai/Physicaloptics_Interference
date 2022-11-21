# -*- coding: utf-8 -*-
# @Time    : 2022/11/13 21:12
# @Author  : zhangkai
# @File    : Function.py
# @Software: PyCharm


import matplotlib
import numpy as np

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def Interference(mylambda=532e-6, z=30, reflectivity=0.9):
    """
    球面波干涉——FP干涉仪（透射）
    :param mylambda: 波长
    :param z: 传播距离
    :param reflectivity:  反射率
    :return: XX,YY,I,xx,Ic
    """

    k = 2 * np.pi / mylambda  #
    A0 = 1

    Lx = 5  # 接收屏
    Ly = 5
    dd = 3e-3  # 像素大小
    xx = np.arange(-Lx / 2, (Lx / 2) + dd, dd)
    yy = np.arange(-Ly / 2, (Ly / 2) + dd, dd)
    XX, YY = np.meshgrid(xx, yy)

    # 入射光
    RR = np.sqrt(XX ** 2 + YY ** 2 + z ** 2)  # 入射
    E0 = A0 * np.exp(1j * k * RR)
    I0 = np.abs(E0 **2)


    #第一次透射
    A = A0 * (1 - reflectivity)

    E = A * np.exp(1j * k * RR)

    #后续透射
    for i in range(6):
        z = z + 0.5
        RR = np.sqrt(XX ** 2 + YY ** 2 + z ** 2)
        A = reflectivity * A
        E1 = A * np.exp(1j * k * RR)
        E = E + E1


    I = np.abs(E **2)
    # print(np.max(np.exp(1j * k * RR)))
    Ic = I[int(len(yy) / 2)] / I0[int(len(yy) / 2)]
    return XX, YY, I, xx, Ic
