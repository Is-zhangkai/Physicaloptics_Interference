# -*- coding: utf-8 -*-
# @Time    : 2022/10/10 15:55
# @Author  : zhangkai
# @File    : test.py
# @Software: PyCharm

import matplotlib
import numpy as np
import Function as fun
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

mylambda = 532e-6       #波长



z0 = 30  # 传播距离
XX,YY,I,xx,Ic=fun.Interference(mylambda,z0,0.9)



plt.figure()
plt.plot(xx,Ic)




# # 画出三维坐标系：
# plt.figure()
# axes = plt.axes(projection="3d")
# # 绘制曲面：
# axes.plot_surface(XX, YY, I, rstride=9, cstride=9, antialiased=True, cmap='rainbow')
#
I=255*(I-np.min(I))/(np.max(I)-np.min(I))      #调整范围


I=np.uint8(I)
plt.figure()
plt.imshow(I,cmap='gray')
plt.show()
