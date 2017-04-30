#!/usr/bin/env python
# encoding: utf-8

"""
@author: val
@software: PyCharm
@file: test.py
@time: 4/30/17 6:42 PM
"""


def func():
    pass


class Main(object):
    def __init__(self,x):
        self.x = x
        self.y = x**2


if __name__ == '__main__':
    a = Main(2)
    print a.x
    print a.y
    a.x = 3
    print a.x
    print a.y