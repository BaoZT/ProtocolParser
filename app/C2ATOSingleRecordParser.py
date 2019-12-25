from CommonParse import BytesStream
streamReverseEsc = ('2d1efa03e0496405f0fc048bd4800bd46000000000480002945c8a6180bf')

item = BytesStream(streamReverseEsc)
content = ['m_waysidetime', 'nid_depart_track', 'm_depart_time', 'nid_arrival_track', 'm_arrival_time', 'm_task',
           'm_skip', 'm_tbplan']
width = [24, 24, 24, 24, 24, 2, 2, 2]

content_it = ['nid_depart_track', 'm_depart_time', 'nid_arrival_track', 'm_arrival_time', 'm_task',
           'm_skip', 'm_tbplan']
width_it = [24, 24, 24, 24, 2, 2, 2]

# 解析内容
while item.curBitsIndex < len(item.get_stream_in_bytes()) * 8 - 1:
    nid_stm = item.get_segment_by_index(item.curBitsIndex, 8)
    l_msg = item.get_segment_by_index(item.curBitsIndex, 8)
    nid_packet = item.get_segment_by_index(item.curBitsIndex, 8)
    l_packet = item.get_segment_by_index(item.curBitsIndex, 13)

    nid_sub_packet = item.get_segment_by_index(item.curBitsIndex, 8)
    print('nid:' + str(nid_sub_packet))
    # E44 用户消息
    packet = item.get_segment_by_index(item.curBitsIndex, 8)
    print('nid:' + str(packet))
    dir = item.get_segment_by_index(item.curBitsIndex, 2)
    print('dir:' + str(dir))
    l_pkt = item.get_segment_by_index(item.curBitsIndex, 13)
    print('l_packet:' + str(l_pkt))
    # 计划包
    wl_packet = item.get_segment_by_index(item.curBitsIndex, 9)
    print('wl_packet:' + str(wl_packet))
    it = item.get_segment_by_index(item.curBitsIndex, 2)
    print('dir:' + str(it))
    it = item.get_segment_by_index(item.curBitsIndex, 13)
    print('ctcs21-lp:' + str(it))
    for idx, name in enumerate(content):
        it = item.get_segment_by_index(item.curBitsIndex, width[idx])
        if 'time' in content[idx]:
            print('-------> BCD:' + hex(it))
        print(content[idx] + ':' + str(it))

    it = item.get_segment_by_index(item.curBitsIndex, 5)
    print('niter:' + str(it))
    for i in range(it):
        for idx, name in enumerate(content_it):
            it = item.get_segment_by_index(item.curBitsIndex, width_it[idx])
            if 'time' in content_it[idx]:
                print('-------> BCD:' + hex(it))
            print(content_it[idx] + ':' + str(it))

    break


    # 在下一次监测前，判断退出
    if item.curBitsIndex >= len(item.get_stream_in_bytes()) * 8 - 1 - 8:   #代表一个字节内
        break
