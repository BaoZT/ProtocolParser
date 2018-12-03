#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/2 21:33
# @Author  : Bao Zhengtang
# @Site    : 
# @File    : test_CommonParse.py
# @Software: PyCharm

import unittest
from CommonParse import *

class TestCommonParse(unittest.TestCase):

    def setUp(self):
        self.hex_string = '452F68'
        self.bytesStream = BytesStream(self.hex_string, 0)

    def test_getSegmentByIndex(self):
        self.assertEqual(5, self.bytesStream.getSegmentByIndex(4, 4))
        self.assertEqual(15, self.bytesStream.getSegmentByIndex(12, 4))
        self.assertEqual(5, self.bytesStream.getSegmentByIndex(8, 5))
        # 需要整体搬移的有缺陷