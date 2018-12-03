#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
This Exception is use for bytes process outside err
'''
class BytesProcessOutsideException(Exception):
    def __init__(self, err = 'Bytes Process Outside err!'):
        super(__class__, self).__init__(err)

'''
This Exception throws when try to get an empty segment
from hex stream,which means width parameter is 0
'''
class BytesProcessEmptySegException(Exception):
    def __init__(self, err = 'Bytes get the empty segment err!'):
        super(__class__, self).__init__(err)

'''
This class Define BytesStream Class which has provides basic
methods for custom parse,also template is provide in future.
'''
class BytesStream(object):


    def __init__(self, hexStream=str, endian=int):
        """
        Init the hex string and parse parameters
        :param stream: The hex string
        :param endian: Big endian is 0,little endian is 1
        """
        self.hexStream = hexStream
        self.curBitsIndex = 0
        self.curBytesIndex = 0
        self.endian = endian     # default big endian is 0, little endian is 1
        # private field
        self._streamInBytes = bytes.fromhex(hexStream)  # protected field

    def getStreamInBytes(self):
        """
        Get the hex string in bytes type
        :return: bytes stream
        """
        return self._streamInBytes

    def getSegmentByIndex(self, idx_start=int, seg_width=int):
        """
        Get assigned bit segment from stream
        :param idx_start:segment start index in bit,from 0 to length of stream minus 1
        :param seg_width:segment width in bit,from 1 to length of stream
        :return:decimal result
        """
        # check input value
        sum_bit = len(self.hexStream) * 4  # cus hex string element indicate 4 bits
        biggest_bit_idx = sum_bit - 1

        if (idx_start > biggest_bit_idx) or \
            ((idx_start + seg_width) > sum_bit) or \
            (seg_width > sum_bit):
            raise BytesProcessOutsideException()
        elif seg_width == 0:
            raise BytesProcessEmptySegException()
        else:
            byte_offset_start = int(idx_start / 8)
            bit_offset_start = int(idx_start - (byte_offset_start * 8))
            byte_offset_end = int((idx_start + seg_width - 1) / 8)
            bit_offset_end = int((idx_start + seg_width) - (byte_offset_end * 8) - 1)

        # compute the byte and bit offset
        stream_bytes = bytearray(self._streamInBytes)  # type transfer for modified
        seg_bytes = stream_bytes[byte_offset_start:byte_offset_end + 1]

        len_seg_bytes = len(seg_bytes)
        mask_head = 0
        mask_tail = 0
        for head_idx in range((7 - bit_offset_start) + 1):  # range fun product index
            mask_head = mask_head | (1 << head_idx)
        seg_bytes[0] = seg_bytes[0] & mask_head

        for tail_idx in range(bit_offset_end + 1):
            mask_tail = mask_tail | (1 << (7 - tail_idx))
        seg_bytes[len_seg_bytes - 1] = seg_bytes[len_seg_bytes - 1] & mask_tail
        # bytes endian process

        # bytes relocation
        seg_bytes_bit_offset = (7 - bit_offset_end)
        seg_bytes = bytes(seg_bytes)    # return to the original condition
        seg_hex_str = bytes.hex(seg_bytes)
        seg_offset_value = int(seg_hex_str,16)   # input ensure hex string
        seg_value = seg_offset_value >> seg_bytes_bit_offset

        return seg_value




    def getContentByTemplate(self):
        pass
