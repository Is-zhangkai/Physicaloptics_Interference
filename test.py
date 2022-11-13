# -*- coding: utf-8 -*-
# @Time    : 2022/10/10 15:55
# @Author  : zhangkai
# @File    : test.py
# @Software: PyCharm
import matplotlib
import numpy as np

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

"""
:parametersdfghbs
sdfhs
sdfhs
sdfh
"""

mylambda = 532e-6       #波长
k = 2 * np.pi / mylambda        #
A0 = 0.5
z0 = 30  # 传播距离
Lx = 5      #接收屏
Ly = 5
dd = 3e-3  # 像素大小
xx = np.arange(-Lx / 2, (Lx / 2)+dd, dd)
yy = np.arange(-Ly / 2, (Ly / 2)+dd, dd)
XX, YY = np.meshgrid(xx, yy)

RR = np.sqrt(XX ** 2 + YY ** 2 + z0 ** 2)

# E = (A0 / z0) * math.exp(1j * k * RR)
E0 = A0 * np.exp(1j * k * RR)






I = np.abs(E0 ** 2)
z = z0
E = 0
A = A0
for i in range(30):
    z = z + 0.5
    RR = np.sqrt(XX ** 2 + YY ** 2 + z ** 2)
    A = 0.9 * A
    E1 = A * np.exp(1j * k * RR)
    E = E + E1

I = np.abs(E ** 2)

# # 画出三维坐标系：
# axes = plt.axes(projection="3d")
# # 绘制曲面：
# axes.plot_surface(XX, YY, I, rstride=7, cstride=7, antialiased=True, cmap='rainbow')
plt.imshow(I)
plt.show()
