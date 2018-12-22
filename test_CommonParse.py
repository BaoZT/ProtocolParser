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
        self.bytesStream_b_endian = BytesStream(self.hex_string, 0)

        self.hex_string = '12345678'
        self.bytesStream_l_endian = BytesStream(self.hex_string, 1)

        self.hex_string = '5a'
        self.bytesStream_l_set = BytesStream(self.hex_string, 1)



    def tearDown(self):
        pass

    def test_getSegmentByIndex(self):
        # regular test
        self.assertEqual(5, self.bytesStream_b_endian.getSegmentByIndex(4, 4))
        self.assertEqual(15, self.bytesStream_b_endian.getSegmentByIndex(12, 4))
        self.assertEqual(5, self.bytesStream_b_endian.getSegmentByIndex(8, 5))
        self.assertEqual(1517, self.bytesStream_b_endian.getSegmentByIndex(10, 11))
        # boundary test
        self.assertEqual(0, self.bytesStream_b_endian.getSegmentByIndex(0, 1))
        self.assertEqual(1, self.bytesStream_b_endian.getSegmentByIndex(0, 2))
        self.assertEqual(4534120, self.bytesStream_b_endian.getSegmentByIndex(0, 24))
        self.assertEqual(0, self.bytesStream_b_endian.getSegmentByIndex(23, 1))

        # regular test
        self.assertEqual(22068, self.bytesStream_l_endian.getSegmentByIndex(8, 16))
        self.assertEqual(53130, self.bytesStream_l_endian.getSegmentByIndex(13, 16))
        self.assertEqual(22020, self.bytesStream_l_endian.getSegmentByIndex(13, 11))


        # exception test
        #self.assertEqual(5, self.bytesStream.getSegmentByIndex(0, 0))
        #self.assertEqual(4534120, self.bytesStream.getSegmentByIndex(24, 1))

    def test_setSegmentByIndex(self):
        self.assertEqual(b'Zm',  self.bytesStream_l_set.setSegmentByIndex(109,8,8))
        self.assertEqual(b'Z\x80', self.bytesStream_l_set.setSegmentByIndex(4,8,3))
        self.assertEqual(b'_', self.bytesStream_l_set.setSegmentByIndex(7,5,3))