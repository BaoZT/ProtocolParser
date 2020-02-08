#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/2 21:33
# @Author  : Bao Zhengtang
# @Site    : 
# @File    : test_suite.py
# @Software: PyCharm

import unittest
from tests.test_CommonParse import TestCommonParse        # 导入要进行测试的测试文件

if __name__ == '__main__':
    suite = unittest.TestSuite()              #实例化一个Testsuite对象
    tests = [TestCommonParse('test_getSegmentByIndex'), TestCommonParse('test_setSegmentByIndex'),
             TestCommonParse('test_fastGetSegmentByIndex'), TestCommonParse('test_fastSetSegmentByIndex'),
             TestCommonParse('test_msgSetGetCase')]
                # 测试类继承了unittest.TestCse,所以可以这样生成实例
    suite.addTests(tests)                     #直接传入列表的方式添加，也可以通过addTest单个添加

    runner = unittest.TextTestRunner()        # 运行
    runner.run(suite)