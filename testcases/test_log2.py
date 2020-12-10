'''
# -*- encoding=utf-8 -*-
Created on 2020年9月10日下午3:34:37
@author: Joe
@file:testcases.test_log.py
'''
import unittest

from ddt import data, ddt

from utils.HandleLogging import logger


__author__ = "Joe"


@ddt
class TestLogger(unittest.TestCase):
    '''
    classdocs
    '''

    @logger("test")
    @data(*{"admin1": "1", "admin2": '2', "admin3": '3', "admin4": "4"})
#     @unpack
    def test_01(self, data1):
        print("Logger装饰器:{}".format(data1))


if __name__ == '__main__':
    unittest.main()
