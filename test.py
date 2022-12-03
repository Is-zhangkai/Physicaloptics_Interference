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

    #波长


# z0 = 30  # 传播距离
# XX,YY,I,xx,Ic=fun.Interference(mylambda,z0,0.9)

# plt.figure()
# plt.plot(xx,Ic)
# # # 画出三维坐标系：
# # plt.figure()
# # axes = plt.axes(projection="3d")
# # # 绘制曲面：
# # axes.plot_surface(XX, YY, I, rstride=9, cstride=9, antialiased=True, cmap='rainbow')
# I=255*(I-np.min(I))/(np.max(I)-np.min(I))      #调整范围
# I=np.uint8(I)
# plt.figure()
# plt.imshow(I,cmap='gray')
# plt.show()





def plane_wave(mylambda,A,alpha,bata,z):

    k = 2 * np.pi / mylambda  #

    alpha = alpha * np.pi / 180
    bata = bata * np.pi / 180
    Lx = 3 # 接收屏
    Ly = 3
    dd = 2e-3  # 像素大小
    xx = np.arange(-Lx / 2, (Lx / 2) + dd, dd)
    yy = np.arange(-Ly / 2, (Ly / 2) + dd, dd)
    XX, YY = np.meshgrid(xx, yy)
    cos_gama=np.sqrt(np.abs(1-np.cos(alpha)**2-np.cos(bata)**2))
    E=A*np.exp(1j*k*(np.cos(alpha)*XX+np.cos(bata)*YY+cos_gama*z))
    return E



if __name__ == '__main__':
    alpha = 90
    beta = 90
    mylambda = 532e-6
    z = 35
    # E1=plane_wave(mylambda,0.5,alpha,beta,30)
    # E2=plane_wave(mylambda,0.5,alpha,89,30)
    #
    # E=E1+E2
    #
    # I = np.abs(E ** 2)
    # I=255*(I-np.min(I))/(np.max(I)-np.min(I))      #调整范围
    # I=np.uint8(I)
    # plt.figure()
    # plt.imshow(I,cmap='gray')
    # plt.show()
    L = 3  # 接收屏
    dd = 2e-3  # 像素大小
    xx = np.arange(-L / 2, (L / 2) , dd)
    XX, YY = np.meshgrid(xx, xx)
    sigma=0.1
    z_B=np.exp(-((XX)**2+(YY)**2)/(2*sigma**2))/(2*np.pi*sigma**2)
    I = np.abs(z_B** 2)
    I=255*(I-np.min(I))/(np.max(I)-np.min(I))      #调整范围
    I=np.uint8(I)
    plt.figure()
    plt.imshow(I,cmap='gray')
    plt.show()