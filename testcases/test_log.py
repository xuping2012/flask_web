'''
# -*- encoding=utf-8 -*-
Created on 2020年9月10日下午3:34:37
@author: Joe
@file:testcases.test_log.py
'''
import pytest

from utils.HandleLogging import logger


__author__ = "Joe"


class TestLogger(object):
    '''
    classdocs
    '''

    @logger("test")
    @pytest.mark.parametrize("data", ["admin1", "admin2"])
    def test_01(self, data):
        print("Logger装饰器:{}".format(data))


if __name__ == '__main__':

    pytest.main()
