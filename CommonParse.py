#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author:  Zhengtang Bao

@license: (C) Copyright 2017-2018, Author Limited.

@contact: baozhengtang@gmail.com

@software: LogPlot

@file: CommonParse.py

@time: 2018/6/3 9:45

@desc: Provide Basic bit assembling and slicing action in hex string

"""


class BytesProcessOutsideException(Exception):
    """This Exception is use for bytes process outside err"""
    def __init__(self, err='Bytes Process Outside err!'):
        super(__class__, self).__init__(err)


class BytesProcessEmptySegException(Exception):
    """This Exception throws when try to get an empty segment
       from hex stream,which means width parameter is 0"""
    def __init__(self, err='Bytes get the empty segment err!'):
        super(__class__, self).__init__(err)


class BytesIncompleteException(Exception):
    """This Exception throws when input hex bytes string is not in bytes,
       which means the num of character  must be even"""
    def __init__(self, err='Bytes string incomplete err!'):
        super(__class__, self).__init__(err)


class BytesStream(object):
    """This class Define BytesStream Class which has provides basic
       methods for custom parse,also template is provide in future."""
    def __init__(self, hex_stream=str, endian=0):
        """
        Init the hex string and parse parameters
        :param hex_stream: The hex string
        :param endian: Big endian is 0,little endian is 1, default is 0
        """
        self.hexStream = hex_stream
        self.curBitsIndex = 0
        self.curBytesIndex = 0
        self.endian = endian     # default big endian is 0, little endian is 1
        # private field
        self._streamInBytes = bytes.fromhex(hex_stream)  # protected field

    def get_stream_in_bytes(self):
        """
        Get the hex string in bytes type
        :return: bytes stream
        """
        return self._streamInBytes

    def get_segment_by_index(self, idx_start=int, seg_width=int, sign=0):
        """
        Get assigned bit segment from stream
        :param idx_start:segment start index in bit,from 0 to length of stream minus 1
        :param seg_width:segment width in bit,from 1 to length of stream
        :param sign: if width include value sign, which 0=positive,1=negative,default is 0
        :return:decimal result
        """
        # check input value
        if (len(self.hexStream) % 2) != 0:
            raise BytesIncompleteException()

        sum_bit = len(self.hexStream) * 4  # because hex string element indicate 4 bits
        biggest_bit_idx = sum_bit - 1

        if (idx_start > biggest_bit_idx) or \
            ((idx_start + seg_width) > sum_bit) or \
            (seg_width > sum_bit):
            raise BytesProcessOutsideException('BytesProcessOutsideException! '
                                               'Info: idx_start=%d,seg_width=%d,sum_bit=%d,stream:%s' %
                                               (idx_start, seg_width, sum_bit, self.hexStream))
        elif seg_width == 0:
            raise BytesProcessEmptySegException('BytesProcessEmptySegException! seg_width = 0')
        else:
            byte_offset_start = int(idx_start / 8)
            bit_offset_start = int(idx_start - (byte_offset_start * 8))
            byte_offset_end = int((idx_start + seg_width - 1) / 8)
            bit_offset_end = int((idx_start + seg_width) - (byte_offset_end * 8) - 1)
            # update current bit and byte idx
            self.curBitsIndex = idx_start + seg_width  # naturally point the next bit
            self.curBytesIndex = byte_offset_end
            # compute the byte and bit offset
            stream_bytes = bytearray(self._streamInBytes)  # type transfer for modified
            seg_bytes = stream_bytes[byte_offset_start:byte_offset_end + 1]

            len_seg_bytes = len(seg_bytes)
            mask_head = 0
            mask_tail = 0
            for head_idx in range((7 - bit_offset_start) + 1):  # range fun product index
                mask_head |= (1 << head_idx)
            seg_bytes[0] = seg_bytes[0] & mask_head

            for tail_idx in range(bit_offset_end + 1):
                mask_tail |= (1 << (7 - tail_idx))
            seg_bytes[len_seg_bytes - 1] = seg_bytes[len_seg_bytes - 1] & mask_tail
            # bytes relocation
            seg_bytes_bit_offset = (7 - bit_offset_end)
            seg_bytes = bytes(seg_bytes)    # return to the original condition
            seg_hex_str = bytes.hex(seg_bytes)
            seg_offset_value = int(seg_hex_str, 16)   # input ensure hex string
            seg_value = seg_offset_value >> seg_bytes_bit_offset    # complete the segment cutoff
            # bytes endian process
            if len_seg_bytes > 1 and self.endian == 1:  # if segment bigger than 1B, process little endian
                #
                value_str_hex = hex(seg_value)
                value_str_hex = value_str_hex[2:]
                if len(value_str_hex) % 2 == 0:
                    pass
                else:
                    value_str_hex = '0' + value_str_hex
                # move bytes of the value
                value_byte_array = bytearray(bytes.fromhex(value_str_hex))
                # reverse the bytes array
                value_byte_array_new = self.__bytes_reverse(value_byte_array)
                # transfer int value
                seg_value = int(bytes.hex(bytes(value_byte_array_new)), 16)

            # value sign process
            if sign == 1:
                if seg_width in [8, 16, 32, 64]:
                    if seg_value > (2**(seg_width-1)-1):
                        seg_value = seg_value - 2**seg_width
                    else:
                        pass
                else:
                    pass
            else:
                pass

        return seg_value

    def set_segment_by_index(self, value=int, idx_start=int, val_width=int):
        """
        Set a value to the assigned bit offset with input width in bytes stream
        :param value: value to be set
        :param idx_start: bit offset in byte stream,start with 0
        :param val_width: bit width of value
        :return: the bytes type stream after set the value
        """
        base_byte_array = bytearray(self._streamInBytes)       # if init width a bytestream
        joint_mask = bytearray([0xFF])   # init the mask use for joint the value
        # check input value
        if (len(self.hexStream) % 2) != 0:
            raise BytesIncompleteException ()
        # check width
        if val_width < 1:
            raise BytesProcessOutsideException()
        elif value > 2**val_width - 1:
            raise BytesProcessOutsideException()
        else:
            # compute start byte and bit vacancy
            sum_bit = len(self.hexStream) * 4  # cus hex string element indicate 4 bits
            ret_bytes_array = bytearray.fromhex(self.hexStream)
            byte_offset_start = int(idx_start/8)
            bit_offset_start = idx_start - (byte_offset_start * 8)
            # compute end
            byte_offset_stop = int(((idx_start + val_width) - 1) / 8)

            # update current bit and byte idx
            self.curBitsIndex = idx_start + val_width
            self.curBytesIndex = byte_offset_stop

            # bit vacancy which the value need to left offset
            bit_vacancy_num = 8 - bit_offset_start
            if bit_vacancy_num == 8:
                ret_bytes_array += b'\x00'  # if just right not bit left, append one byte
            else:
                tmp_mask = (joint_mask[0] >> bit_vacancy_num)
                joint_mask[0] = tmp_mask << bit_vacancy_num
            # transfer value in bytes form
            value <<= bit_vacancy_num - val_width       # as python can offset left no limit, consider the width
            # positive or negative
            if value >= 0:
                str_value_hex = hex(value)[2:]              # slice the hex string after '0x'
            else:
                str_value_hex = hex(value)[3:]  # slice the hex string after '-0x'

            if len(str_value_hex) % 2 == 0:
                pass
            else:
                str_value_hex = '0' + str_value_hex
            value_byte_array = bytearray.fromhex(str_value_hex)
            # connect the joint part
            ret_bytes_array[byte_offset_start] &= joint_mask[0]   # mask the joint part
            ret_bytes_array[byte_offset_start] = ret_bytes_array[byte_offset_start] | value_byte_array[0]
            # judge if only in a byte
            if (bit_offset_start + val_width - 1) <= 7:
                pass
            else:
                ret_bytes_array += value_byte_array[1:1 + int((val_width - bit_vacancy_num) / 8)]

        return bytes(ret_bytes_array[:byte_offset_stop+1])  # must include byte_offset_stop

    def get_content_by_template(self):
        pass

    def __bytes_reverse(self, bytes_input=bytearray):
        """
        Get the bytes and reverse it and return
        :param bytes_input: the bytes input
        :return: the reversed bytes
        """
        len_in = len(bytes_input)
        ret_bytes = bytearray(len_in)
        for idx, item in enumerate(bytes_input):
            ret_bytes[idx] = bytes_input[len_in-idx-1]
        return ret_bytes