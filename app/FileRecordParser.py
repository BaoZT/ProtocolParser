from CommonParse import BytesStream
from app.BaseMethod import iner_escape_reverse, get_file_list
import threading
import time
# 定义记录消息头结构
msg_head_width = [8, 8, 10, 2, 1, 32, 32, 32, 32, 16, 3]
str_head_name = ['escap_head', 'nid_msg', 'l_msg', 'nid_modle', 'q_standby', 'n_cycle',
                 't_ato', 't_atoutc', 'm_pos', 'v_speed', 'm_atomode']
dic_msg = {}  # 创建消息头字典


# 记录板单条记录处理
def mvb_process(raw_record):
    """
    对于每一条原始记录板信息进行处理
    :param raw_record: 原始记录信息
    :return: -1=错误，0=正常, 1=空转， 2=打滑， 3=空转+打滑
    """
    ret = 0   # 返回值
    spin = 0  # 空转指示
    slip = 0  # 打滑指示
    streamReverseEsc = iner_escape_reverse(raw_record)  # 反转义每一条记录
    if streamReverseEsc == '':
        return -1
    item = BytesStream(streamReverseEsc)            # 创建解析对象
    # 解析消息头
    #print('*' * 30 + 'MSG_HEAD ' + '*' * 30)
    for idx, content in enumerate(msg_head_width):
        #print(str_head_name[idx] + ':' + str(item.get_segment_by_index(item.curBitsIndex, msg_head_width[idx])))
        dic_msg[str_head_name[idx]] = str(item.get_segment_by_index(item.curBitsIndex, msg_head_width[idx], sign=1))
    #print('*' * 30 + 'MSG_CONTENT ' + '*' * 30)
    # 解析内容
    while item.curBitsIndex < len(item.get_stream_in_bytes())*8-1:
        nid = item.get_segment_by_index(item.curBitsIndex, 8)
        #print('nid:' + str(nid))
        l_pkt = item.get_segment_by_index(item.curBitsIndex, 13)
        #print('l_pkt:' + str(l_pkt))
        if nid == 0:
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
                ltime = time.localtime(int(dic_msg['t_atoutc']))
                timeStr = time.strftime("%H:%M:%S", ltime)
                print(timeStr + ', v:' + dic_msg['v_speed'] + '空转！')
                print('记录板记录: '+ raw_record)
            if item.get_segment_by_index(item.curBitsIndex, 4) != 0:
                slip = 1
                ltime = time.localtime(int(dic_msg['t_atoutc']))
                timeStr = time.strftime("%H:%M:%S", ltime)
                print(timeStr + ', v:' + dic_msg['v_speed'] + '打滑！')
                print('记录板记录: ' + raw_record)
            item.get_segment_by_index(item.curBitsIndex, 19 * 8)
        else:
            item.get_segment_by_index(item.curBitsIndex, l_pkt - 21)
            #print('content:' + hex(item.get_segment_by_index(item.curBitsIndex, l_pkt - 21)))
        # 判断空转和打滑
        if spin == 1 and slip == 1:
            ret = 3
        elif slip == 1:   # 打滑2
            ret = 2
        elif spin == 1:   # 空转1
            ret = 1
        else:
            ret = 0       # 其他认为正常
        # 在下一次监测前，判断退出
        if item.curBitsIndex >= len(item.get_stream_in_bytes())*8-1-8-8:
            break
    # 解析完成
    return ret


# 解析记录文件
def log_file_process(recordFile=str):
    """
    输入文件解析mvb空转打滑
    :param recordFile:
    :return:
    """
    ret = 0
    with open(recordFile) as f:
        # 打开，遍历记录
        print('解析中:' + recordFile)
        for item in f:
            try:
                ret = mvb_process(item.rstrip())
                if ret > 0:
                    print('空转打滑记录 '+ recordFile)
            except Exception as errInfo:
                print(errInfo)


# 指定基础路径
basePath = r"E:\99 My Python Projects\ProtocolParser\app\DataFiles\DataFiles"
recordFileList = []
# 获取所有记录文件
recordFileList = get_file_list(recordFileList, basePath, '.txt')
# 创建线程队列
thList = []

print('*'*10+'文件遍历'+'*'*10)
# 遍历记录文件
for recordFile in recordFileList:
    print(recordFile)
    # 限制条件
    t = threading.Thread(target=log_file_process, args=(recordFile,))
    thList.append(t)

print('*'*10+'开启线程'+'*'*10)
tStart = time.time()
# 开启线程
for th in thList:
    th.start()
tStop = time.time()

print('解析耗时='+str(tStop-tStart))



