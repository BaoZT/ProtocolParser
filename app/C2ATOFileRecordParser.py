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
def atp2ato_process(raw_record):
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
        if nid == 4:
            item.get_segment_by_index(item.curBitsIndex, 8)
            l_msg = item.get_segment_by_index(item.curBitsIndex, 8)
            # 记录bit数
            bit_idx = item.curBitsIndex
            byte_idx = item.curBytesIndex
            # 以下为lpacket描述范围
            item.get_segment_by_index(item.curBitsIndex, 8)
            all_len = item.get_segment_by_index(item.curBitsIndex, 13)
            # 监测ATO2ATP数据包
            while all_len != (item.curBitsIndex - bit_idx):
                nid = item.get_segment_by_index(item.curBitsIndex, 8)
                print('nid:%d' % nid, end=',')
                if nid == 132:
                    print('-->'+dic_msg['t_ato'], end=',')
                    print('e44:'+str(item.get_segment_by_index(item.curBitsIndex, 8)), end=',')
                    print('e44_l_p:'+str(item.get_segment_by_index(item.curBitsIndex, 13)), end=',')
                    print('wl_id:'+str(item.get_segment_by_index(item.curBitsIndex, 9)),end=',')
                    print('wl_id_len:'+str(item.get_segment_by_index(item.curBitsIndex, 13)), end=',')
                    print('track:'+str(item.get_segment_by_index(item.curBitsIndex, 24)), end=',')
                    print('time:'+str(item.get_segment_by_index(item.curBitsIndex, 24)),end=',')
                    print('track:'+str(item.get_segment_by_index(item.curBitsIndex, 24)), end=',')
                    print('time:'+str(item.get_segment_by_index(item.curBitsIndex, 24)), end=',')
                    print('task:'+str(item.get_segment_by_index(item.curBitsIndex, 2)), end=',')
                    print('skip:'+str(item.get_segment_by_index(item.curBitsIndex, 2)), end=',')
                    print('mtbplan:'+str(item.get_segment_by_index(item.curBitsIndex, 2)))
                elif nid == 129:
                    print('ato_mode:' + str(item.get_segment_by_index(item.curBitsIndex, 4)), end=',')
                    print('door_mode:' + str(item.get_segment_by_index(item.curBitsIndex, 2)), end=',')
                    print('tb_state:' + str(item.get_segment_by_index(item.curBitsIndex, 2)), end=',')
                    print('door_state:' + str(item.get_segment_by_index(item.curBitsIndex, 2)), end=',')
                    print('ato_err:' + str(item.get_segment_by_index(item.curBitsIndex, 16)), end=',')
                    print('ato_stop_err:' + str(item.get_segment_by_index(item.curBitsIndex, 16)))
                elif nid == 130:
                    print('l_cmd:' + str(item.get_segment_by_index(item.curBitsIndex, 2)), end=',')
                    print('r_cmd:' + str(item.get_segment_by_index(item.curBitsIndex, 2)))
                elif nid == 131:
                    print('tbs:' + str(item.get_segment_by_index(item.curBitsIndex, 2)), end=',')
                    print('skip:' + str(item.get_segment_by_index(item.curBitsIndex, 2)), end=',')
                    print('plan_valid:' + str(item.get_segment_by_index(item.curBitsIndex, 2)), end=',')
                    print('tb:' + str(item.get_segment_by_index(item.curBitsIndex, 2)), end=',')
                    print('ato_count_time:' + str(item.get_segment_by_index(item.curBitsIndex, 16)), end=',')
                    print('tcms_state:' + str(item.get_segment_by_index(item.curBitsIndex, 2)), end=',')
                    print('padding:' + str(item.get_segment_by_index(item.curBitsIndex, 22)))
                elif nid == 133:
                    print()
                else:
                    print('err!!!!!')
            #结果监测
            if all_len == (item.curBitsIndex - bit_idx):
                if (all_len + 16) % 8 == 0:    # 刚好除整数
                    print('seq:' + str(item.get_segment_by_index(item.curBitsIndex, 32)), end=',')
                    print('t_atp:' + str(item.get_segment_by_index(item.curBitsIndex, 32)), end=',')
                    print('crc:' + hex(item.get_segment_by_index(item.curBitsIndex, 32)), end=',')
                    if l_msg == item.curBytesIndex - byte_idx + 2:  # 2B即为消息头两个8位
                        print('msg ok')
                else:
                    # 重新校正bit索引
                    tump = int(((all_len + 16 + 7) // 8) * 8) - all_len - 16  # 字节下跳的bit数，减去消息头16bit和内容bit后
                    item.get_segment_by_index(item.curBitsIndex, tump)
                    print('seq:' + str(item.get_segment_by_index(item.curBitsIndex, 32)), end=',')
                    print('t_atp:' + str(item.get_segment_by_index(item.curBitsIndex, 32)), end=',')
                    print('crc:' + hex(item.get_segment_by_index(item.curBitsIndex, 32)), end=',')
                    if l_msg == item.curBytesIndex - byte_idx + 2:
                        print('msg ok')
                    else:
                        print('fatal err！ l_msg %d, real %d' % (l_msg, item.curBytesIndex - byte_idx + 2))
        elif nid == 3:
            print('---->atp2ato_content:' + hex(item.get_segment_by_index(item.curBitsIndex, l_pkt - 21)))
        else:
            item.get_segment_by_index(item.curBitsIndex, l_pkt - 21)
            #print('content:' + hex(item.get_segment_by_index(item.curBitsIndex, l_pkt - 21)))
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
                ret = atp2ato_process(item.rstrip())
                if ret > 0:
                    print('ATO->ATP '+ recordFile)
            except Exception as errInfo:
                print(errInfo)


# 指定基础路径
basePath = r"F:\04-ATO Debug Data\C2ATO\DataFiles"
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



