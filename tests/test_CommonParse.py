#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/2 21:33
# @Author  : Bao Zhengtang
# @Site    : 
# @File    : test_CommonParse.py
# @Software: PyCharm

import unittest
import sys
from CommonParse import  BytesStream


class TestCommonParse(unittest.TestCase):

    def setUp(self):
        self.hex_string = '452F68'
        self.bytesStream_b_endian = BytesStream(self.hex_string, 0)

        self.hex_string = '12345678'
        self.hex_string2 = '039A120D'
        self.bytesStream_l_endian = BytesStream(self.hex_string, 1)
        self.bytesStream_l_endian2 = BytesStream(self.hex_string2, 1)

        self.hex_string = '5a'
        self.bytesStream_l_set = BytesStream(self.hex_string, 1)

        self.hex_string = '005a'
        self.bytesStream_l_set2 = BytesStream(self.hex_string, 1)

    def tearDown(self):
        pass

    def test_getSegmentByIndex(self):
        # regular test
        self.assertEqual(5, self.bytesStream_b_endian.get_segment_by_index(4, 4))
        self.assertEqual(15, self.bytesStream_b_endian.get_segment_by_index(12, 4))
        self.assertEqual(5, self.bytesStream_b_endian.get_segment_by_index(8, 5))
        self.assertEqual(7, self.bytesStream_b_endian.get_segment_by_index(self.bytesStream_b_endian.curBitsIndex, 3))
        self.assertEqual(3, self.bytesStream_b_endian.get_segment_by_index(self.bytesStream_b_endian.curBitsIndex, 3))
        self.assertEqual(2, self.bytesStream_b_endian.get_segment_by_index(self.bytesStream_b_endian.curBitsIndex, 3))
        self.assertEqual(0, self.bytesStream_b_endian.get_segment_by_index(self.bytesStream_b_endian.curBitsIndex, 2))

        # boundary test
        self.assertEqual(0, self.bytesStream_b_endian.get_segment_by_index(0, 1))
        self.assertEqual(1, self.bytesStream_b_endian.get_segment_by_index(0, 2))
        self.assertEqual(4534120, self.bytesStream_b_endian.get_segment_by_index(0, 24))
        self.assertEqual(0, self.bytesStream_b_endian.get_segment_by_index(23, 1))

        # regular test
        self.assertEqual(22068, self.bytesStream_l_endian.get_segment_by_index(8, 16))
        self.assertEqual(86, self.bytesStream_l_endian.get_segment_by_index(16, 8))
        self.assertEqual(30806, self.bytesStream_l_endian.get_segment_by_index(16, 16))
        self.assertEqual(7886388, self.bytesStream_l_endian.get_segment_by_index(8, 24))
        # exception test
        # self.assertEqual(5, self.bytesStream.getSegmentByIndex(0, 0))
        # self.assertEqual(4534120, self.bytesStream.getSegmentByIndex(24, 1))

    def test_fastGetSegmentByIndex(self):
        # regular test
        self.assertEqual(22068, self.bytesStream_l_endian.fast_get_segment_by_index(8, 16))
        self.assertEqual(86, self.bytesStream_l_endian.fast_get_segment_by_index(16, 8))
        self.assertEqual(30806, self.bytesStream_l_endian.fast_get_segment_by_index(16, 16))
        self.assertEqual(7886388, self.bytesStream_l_endian.fast_get_segment_by_index(8, 24))
        self.assertEqual(3346, self.bytesStream_l_endian2.fast_get_segment_by_index(16, 16))

    def test_setSegmentByIndex(self):
        self.assertEqual('5a6d', self.bytesStream_l_set.set_segment_by_index(109, 8, 8))
        self.assertEqual('5a80', self.bytesStream_l_set.set_segment_by_index(4, 8, 3))
        self.assertEqual('5f', self.bytesStream_l_set.set_segment_by_index(7, 5, 3))
        self.assertEqual('56', self.bytesStream_l_set.set_segment_by_index(3, 4, 3))
        self.assertEqual('565a', self.bytesStream_l_set.set_segment_by_index(90, 8, 8))
        self.assertEqual('7e', self.bytesStream_l_set.set_segment_by_index(126, 0, 8))
        self.assertEqual('7ec9', self.bytesStream_l_set.set_segment_by_index(201, self.bytesStream_l_set.curBitsIndex, 8))

        hex_string = '005a'
        bytesStream_l_set2 = BytesStream(hex_string)
        self.assertEqual('005a0000fe', bytesStream_l_set2.set_segment_by_index(254, 32, 8))

    def test_fastSetSegmentByIndex(self):
        self.assertEqual('5a6d', self.bytesStream_l_set.fast_set_segment_by_index(109, 8, 8))
        self.assertEqual('5a80', self.bytesStream_l_set.fast_set_segment_by_index(4, 8, 3))
        self.assertEqual('5f', self.bytesStream_l_set.fast_set_segment_by_index(7, 5, 3))
        self.assertEqual('56', self.bytesStream_l_set.fast_set_segment_by_index(3, 4, 3))
        self.assertEqual('565a', self.bytesStream_l_set.fast_set_segment_by_index(90, 8, 8))
        self.assertEqual('7e', self.bytesStream_l_set.fast_set_segment_by_index(126, 0, 8))
        
        self.assertEqual('005a0000fe', self.bytesStream_l_set2.fast_set_segment_by_index(254, 32, 8))

    def test_msgSetGetCase(self):
        raw_hex = '2D49FA0EA01805276EF820C8180D40CAF012D40457000C79C2B03D425E4521A3459D89C30AC20003FFFFFFFC00637DFC006C' \
                  'C68C00266B190006B7FBA0'
        stream_fast_get_b = BytesStream(raw_hex, endian=0)
        self.assertEqual(45, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 8))
        self.assertEqual(73, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 8))
        self.assertEqual(250, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 8))
        self.assertEqual(468, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 13))
        # sp3
        self.assertEqual(3, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 8))
        self.assertEqual(10808799, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 32))
        # sp4
        self.assertEqual(4, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 8))
        self.assertEqual(6403, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 16))
        self.assertEqual(27793758, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 32))
        # sp2
        self.assertEqual(2, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 8))
        self.assertEqual(1, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 2))
        self.assertEqual(1, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 2))
        self.assertEqual(2, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 2))
        self.assertEqual(2, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 2))
        self.assertEqual(2, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 2))
        self.assertEqual(0, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 2))
        self.assertEqual(2222, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 16))
        self.assertEqual(1635205, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 32))
        self.assertEqual(3, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 3))
        self.assertEqual(0, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 4))
        self.assertEqual(1027759685, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 32))
        self.assertEqual(8611, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 16))
        self.assertEqual(17821, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 16))
        self.assertEqual(2, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 2))
        self.assertEqual(9996, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 16))
        self.assertEqual(43, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 8))
        self.assertEqual(0, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 4))
        self.assertEqual(32768, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 16))
        self.assertEqual(4294967295, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 32))
        self.assertEqual(1630079, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 32))
        self.assertEqual(1782179, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 32))
        self.assertEqual(629446, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 32))
        self.assertEqual(1, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 2))
        self.assertEqual(440315, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 32))
        self.assertEqual(2, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 2))
        self.assertEqual(2, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 2))

        stream_fast_set_b = BytesStream('', endian=0)
        stream_fast_set_b.fast_set_segment_by_index(45, stream_fast_set_b.curBitsIndex, 8)
        stream_fast_set_b.fast_set_segment_by_index(73, stream_fast_set_b.curBitsIndex, 8)
        stream_fast_set_b.fast_set_segment_by_index(250, stream_fast_set_b.curBitsIndex, 8)
        stream_fast_set_b.fast_set_segment_by_index(468, stream_fast_set_b.curBitsIndex, 13)
        # sp3
        stream_fast_set_b.fast_set_segment_by_index(3, stream_fast_set_b.curBitsIndex, 8)
        stream_fast_set_b.fast_set_segment_by_index(10808799, stream_fast_set_b.curBitsIndex, 32)
        # sp4
        stream_fast_set_b.fast_set_segment_by_index(4, stream_fast_set_b.curBitsIndex, 8)
        stream_fast_set_b.fast_set_segment_by_index(6403, stream_fast_set_b.curBitsIndex, 16)
        stream_fast_set_b.fast_set_segment_by_index(27793758, stream_fast_set_b.curBitsIndex, 32)
        stream_fast_set_b.fast_set_segment_by_index(2, stream_fast_set_b.curBitsIndex, 8)
        stream_fast_set_b.fast_set_segment_by_index(1, stream_fast_set_b.curBitsIndex, 2)
        stream_fast_set_b.fast_set_segment_by_index(1, stream_fast_set_b.curBitsIndex, 2)
        stream_fast_set_b.fast_set_segment_by_index(2, stream_fast_set_b.curBitsIndex, 2)
        stream_fast_set_b.fast_set_segment_by_index(2, stream_fast_set_b.curBitsIndex, 2)
        stream_fast_set_b.fast_set_segment_by_index(2, stream_fast_set_b.curBitsIndex, 2)
        stream_fast_set_b.fast_set_segment_by_index(0, stream_fast_set_b.curBitsIndex, 2)
        stream_fast_set_b.fast_set_segment_by_index(2222, stream_fast_set_b.curBitsIndex, 16)
        stream_fast_set_b.fast_set_segment_by_index(1635205, stream_fast_set_b.curBitsIndex, 32)
        stream_fast_set_b.fast_set_segment_by_index(3, stream_fast_set_b.curBitsIndex, 3)
        stream_fast_set_b.fast_set_segment_by_index(0, stream_fast_set_b.curBitsIndex, 4)
        stream_fast_set_b.fast_set_segment_by_index(1027759685, stream_fast_set_b.curBitsIndex, 32)
        stream_fast_set_b.fast_set_segment_by_index(8611, stream_fast_set_b.curBitsIndex, 16)
        stream_fast_set_b.fast_set_segment_by_index(17821, stream_fast_set_b.curBitsIndex, 16)
        stream_fast_set_b.fast_set_segment_by_index(2, stream_fast_set_b.curBitsIndex, 2)
        stream_fast_set_b.fast_set_segment_by_index(9996, stream_fast_set_b.curBitsIndex, 16)
        stream_fast_set_b.fast_set_segment_by_index(43, stream_fast_set_b.curBitsIndex, 8)
        stream_fast_set_b.fast_set_segment_by_index(0, stream_fast_set_b.curBitsIndex, 4)
        stream_fast_set_b.fast_set_segment_by_index(32768, stream_fast_set_b.curBitsIndex, 16)
        stream_fast_set_b.fast_set_segment_by_index(4294967295, stream_fast_set_b.curBitsIndex, 32)
        stream_fast_set_b.fast_set_segment_by_index(1630079, stream_fast_set_b.curBitsIndex, 32)
        stream_fast_set_b.fast_set_segment_by_index(1782179, stream_fast_set_b.curBitsIndex, 32)
        stream_fast_set_b.fast_set_segment_by_index(629446, stream_fast_set_b.curBitsIndex, 32)
        stream_fast_set_b.fast_set_segment_by_index(1, stream_fast_set_b.curBitsIndex, 2)
        stream_fast_set_b.fast_set_segment_by_index(440315, stream_fast_set_b.curBitsIndex, 32)
        stream_fast_set_b.fast_set_segment_by_index(2, stream_fast_set_b.curBitsIndex, 2)
        stream_fast_set_b.fast_set_segment_by_index(2, stream_fast_set_b.curBitsIndex, 2)
        self.assertEqual(stream_fast_set_b.hexStream.upper(), raw_hex) 
        
        stream_get_b = BytesStream(raw_hex, endian=0)
        self.assertEqual(45, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 8))
        self.assertEqual(73, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 8))
        self.assertEqual(250, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 8))
        self.assertEqual(468, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 13))
        # sp3
        self.assertEqual(3, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 8))
        self.assertEqual(10808799, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 32))
        # sp4
        self.assertEqual(4, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 8))
        self.assertEqual(6403, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 16))
        self.assertEqual(27793758, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 32))
        # sp2
        self.assertEqual(2, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 8))
        self.assertEqual(1, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 2))
        self.assertEqual(1, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 2))
        self.assertEqual(2, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 2))
        self.assertEqual(2, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 2))
        self.assertEqual(2, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 2))
        self.assertEqual(0, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 2))
        self.assertEqual(2222, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 16))
        self.assertEqual(1635205, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 32))
        self.assertEqual(3, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 3))
        self.assertEqual(0, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 4))
        self.assertEqual(1027759685, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 32))
        self.assertEqual(8611, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 16))
        self.assertEqual(17821, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 16))
        self.assertEqual(2, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 2))
        self.assertEqual(9996, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 16))
        self.assertEqual(43, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 8))
        self.assertEqual(0, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 4))
        self.assertEqual(32768, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 16))
        self.assertEqual(4294967295, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 32))
        self.assertEqual(1630079, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 32))
        self.assertEqual(1782179, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 32))
        self.assertEqual(629446, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 32))
        self.assertEqual(1, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 2))
        self.assertEqual(440315, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 32))
        self.assertEqual(2, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 2))
        self.assertEqual(2, stream_get_b.get_segment_by_index(stream_get_b.curBitsIndex, 2))

        stream_set_b = BytesStream('', endian=0)
        stream_set_b.set_segment_by_index(45, stream_set_b.curBitsIndex, 8)
        stream_set_b.set_segment_by_index(73, stream_set_b.curBitsIndex, 8)
        stream_set_b.set_segment_by_index(250, stream_set_b.curBitsIndex, 8)
        stream_set_b.set_segment_by_index(468, stream_set_b.curBitsIndex, 13)
        # sp3
        stream_set_b.set_segment_by_index(3, stream_set_b.curBitsIndex, 8)
        stream_set_b.set_segment_by_index(10808799, stream_set_b.curBitsIndex, 32)
        # sp4
        stream_set_b.set_segment_by_index(4, stream_set_b.curBitsIndex, 8)
        stream_set_b.set_segment_by_index(6403, stream_set_b.curBitsIndex, 16)
        stream_set_b.set_segment_by_index(27793758, stream_set_b.curBitsIndex, 32)
        stream_set_b.set_segment_by_index(2, stream_set_b.curBitsIndex, 8)
        stream_set_b.set_segment_by_index(1, stream_set_b.curBitsIndex, 2)
        stream_set_b.set_segment_by_index(1, stream_set_b.curBitsIndex, 2)
        stream_set_b.set_segment_by_index(2, stream_set_b.curBitsIndex, 2)
        stream_set_b.set_segment_by_index(2, stream_set_b.curBitsIndex, 2)
        stream_set_b.set_segment_by_index(2, stream_set_b.curBitsIndex, 2)
        stream_set_b.set_segment_by_index(0, stream_set_b.curBitsIndex, 2)
        stream_set_b.set_segment_by_index(2222, stream_set_b.curBitsIndex, 16)
        stream_set_b.set_segment_by_index(1635205, stream_set_b.curBitsIndex, 32)
        stream_set_b.set_segment_by_index(3, stream_set_b.curBitsIndex, 3)
        stream_set_b.set_segment_by_index(0, stream_set_b.curBitsIndex, 4)
        stream_set_b.set_segment_by_index(1027759685, stream_set_b.curBitsIndex, 32)
        stream_set_b.set_segment_by_index(8611, stream_set_b.curBitsIndex, 16)
        stream_set_b.set_segment_by_index(17821, stream_set_b.curBitsIndex, 16)
        stream_set_b.set_segment_by_index(2, stream_set_b.curBitsIndex, 2)
        stream_set_b.set_segment_by_index(9996, stream_set_b.curBitsIndex, 16)
        stream_set_b.set_segment_by_index(43, stream_set_b.curBitsIndex, 8)
        stream_set_b.set_segment_by_index(0, stream_set_b.curBitsIndex, 4)
        stream_set_b.set_segment_by_index(32768, stream_set_b.curBitsIndex, 16)
        stream_set_b.set_segment_by_index(4294967295, stream_set_b.curBitsIndex, 32)
        stream_set_b.set_segment_by_index(1630079, stream_set_b.curBitsIndex, 32)
        stream_set_b.set_segment_by_index(1782179, stream_set_b.curBitsIndex, 32)
        stream_set_b.set_segment_by_index(629446, stream_set_b.curBitsIndex, 32)
        stream_set_b.set_segment_by_index(1, stream_set_b.curBitsIndex, 2)
        stream_set_b.set_segment_by_index(440315, stream_set_b.curBitsIndex, 32)
        stream_set_b.set_segment_by_index(2, stream_set_b.curBitsIndex, 2)
        stream_set_b.set_segment_by_index(2, stream_set_b.curBitsIndex, 2)
        self.assertEqual(stream_set_b.hexStream.upper(), raw_hex)  #   test

        raw_hex2 = '2D18FB026C1E2FFFEB8FFFF8'
        stream_fast_get_b = BytesStream(raw_hex2, endian=0)
        # sp131
        self.assertEqual(45, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 8))
        self.assertEqual(24, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 8))
        self.assertEqual(251, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 8))
        self.assertEqual(77, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 13))
        self.assertEqual(131, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 8))
        self.assertEqual(3, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 2))
        self.assertEqual(0, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 2))
        self.assertEqual(1, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 2))
        self.assertEqual(32767, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 16))
        self.assertEqual(1, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 2))
        self.assertEqual(1, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 2))
        self.assertEqual(3, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 2))
        self.assertEqual(1, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 4))
        self.assertEqual(65535, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 16))

        stream_set_b = BytesStream('', endian=0)
        stream_set_b.set_segment_by_index(45, stream_set_b.curBitsIndex, 8)
        stream_set_b.set_segment_by_index(24, stream_set_b.curBitsIndex, 8)
        stream_set_b.set_segment_by_index(251, stream_set_b.curBitsIndex, 8)
        stream_set_b.set_segment_by_index(77, stream_set_b.curBitsIndex, 13)
        stream_set_b.set_segment_by_index(131, stream_set_b.curBitsIndex, 8)
        stream_set_b.set_segment_by_index(3, stream_set_b.curBitsIndex, 2)
        stream_set_b.set_segment_by_index(0, stream_set_b.curBitsIndex, 2)
        stream_set_b.set_segment_by_index(1, stream_set_b.curBitsIndex, 2)
        stream_set_b.set_segment_by_index(32767, stream_set_b.curBitsIndex, 16)
        stream_set_b.set_segment_by_index(1, stream_set_b.curBitsIndex, 2)
        stream_set_b.set_segment_by_index(1, stream_set_b.curBitsIndex, 2)
        stream_set_b.set_segment_by_index(3, stream_set_b.curBitsIndex, 2)
        stream_set_b.set_segment_by_index(1, stream_set_b.curBitsIndex, 4)
        stream_set_b.set_segment_by_index(65535, stream_set_b.curBitsIndex, 16)
        self.assertEqual(stream_set_b.hexStream.upper(), raw_hex2)  # test

        raw_hex3 = '7EC92718003B00781726AADAEE5D9799E0DA1B1F05F1090228F9D85069D21808255D80000000000000000000000000000000812AED55FFFFFFFFFFFC0562168000000000320B4204A8DC28FFFFFFFFFFFFFC00000000000000014060FD2D1DFA03A81817209FD02705F004113C98000765F102E413FA9B42FC660008AB81800000000000000000055000089C45555180000000000000000000000000007F'
        stream_fast_get_b = BytesStream(raw_hex3, endian=0)

        self.assertEqual(126, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 8))
        self.assertEqual(201, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 8))
        self.assertEqual(156, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 10))
        self.assertEqual(1, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 2))
        self.assertEqual(1, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 1))
        self.assertEqual(483343, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 32))
        self.assertEqual(48551259, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 32))
        self.assertEqual(1573630707, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 32))
        self.assertEqual(1008419683, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 32))
        self.assertEqual(-8002, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 16, sign=1))
        self.assertEqual(1, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 3))
        # p9
        self.assertEqual(9, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 8))
        self.assertEqual(69, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 13))
        self.assertEqual(7995, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 16))
        self.assertEqual(168639043, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 32))
        # p1
        self.assertEqual(1, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 8))
        self.assertEqual(149, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 13))
        self.assertEqual(int(0x76000000000000000000000000000000), stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 149-21))
        # p2
        self.assertEqual(2, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 8))
        self.assertEqual(149, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 13))
        self.assertEqual(int(0x76aafffffffffffe02b10b4000000000), stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 149-21))
        # p25
        # self.assertEqual(25, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 8))
        # self.assertEqual(180, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 13))
        # self.assertEqual(0, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 1))
        # self.assertEqual(0, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 1))
        # self.assertEqual(1, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 1))
        # self.assertEqual(39087636, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 32))
        # self.assertEqual(1, stream_fast_get_b.fast_get_segment_by_index(stream_fast_get_b.curBitsIndex, 2))

        self.assertEqual(25, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 8))
        self.assertEqual(180, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 13))
        self.assertEqual(0, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 1))
        self.assertEqual(0, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 1))
        self.assertEqual(1, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 1))
        self.assertEqual(39087636, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 32))
        self.assertEqual(1, stream_fast_get_b.get_segment_by_index(stream_fast_get_b.curBitsIndex, 2))
        
    def test_msgZeroHeadSetCase(self):
        item = BytesStream('')
        item.set_segment_by_index(100823,item.curBitsIndex,24)
        if False:
            item.set_segment_by_index(13,item.curBitsIndex,9)                     # 按照CTCS3+ATO中C13包

        else:
            item.set_segment_by_index(0,item.curBitsIndex,9)
        item.set_segment_by_index(0,item.curBitsIndex,2)
        item.set_segment_by_index(0,item.curBitsIndex,2)
        item.set_segment_by_index(0,item.curBitsIndex,24)
        item.set_segment_by_index(0,item.curBitsIndex,15)
        item.set_segment_by_index(1,item.curBitsIndex,4)
        self.assertEqual("0189d700000000000001", item.hexStream)

        item = BytesStream('')
        item.fast_set_segment_by_index(100823,item.curBitsIndex,24)
        if False:
            item.fast_set_segment_by_index(13,item.curBitsIndex,9)                     # 按照CTCS3+ATO中C13包

        else:
            item.fast_set_segment_by_index(0,item.curBitsIndex,9)
        item.fast_set_segment_by_index(0,item.curBitsIndex,2)
        item.fast_set_segment_by_index(0,item.curBitsIndex,2)
        item.fast_set_segment_by_index(0,item.curBitsIndex,24)
        item.fast_set_segment_by_index(0,item.curBitsIndex,15)
        item.fast_set_segment_by_index(1,item.curBitsIndex,4)
        #self.assertEqual("0189d700000000000001", item.hexStream)

    
    