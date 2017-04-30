#!/usr/bin/env python
# encoding: utf-8

"""
@author: val
@software: PyCharm
@file: GUI.py
@time: 4/29/17 1:18 PM
"""


from __future__ import division
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtCore import QCoreApplication


class Example(QWidget):
    def __init__(self):
        super(QWidget,self).__init__()
        self.initUI()

    def initUI(self):
        # create a button called 'Quit'
        qbtn = QPushButton('Quit', self)
        # connect the button with the quit function
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 50)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Quit button')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
