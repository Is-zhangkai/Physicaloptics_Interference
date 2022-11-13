# -*- coding: utf-8 -*-
# @Time    : 2022/11/12 15:39
# @Author  : zhangkai
# @File    : try.py
# @Software: PyCharm

import matplotlib
import numpy as np

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

mylambda = 532e-6       #波长
k = 2 * np.pi / mylambda        #
k1 = 2 * np.pi / 522e-6          #
A0 = 1
z0 = 30  # 传播距离
Lx = 5      #接收屏
Ly = 5
dd = 3e-3  # 像素大小
xx = np.arange(-Lx / 2, (Lx / 2)+dd, dd)
yy = np.arange(-Ly / 2, (Ly / 2)+dd, dd)
XX, YY = np.meshgrid(xx, yy)

RR = np.sqrt(XX ** 2 + YY ** 2 + z0 ** 2)

E0 = A0 * np.exp(1j * k * RR)
I0 = np.abs(E0 ** 2)



z = z0

A = A0*0.1*0.1
RR = np.sqrt(XX ** 2 + YY ** 2 + z ** 2)
E = A * np.exp(1j * k * RR)

for i in range(10):
    z = z + 0.5
    RR = np.sqrt(XX ** 2 + YY ** 2 + z ** 2)
    A = 0.9 *0.9* A
    E1 = A * np.exp(1j * k * RR)
    E = E + E1

z = z0

A = A0*0.1*0.1
RR = np.sqrt(XX ** 2 + YY ** 2 + z ** 2)
E = E+A * np.exp(1j * k1 * RR)

for i in range(10):
    z = z + 0.5
    RR = np.sqrt(XX ** 2 + YY ** 2 + z ** 2)
    A = 0.9 *0.9* A
    E1 = A * np.exp(1j * k1 * RR)
    E = E + E1







I = np.abs(E ** 2)



#
# plt.plot(xx,I[int(len(yy)/2)]/I0[int(len(yy)/2)])
# plt.show()



I=(I-np.min(I))*255/(np.max(I)-np.min(I))
# # 画出三维坐标系：
# axes = plt.axes(projection="3d")
# # 绘制曲面：
# axes.plot_surface(XX, YY, I, rstride=4, cstride=4, antialiased=True, cmap='rainbow')
#
# plt.show()

plt.imshow(I,cmap='gray')
plt.show()
