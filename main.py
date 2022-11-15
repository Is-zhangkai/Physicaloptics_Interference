# -*- coding: utf-8 -*-
# @Time    : 2022/11/13
# @Author  : zhangkai
# @File    : main.py
# @Software: PyCharm
"""
主函数，打开主界面
"""

import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from qt_material import apply_stylesheet
from Package import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mywindow = MainWindow()

    mywindow.setWindowTitle("Physicaloptics_Fresnel")
    mywindow.setWindowIcon(QIcon("./icon.ico"))
    # 使用主题
    # apply_stylesheet(app, theme='dark_zk.xml')

    mywindow.show()
    sys.exit(app.exec_())