from CommonParse import BytesStream
from app.BaseMethod import iner_escape_reverse, get_file_list, DataLabel
import threading
import time
import os
import matplotlib.pyplot as plt
import scipy.io
import numpy as np
# 定义记录消息头结构
msg_head_width = [8, 8, 10, 2, 1, 32, 32, 32, 32, 16, 3]
str_head_name = ['escap_head', 'nid_msg', 'l_msg', 'nid_modle', 'q_standby', 'n_cycle',
                 't_ato', 't_atoutc', 'm_pos', 'v_speed', 'm_atomode']
dic_msg = {}  # 创建消息头字典

spin_slope_list = []

# 记录板单条记录处理
def mvb_process(raw_record, fw):
    """
    对于每一条原始记录板信息进行处理
    :param raw_record: 原始记录信息
    :return: -1=错误，0=正常, 1=空转， 2=打滑， 3=空转+打滑
    """
    ret = 0   # 返回值
    spin = 0  # 空转指示
    slip = 0  # 打滑指示
    dl = DataLabel()
    streamReverseEsc = iner_escape_reverse(raw_record)  # 反转义每一条记录
    if streamReverseEsc == '':
        ret = -1
        return ret, dl
    item = BytesStream(streamReverseEsc)            # 创建解析对象
    # 解析消息头
    #print('*' * 30 + 'MSG_HEAD ' + '*' * 30)
    for idx, content in enumerate(msg_head_width):
        #print(str_head_name[idx] + ':' + str(item.get_segment_by_index(item.curBitsIndex, msg_head_width[idx])))
        dic_msg[str_head_name[idx]] = str(item.get_segment_by_index(item.curBitsIndex, msg_head_width[idx], sign=1))
    #print('*' * 30 + 'MSG_CONTENT ' + '*' * 30)

    dl.t_atoutc = dic_msg['t_atoutc']
    dl.t_ato = dic_msg['t_ato']
    dl.m_atomode = dic_msg['m_atomode']
    dl.v_speed = dic_msg['v_speed']
    # ATO控制信息
    tb_info = 0
    tb_cmd = ''
    t_num=0
    b_num=0
    # 解析内容
    while item.curBitsIndex < len(item.get_stream_in_bytes())*8-1:
        nid = item.get_segment_by_index(item.curBitsIndex, 8)
        #print('nid:' + str(nid))
        l_pkt = item.get_segment_by_index(item.curBitsIndex, 13)
        #print('l_pkt:' + str(l_pkt))
        if nid == 1:
            item.get_segment_by_index(item.curBitsIndex, 8)  # 心跳
            item.get_segment_by_index(item.curBitsIndex, 8)  # 有效
            tb_info = item.get_segment_by_index(item.curBitsIndex, 8)  # 牵引制动
            if tb_info == 170:
                tb_cmd='牵引'
            elif tb_info == 165:
                tb_cmd='惰行'
            elif tb_info == 85:
                tb_cmd='制动'
            else:
                tb_cmd='无命令'
            t_num = item.get_segment_by_index(item.curBitsIndex, 16)  # 牵引控制量
            b_num = item.get_segment_by_index(item.curBitsIndex, 16)  # 牵引控制量
            item.get_segment_by_index(item.curBitsIndex, 9 * 8)
        elif nid == 0:
            #print('hear_beat:' + str(item.get_segment_by_index(item.curBitsIndex, 8)))
            item.get_segment_by_index(item.curBitsIndex, 8)
            item.get_segment_by_index(item.curBitsIndex, 8)   # MOMC/AOMC
            item.get_segment_by_index(item.curBitsIndex, 8)   # ATO有效反馈
            item.get_segment_by_index(item.curBitsIndex, 8)   # 牵引制动反馈
            item.get_segment_by_index(item.curBitsIndex, 16)  # 牵引控制量反馈
            item.get_segment_by_index(item.curBitsIndex, 16)  # 制动控制量反馈
            item.get_segment_by_index(item.curBitsIndex, 8)   # 保持制动反馈
            item.get_segment_by_index(item.curBitsIndex, 8)   # 开左门开右门
            item.get_segment_by_index(item.curBitsIndex, 8)   # 恒速反馈
            item.get_segment_by_index(item.curBitsIndex, 8)   # 车门状态
            if item.get_segment_by_index(item.curBitsIndex, 4) != 0:
                spin = 1
                dl.spin_event = 1
                ltime = time.localtime(int(dic_msg['t_atoutc']))
                timeStr = time.strftime(",%H:%M:%S", ltime)
                fw.write(dic_msg['m_atomode']+',')
                fw.write(tb_cmd+','+str(t_num)+','+str(b_num))
                fw.write(timeStr + ',' + dic_msg['v_speed'] + ',空转！\n')
                # fw.write('记录板记录: '+ raw_record + '\n')
            if item.get_segment_by_index(item.curBitsIndex, 4) != 0:
                slip = 1
                dl.slope_event = 1
                ltime = time.localtime(int(dic_msg['t_atoutc']))
                timeStr = time.strftime(",%H:%M:%S", ltime)
                fw.write(dic_msg['m_atomode'] + ',')
                fw.write(tb_cmd+','+str(t_num)+','+str(b_num))
                fw.write(timeStr + ',' + dic_msg['v_speed'] + ',打滑！\n')
                # fw.write('记录板记录: ' + raw_record + '\n')
            item.get_segment_by_index(item.curBitsIndex, 19 * 8)

        else:
            item.get_segment_by_index(item.curBitsIndex, l_pkt - 21)
            #print('content:' + hex(item.get_segment_by_index(item.curBitsIndex, l_pkt - 21)))
        # 判断空转和打滑
        if spin == 0 and slip == 0:
            pass
        else:
            if spin == 1 and slip == 1:
                ret = 3
            elif slip == 1:   # 打滑2
                ret = 2
            elif spin == 1:   # 空转1
                ret = 1
        # 在下一次监测前，判断退出
        if item.curBitsIndex >= len(item.get_stream_in_bytes())*8-1-8-8:
            break
    # 解析完成
    return ret, dl


# 解析记录文件
def log_file_process(recordFile=str, fw=str):
    """
    输入文件解析mvb空转打滑
    :param recordFile:记录文件
    :param fw: 结果文件句柄
    :return:
    """
    ret = 0
    with open(recordFile) as f:
        # 打开，遍历记录
        print('解析中:' + recordFile)
        for item in f:
            try:
                ret = mvb_process(item.rstrip(), fw)
                if ret[0] > 0:
                    spin_slope_list.append(ret[1])
            except Exception as errInfo:
                print(errInfo)


# 指定基础路径
basePath = r"E:\99-MyPythonProjects\ProtocolParser\app\DataFiles"
recordFileList = []
# 获取所有记录文件
recordFileList = get_file_list(recordFileList, basePath, '.txt')
# 创建线程队列
thList = []

print('*'*10+'文件遍历'+'*'*10)
resultPath = basePath.replace('DataFiles', 'DataResult')
if os.path.exists(resultPath):
    pass
else:
    os.makedirs(resultPath)
resultFile = os.path.join(resultPath, 'result.txt')
# 打开写入文件
with open(resultFile,'w') as fw:
    # 遍历记录文件
    for recordFile in recordFileList:
        print(recordFile)
        # 限制条件
        t = threading.Thread(target=log_file_process, args=(recordFile, fw))
        thList.append(t)

    print('*' * 10 + '开启线程' + '*' * 10)
    tStart = time.time()
    # 开启线程
    for th in thList:
        th.start()
        th.join()
    tStop = time.time()
    print('解析耗时=' + str(tStop - tStart))
