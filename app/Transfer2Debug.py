from CommonParse import BytesStream
from app.BaseMethod import iner_escape_reverse, get_file_list, copy_file_dir
import threading
import os
import time
TIME_ZONE = ''
# 定义记录消息头结构
msg_head_width = [8, 8, 10, 2, 1, 32, 32, 32, 32, 16, 3]
str_head_name = ['escap_head', 'nid_msg', 'l_msg', 'nid_modle', 'q_standby', 'n_cycle',
                 't_ato', 't_atoutc', 'm_pos', 'v_speed', 'm_atomode']

dic_msg = {}
dic_mvb = {}
dic_sdu = {}
dic_atp2ato_pkt = {}
dic_ato2atp_pkt = {}
dic_rp = {}
# 记录板单条记录处理
def ctrl_process_transfer(raw_record):
    """
    对于每一条原始记录板信息进行处理
    :param raw_record: 原始记录信息
    :return: 函数执行返回值和数据解析结果 ret_sig:0=政常,-1=错误消息,-2=存在启机过程
    """
    global dic_msg
    global dic_mvb
    global dic_sdu
    global dic_atp2ato_pkt
    global dic_ato2atp_pkt
    # 清空数据包字典
    dic_atp2ato_pkt = {}
    dic_ato2atp_pkt = {}

    ret_sig = 0        # 返回值指示
    streamReverseEsc = iner_escape_reverse(raw_record)  # 反转义每一条记录
    if streamReverseEsc == '':
        ret_sig = -1
        return ret_sig
    item = BytesStream(streamReverseEsc)            # 创建解析对象
    # 解析消息头
    #print('*' * 30 + 'MSG_HEAD ' + '*' * 30)
    for idx, content in enumerate(msg_head_width):
        #print(str_head_name[idx] + ':' + str(item.get_segment_by_index(item.curBitsIndex, msg_head_width[idx])))
        dic_msg[str_head_name[idx]] = str(item.get_segment_by_index(item.curBitsIndex, msg_head_width[idx]))

    #print('*' * 30 + 'MSG_CONTENT ' + '*' * 30)
    # 解析内容
    while item.curBitsIndex < len(item.get_stream_in_bytes())*8-1:
        nid = item.get_segment_by_index(item.curBitsIndex, 8)
        #print('nid:' + str(nid))
        l_pkt = item.get_segment_by_index(item.curBitsIndex, 13)
        #print('l_pkt:' + str(l_pkt))
        if nid == 0:
            mvb_recv = hex(item.get_segment_by_index(item.curBitsIndex, l_pkt - 21)).upper()[2:]
            if len(mvb_recv) % 2 == 0:
                dic_mvb['tcms2ato'] = 'MVB[3346]:039A120D'+mvb_recv
            else:
                dic_mvb['tcms2ato'] = 'MVB[3346]:039A120D'+'0'+mvb_recv
        elif nid == 1:
            ato_ctrl = hex(item.get_segment_by_index(item.curBitsIndex, l_pkt - 21)).upper()[2:]
            if len(ato_ctrl) % 2 == 0:
                dic_mvb['ato2tcms_ctrl'] = 'MVB[3344]:01CF100D'+ato_ctrl
            else:
                dic_mvb['ato2tcms_ctrl'] = 'MVB[3344]:01CF100D'+'0'+ato_ctrl
        elif nid == 2:
            ato_state = hex(item.get_segment_by_index(item.curBitsIndex, l_pkt - 21)).upper()[2:]
            if len(ato_ctrl) % 2 == 0:
                dic_mvb['ato2tcms_state'] = 'MVB[3345]:01CF110D'+ato_state
            else:
                dic_mvb['ato2tcms_state'] = 'MVB[3345]:01CF110D'+'0'+ato_state
        elif nid == 3:
            item.get_segment_by_index(item.curBitsIndex, 8)
            l_msg = item.get_segment_by_index(item.curBitsIndex, 8)
            # 记录bit数
            bit_idx = item.curBitsIndex
            byte_idx = item.curBytesIndex
            # 以下为lpacket描述范围
            item.get_segment_by_index(item.curBitsIndex, 8)
            all_len = item.get_segment_by_index(item.curBitsIndex, 13)
            # 监测ATP2ATO数据包（L_PACKET）
            while all_len != (item.curBitsIndex - bit_idx):
                nid = item.get_segment_by_index(item.curBitsIndex, 8)
                if nid == 0:
                    item.get_segment_by_index(item.curBitsIndex, 13)
                    item.get_segment_by_index(item.curBitsIndex, 2)
                    item.get_segment_by_index(item.curBitsIndex, 24)  # NID_LRBG
                    item.get_segment_by_index(item.curBitsIndex, 15)
                    item.get_segment_by_index(item.curBitsIndex, 2)
                    item.get_segment_by_index(item.curBitsIndex, 2)
                    item.get_segment_by_index(item.curBitsIndex, 15)
                    item.get_segment_by_index(item.curBitsIndex, 15)
                    Q_LENGTH = item.get_segment_by_index(item.curBitsIndex, 2)
                    # 列车完整性确认
                    if Q_LENGTH == 1 or Q_LENGTH == 2:
                        L_TRAINT = item.get_segment_by_index(item.curBitsIndex, 15)
                        item.get_segment_by_index(item.curBitsIndex, 7)
                        item.get_segment_by_index(item.curBitsIndex, 2)
                        item.get_segment_by_index(item.curBitsIndex, 4)
                        M_LEVEL =  item.get_segment_by_index(item.curBitsIndex, 3)
                        if M_LEVEL == 1:
                            NID_STM = item.get_segment_by_index(item.curBitsIndex, 8)
                    else:
                        item.get_segment_by_index(item.curBitsIndex, 7)
                        item.get_segment_by_index(item.curBitsIndex, 2)
                        item.get_segment_by_index(item.curBitsIndex, 4)
                        M_LEVEL = item.get_segment_by_index(item.curBitsIndex, 3)
                        if M_LEVEL == 1:
                            NID_STM = item.get_segment_by_index(item.curBitsIndex, 8)
                elif nid == 1:
                    item.get_segment_by_index(item.curBitsIndex, 13)
                    item.get_segment_by_index(item.curBitsIndex, 2)
                    item.get_segment_by_index(item.curBitsIndex, 24)  # NID_LRBG
                    item.get_segment_by_index(item.curBitsIndex, 24)  # NID_PRVBG
                    item.get_segment_by_index(item.curBitsIndex, 15)
                    item.get_segment_by_index(item.curBitsIndex, 2)
                    item.get_segment_by_index(item.curBitsIndex, 2)
                    item.get_segment_by_index(item.curBitsIndex, 15)
                    item.get_segment_by_index(item.curBitsIndex, 15)
                    Q_LENGTH = item.get_segment_by_index(item.curBitsIndex, 2)
                    # 列车完整性确认
                    if Q_LENGTH == 1 or Q_LENGTH == 2:
                        L_TRAINT = item.get_segment_by_index(item.curBitsIndex, 15)
                        item.get_segment_by_index(item.curBitsIndex, 7)
                        item.get_segment_by_index(item.curBitsIndex, 2)
                        item.get_segment_by_index(item.curBitsIndex, 4)
                        M_LEVEL = item.get_segment_by_index(item.curBitsIndex, 3)
                        if M_LEVEL == 1:
                            NID_STM = item.get_segment_by_index(item.curBitsIndex, 8)
                    else:
                        item.get_segment_by_index(item.curBitsIndex, 7)
                        item.get_segment_by_index(item.curBitsIndex, 2)
                        item.get_segment_by_index(item.curBitsIndex, 4)
                        M_LEVEL = item.get_segment_by_index(item.curBitsIndex, 3)
                        if M_LEVEL == 1:
                            NID_STM = item.get_segment_by_index(item.curBitsIndex, 8)
                elif nid == 2:
                    q_atopermit = item.get_segment_by_index(item.curBitsIndex, 2)
                    q_ato_hardpermit = item.get_segment_by_index(item.curBitsIndex, 2)
                    q_leftdoorpermit = item.get_segment_by_index(item.curBitsIndex, 2)
                    q_rightdoorpermit =  item.get_segment_by_index(item.curBitsIndex, 2)
                    q_door_cmd_dir =  item.get_segment_by_index(item.curBitsIndex, 2)
                    q_tb = item.get_segment_by_index(item.curBitsIndex, 2)
                    v_target = item.get_segment_by_index(item.curBitsIndex, 16)
                    d_target = item.get_segment_by_index(item.curBitsIndex, 32)
                    m_level = item.get_segment_by_index(item.curBitsIndex, 3)  # M_LEVEL
                    m_mode = item.get_segment_by_index(item.curBitsIndex, 4)  # M_MODE
                    o_train_pos = item.get_segment_by_index(item.curBitsIndex, 32)
                    v_permitted = item.get_segment_by_index(item.curBitsIndex, 16)
                    d_ma = item.get_segment_by_index(item.curBitsIndex, 16)
                    m_ms_cmd = item.get_segment_by_index(item.curBitsIndex, 2)  # M_MS_CMD
                    d_neu_sec = item.get_segment_by_index(item.curBitsIndex, 16) # D_DEU_SEC
                    m_low_frequency = item.get_segment_by_index(item.curBitsIndex, 8)
                    q_stopstatus = item.get_segment_by_index(item.curBitsIndex, 4)
                    m_atp_stop_err = item.get_segment_by_index(item.curBitsIndex, 16)
                    d_station_mid_pos = item.get_segment_by_index(item.curBitsIndex, 32)
                    d_jz_sig_pos = item.get_segment_by_index(item.curBitsIndex, 32)
                    d_cz_sig_pos = item.get_segment_by_index(item.curBitsIndex, 32)
                    d_tsm = item.get_segment_by_index(item.curBitsIndex, 32)
                    m_cab_state = item.get_segment_by_index(item.curBitsIndex, 2) # M_CAB_STATE
                    m_position = item.get_segment_by_index(item.curBitsIndex, 32)
                    m_tco_state = item.get_segment_by_index(item.curBitsIndex, 2)
                    reserve = item.get_segment_by_index(item.curBitsIndex, 2)
                    # 解析到2包
                    dic_atp2ato_pkt[2] = [q_atopermit, q_ato_hardpermit, q_leftdoorpermit, q_rightdoorpermit,
                                          q_door_cmd_dir, q_tb, v_target, d_target, m_level, m_mode, o_train_pos,
                                          v_permitted, d_ma, m_ms_cmd, d_neu_sec, m_low_frequency, q_stopstatus,
                                          m_atp_stop_err, d_station_mid_pos, d_jz_sig_pos, d_cz_sig_pos, d_tsm,
                                          m_cab_state, m_position, m_tco_state, reserve]
                elif nid == 3:
                    item.get_segment_by_index(item.curBitsIndex, 32)
                elif nid == 4:
                    dic_sdu['atp_v'] = item.get_segment_by_index(item.curBitsIndex, 16, sign=1)
                    dic_sdu['atp_s'] = item.get_segment_by_index(item.curBitsIndex, 32)
                elif nid == 5:
                    n_units = item.get_segment_by_index(item.curBitsIndex, 8)
                    nid_operational = item.get_segment_by_index(item.curBitsIndex, 32)
                    nid_driver = item.get_segment_by_index(item.curBitsIndex, 32)
                    btm_antenna_position = item.get_segment_by_index(item.curBitsIndex, 8)
                    l_door_dis = item.get_segment_by_index(item.curBitsIndex, 16)
                    l_sdu_wh_size_1 = item.get_segment_by_index(item.curBitsIndex, 16)
                    l_sdu_wh_size_2 = item.get_segment_by_index(item.curBitsIndex, 16)
                    t_cutoff_traction = item.get_segment_by_index(item.curBitsIndex, 16)
                    nid_engine = item.get_segment_by_index(item.curBitsIndex, 24)
                    v_ato_permitted = item.get_segment_by_index(item.curBitsIndex, 4)
                    dic_atp2ato_pkt[5] = [n_units, nid_operational, nid_driver, btm_antenna_position, l_door_dis,
                                          l_sdu_wh_size_1, l_sdu_wh_size_2, t_cutoff_traction, nid_engine,
                                          v_ato_permitted]
                elif nid == 6:
                    item.get_segment_by_index(item.curBitsIndex, 8)
                    item.get_segment_by_index(item.curBitsIndex, 8)
                    item.get_segment_by_index(item.curBitsIndex, 8)
                    item.get_segment_by_index(item.curBitsIndex, 8)
                    item.get_segment_by_index(item.curBitsIndex, 8)
                    item.get_segment_by_index(item.curBitsIndex, 8)
                elif nid == 7:
                    nid_bg = item.get_segment_by_index(item.curBitsIndex, 24)
                    t_middle = item.get_segment_by_index(item.curBitsIndex, 32)
                    d_pos_adj = item.get_segment_by_index(item.curBitsIndex, 32, sign=1)
                    NID_XUSER = item.get_segment_by_index(item.curBitsIndex, 9)
                    # 解析到7包
                    dic_atp2ato_pkt[7] = [nid_bg, t_middle, d_pos_adj, NID_XUSER]
                    if NID_XUSER == 13:
                        q_scale = item.get_segment_by_index(item.curBitsIndex, 2)
                        q_platform = item.get_segment_by_index(item.curBitsIndex, 2)
                        q_door = item.get_segment_by_index(item.curBitsIndex, 2)
                        n_d = item.get_segment_by_index(item.curBitsIndex, 24)
                        d_stop = item.get_segment_by_index(item.curBitsIndex, 15)
                        # 解析到7包
                        dic_atp2ato_pkt[7] = [nid_bg, t_middle, d_pos_adj, NID_XUSER, q_scale, q_platform, q_door, n_d,
                                              d_stop]
                elif nid == 8:
                    q_tsrs = item.get_segment_by_index(item.curBitsIndex, 1)
                    nid_c = item.get_segment_by_index(item.curBitsIndex, 10)
                    nid_tsrs = item.get_segment_by_index(item.curBitsIndex, 14)
                    nid_radio_h = item.get_segment_by_index(item.curBitsIndex, 32)
                    nid_radio_l = item.get_segment_by_index(item.curBitsIndex, 32)
                    q_sleepssion = item.get_segment_by_index(item.curBitsIndex, 1)
                    m_type = item.get_segment_by_index(item.curBitsIndex, 3)
                    # 解析到8包
                    dic_atp2ato_pkt[8] = [q_tsrs, nid_c, nid_tsrs, nid_radio_h, nid_radio_l, q_sleepssion, m_type]
                elif nid == 9:
                    N_ITER = item.get_segment_by_index(item.curBitsIndex, 5)
                    for i in range(N_ITER):
                        item.get_segment_by_index(item.curBitsIndex, 32)
                        item.get_segment_by_index(item.curBitsIndex, 32)
                        item.get_segment_by_index(item.curBitsIndex, 4)
                else:
                    print('err!!!!!')
            # 消息校验和监测
            if all_len == (item.curBitsIndex - bit_idx):
                if (all_len + 16) % 8 == 0:    # 刚好除整数
                    pass
                else: # 重新校正bit索引
                    padding_bit = int(((all_len + 16 + 7) // 8) * 8) - all_len - 16  # 字节下跳的bit数，减去消息头16bit和内容bit后
                    item.get_segment_by_index(item.curBitsIndex, padding_bit)
                # 计算分析消息结尾
                item.get_segment_by_index(item.curBitsIndex, 32)
                item.get_segment_by_index(item.curBitsIndex, 32)
                item.get_segment_by_index(item.curBitsIndex, 32)
                if l_msg == item.curBytesIndex - byte_idx + 2:
                    pass  # 消息校验正确不打印
                else:
                    print('fatal err！ l_msg %d, real %d' % (l_msg, item.curBytesIndex - byte_idx + 2))
        elif nid == 4:
            item.get_segment_by_index(item.curBitsIndex, 8)
            l_msg = item.get_segment_by_index(item.curBitsIndex, 8)
            # 记录bit数
            bit_idx = item.curBitsIndex
            byte_idx = item.curBytesIndex
            # 以下为lpacket描述范围
            item.get_segment_by_index(item.curBitsIndex, 8)
            all_len = item.get_segment_by_index(item.curBitsIndex, 13)
            # 监测ATO2ATP数据包（L_PACKET）
            while all_len != (item.curBitsIndex - bit_idx):
                nid = item.get_segment_by_index(item.curBitsIndex, 8)
                if nid == 130:
                    m_ato_mode = item.get_segment_by_index(item.curBitsIndex, 4)
                    m_door_mode = item.get_segment_by_index(item.curBitsIndex, 2)
                    m_door_status = item.get_segment_by_index(item.curBitsIndex, 2)
                    m_atoerror = item.get_segment_by_index(item.curBitsIndex, 16)
                    m_ato_stop_error = item.get_segment_by_index(item.curBitsIndex, 16)
                    dic_ato2atp_pkt[130] = [m_atoerror, m_ato_mode, m_ato_stop_error, m_door_mode, m_door_status]
                elif nid == 131:
                    m_ato_tbs = item.get_segment_by_index(item.curBitsIndex, 2)
                    m_ato_skip = item.get_segment_by_index(item.curBitsIndex, 2)
                    m_ato_plan = item.get_segment_by_index(item.curBitsIndex, 2)
                    m_ato_time = item.get_segment_by_index(item.curBitsIndex, 16)
                    m_tcms_com = item.get_segment_by_index(item.curBitsIndex, 2)
                    m_gprs_radio = item.get_segment_by_index(item.curBitsIndex, 2)
                    m_gprs_session = item.get_segment_by_index(item.curBitsIndex, 2)
                    m_ato_control_strategy = item.get_segment_by_index(item.curBitsIndex, 4)
                    paddings = item.get_segment_by_index(item.curBitsIndex, 16)
                    dic_ato2atp_pkt[131] = [m_ato_plan, m_ato_skip, m_ato_tbs, m_ato_time, m_gprs_radio, m_gprs_session,
                                            m_tcms_com, m_ato_control_strategy, paddings]  
                elif nid == 132:
                    pass
                elif nid == 133:
                    item.get_segment_by_index(item.curBitsIndex, 10)
                    item.get_segment_by_index(item.curBitsIndex, 14)
                    item.get_segment_by_index(item.curBitsIndex, 64)
                elif nid == 134:
                    item.get_segment_by_index(item.curBitsIndex, 8)
                    item.get_segment_by_index(item.curBitsIndex, 1)
                    L_TEXT = item.get_segment_by_index(item.curBitsIndex, 8)
                    for i in range(L_TEXT):
                        item.get_segment_by_index(item.curBitsIndex, 8)
                else:
                    print('err!!!!!')
            # 消息校验和监测
            if all_len == (item.curBitsIndex - bit_idx):
                if (all_len + 16) % 8 == 0:  # 刚好除整数
                    pass
                else:  # 重新校正bit索引
                    padding_bit = int(((all_len + 16 + 7) // 8) * 8) - all_len - 16  # 字节下跳的bit数，减去消息头16bit和内容bit后
                    item.get_segment_by_index(item.curBitsIndex, padding_bit)
                # 计算分析消息结尾
                item.get_segment_by_index(item.curBitsIndex, 32)
                item.get_segment_by_index(item.curBitsIndex, 32)
                item.get_segment_by_index(item.curBitsIndex, 32)
                if l_msg == item.curBytesIndex - byte_idx + 2:
                    pass  # 消息校验正确不打印
                else:
                    print('fatal err！ l_msg %d, real %d' % (l_msg, item.curBytesIndex - byte_idx + 2))
        elif nid == 9:
            dic_sdu['ato_v'] = item.get_segment_by_index(item.curBitsIndex, 16)
            dic_sdu['ato_s'] = item.get_segment_by_index(item.curBitsIndex, 32)
        elif nid == 25:
            rp_start_train = item.get_segment_by_index(item.curBitsIndex, 1)
            rp_final_station = item.get_segment_by_index(item.curBitsIndex, 1)
            rp_q_pl_legal = item.get_segment_by_index(item.curBitsIndex, 1)
            rp_pl_update = item.get_segment_by_index(item.curBitsIndex, 32)
            rp_pl_num = item.get_segment_by_index(item.curBitsIndex, 2)
            for rp_cnt in range(rp_pl_num):
                rp_ob_sys_time = item.get_segment_by_index(item.curBitsIndex, 32)
                rp_wayside_time = item.get_segment_by_index(item.curBitsIndex, 32)
                rp_pl_legal_arrival_time = item.get_segment_by_index(item.curBitsIndex, 32)
                rp_pl_legal_depart_time = item.get_segment_by_index(item.curBitsIndex, 32)
                rp_pl_legal_arrival_track = item.get_segment_by_index(item.curBitsIndex, 24)
                rp_pl_legal_depart_track = item.get_segment_by_index(item.curBitsIndex, 24)
                rp_pl_legal_skip = item.get_segment_by_index(item.curBitsIndex, 2)
                rp_pl_legal_task = item.get_segment_by_index(item.curBitsIndex, 2)
            rp_pl_out_time = item.get_segment_by_index(item.curBitsIndex, 1)
            rp_pl_stn_state = item.get_segment_by_index(item.curBitsIndex, 2)
            rp_pl_track_balise = item.get_segment_by_index(item.curBitsIndex, 24)
            rp_pl_track_plan = item.get_segment_by_index(item.curBitsIndex, 24)
            rp_pl_in_use = item.get_segment_by_index(item.curBitsIndex, 2)
            rp_pl_valid = item.get_segment_by_index(item.curBitsIndex, 1)
            rp_pl_output_arr_time = item.get_segment_by_index(item.curBitsIndex, 32)
            rp_pl_output_depart_time = item.get_segment_by_index(item.curBitsIndex, 32)
            rp_pl_output_skip = item.get_segment_by_index(item.curBitsIndex, 2)
            rp_pl_output_task = item.get_segment_by_index(item.curBitsIndex, 2)
        elif nid == 53:   # ATO停车状态
            q_stable = str(item.get_segment_by_index(item.curBitsIndex, 2))
            q_real_stable = str(item.get_segment_by_index(item.curBitsIndex, 2))
            ato_stop_err = str(item.get_segment_by_index(item.curBitsIndex, 16, sign=1))
            dic_msg['stop_state'] = (q_stable, q_real_stable, ato_stop_err)
        elif nid == 52:
            o_jd_stop = str(item.get_segment_by_index(item.curBitsIndex, 32))
            o_stn_dis_stop = str(item.get_segment_by_index(item.curBitsIndex, 32))
            o_mid_stop = str(item.get_segment_by_index(item.curBitsIndex, 32))
            o_ma_stop = str(item.get_segment_by_index(item.curBitsIndex, 32))
            o_stop_use = str(item.get_segment_by_index(item.curBitsIndex, 32))
            q_platform = str(item.get_segment_by_index(item.curBitsIndex, 1))
            dic_msg['stop'] = (o_jd_stop, o_stn_dis_stop, o_mid_stop, o_ma_stop, o_stop_use, q_platform)
        elif nid == 54:
            v_ato_cmd = str(item.get_segment_by_index(item.curBitsIndex, 16))
            v_atp_cmd = str(item.get_segment_by_index(item.curBitsIndex, 16))
            ctrl_machine = str(item.get_segment_by_index(item.curBitsIndex, 6))
            adj_ramp = str(item.get_segment_by_index(item.curBitsIndex, 8, sign=1))
            adj_es_ramp = str(item.get_segment_by_index(item.curBitsIndex, 8, sign=1))
            v_s_target = str(item.get_segment_by_index(item.curBitsIndex, 16))
            o_s_target = str(item.get_segment_by_index(item.curBitsIndex, 32))
            lvl_raw = str(item.get_segment_by_index(item.curBitsIndex, 8, sign=1))
            lvl_filter_b = str(item.get_segment_by_index(item.curBitsIndex, 8, sign=1))
            lvl_filter_p = str(item.get_segment_by_index(item.curBitsIndex, 8, sign=1))
            lvl_filter_ramp = str(item.get_segment_by_index(item.curBitsIndex, 8, sign=1))
            lvl_filter_wind = str(item.get_segment_by_index(item.curBitsIndex, 8, sign=1))
            lvl_filter_gfx = str(item.get_segment_by_index(item.curBitsIndex, 8, sign=1))
            lvl_filter_out = str(item.get_segment_by_index(item.curBitsIndex, 8, sign=1))
            q_ato_cutoff = str(item.get_segment_by_index(item.curBitsIndex, 4))
            o_es_pos = str(item.get_segment_by_index(item.curBitsIndex, 32))
            v_es_speed = str(item.get_segment_by_index(item.curBitsIndex, 16))
            o_ma = str(item.get_segment_by_index(item.curBitsIndex, 32))
            # 解析到了关键包
            dic_msg['sc'] = (dic_msg['m_pos'], dic_msg['v_speed'], v_ato_cmd, v_atp_cmd, lvl_filter_out, lvl_filter_out,
                             o_es_pos, v_es_speed, adj_ramp, adj_es_ramp, v_s_target, o_s_target, o_ma, o_ma,
                             ctrl_machine)
        elif nid == 84:
            item.get_segment_by_index(item.curBitsIndex, 8)   # 主控主版本
            item.get_segment_by_index(item.curBitsIndex, 8)   # 主控中版本
            item.get_segment_by_index(item.curBitsIndex, 8)   # 主控小版本
            ret_sig = -2
            return ret_sig   # 存在启机过程，重新生成解析文件
        else:
            item.get_segment_by_index(item.curBitsIndex, l_pkt - 21)
            #print('content:' + hex(item.get_segment_by_index(item.curBitsIndex, l_pkt - 21)))

        # 记录板消息，下一次监测前，判断退出
        if item.curBitsIndex >= len(item.get_stream_in_bytes())*8-1-8-8:
            break
    else:
        pass
    # 解析完成
    return ret_sig


g_q_platform = '0'
g_o_jd = '0'
g_o_stn_dis = '0'
g_o_ma = '0'
g_ato_stop_err = '0'
g_stop_use = '0'


# 按照调试记录文件进行转义成工具文件
def trans_content(path_read=str, path_write=str):
    """
    读取记录板文件并转义为串口工具可读取文件
    :param path_read: 读取文件路径
    :param path_write: 写入文件路径
    :return: None
    """
    global dic_msg
    global dic_atp2ato_pkt
    global dic_sdu
    global dic_mvb

    global g_q_platform
    global g_o_jd
    global g_o_stn_dis
    global g_o_ma
    global g_ato_stop_err
    global g_stop_use
    ret_sig = 1
    # 处理文件分割
    trans_part = 0
    tmp_path_write = path_write   # 记录原始路径，用于后续创建
    # 读取记录文件
    with open(path_read, 'r') as fr:
        # 需要继续执行
        while True:
            # 创建转义后的文件
            with open(path_write, 'w') as fw:
                # 遍历记录文件
                for item in fr:
                    try:
                        #dic_msg = {}
                        ret_sig = ctrl_process_transfer(item.rstrip())
                    except Exception as errInfo:
                        print(errInfo)
                    # 若获取到结果
                    if ret_sig == 0:
                        t_ato = dic_msg['t_ato']
                        n_cycle = dic_msg['n_cycle']
                        m_atomode = dic_msg['m_atomode']
                        dt = time.gmtime(int(dic_msg['t_atoutc'])+3600*8)

                        if 'stop' in dic_msg.keys():
                            stop = dic_msg['stop']
                            g_q_platform = stop[5]
                            g_o_ma = stop[3]
                            g_o_jd = stop[0]
                            g_stop_use = stop[4]
                            g_o_stn_dis = stop[1]

                        if 'stop_state' in dic_msg.keys():
                            stop_state = dic_msg['stop_state']
                            g_ato_stop_err = stop_state[2]

                        # 所有完全的情况
                        if '3' == m_atomode or '2' == m_atomode:
                            fw.write('---CORE_TARK CY_B %s,%s---\n' % (t_ato, n_cycle))
                            fw.write('time:%s-%s-%s %s:%s:%s,system:M\n' % (dt.tm_year, dt.tm_mon, dt.tm_mday, dt.tm_hour,
                                                                          dt.tm_min, dt.tm_sec))
                            # 速传信息
                            if dic_sdu['atp_v'] and dic_sdu['atp_s']:
                                fw.write('v&p_atp:%d,%d\n' % (dic_sdu['atp_v'], dic_sdu['atp_s']))
                            if dic_sdu['ato_v'] and dic_sdu['ato_s']:
                                fw.write('v&p_ato:%d,%d\n' % (dic_sdu['ato_v'], dic_sdu['ato_s']))
                            # 模式状态
                            fw.write('FSM{%s %s 1 1 1 1}sg{2 0 1003934828 21000 AA 2B}ss{0 %s}\n' % (m_atomode,
                                                                                                     m_atomode,
                                                                                                     g_q_platform))
                            # 数据包
                            if 130 in dic_ato2atp_pkt.keys():
                                fw.write('[O->P]SP130:')
                                for idx, item in enumerate(dic_ato2atp_pkt[130]):
                                    fw.write(str(item)+',')
                                fw.write('\n')
                            if 131 in dic_ato2atp_pkt.keys():
                                fw.write('[O->P]SP131:')
                                for item in dic_ato2atp_pkt[131]:
                                    fw.write(str(item)+',')
                                fw.write('\n')
                            if 2 in dic_atp2ato_pkt.keys():
                                fw.write('[P->O]SP2')
                                for item in dic_atp2ato_pkt[2]:
                                    fw.write(',' + str(item))
                                fw.write('\n')

                            if 5 in dic_atp2ato_pkt.keys():
                                fw.write('[P->O]SP5,n_units %d,nid_operational %d,nid_driver %d,'
                                         'btm_antenna_position %d,l_door_dis %d, l_sdu_wh_size_1 %d,'
                                         'l_sdu_wh_size_2 %d,t_cutoff_traction %d,nid_engine %d,'
                                         'v_ato_permitted %d\n' % (dic_atp2ato_pkt[5][0],
                                                                   dic_atp2ato_pkt[5][1],
                                                                   dic_atp2ato_pkt[5][2],
                                                                   dic_atp2ato_pkt[5][3],
                                                                   dic_atp2ato_pkt[5][4],
                                                                   dic_atp2ato_pkt[5][5],
                                                                   dic_atp2ato_pkt[5][6],
                                                                   dic_atp2ato_pkt[5][7],
                                                                   dic_atp2ato_pkt[5][8],
                                                                   dic_atp2ato_pkt[5][9]))
                            if 8 in dic_atp2ato_pkt.keys():
                                fw.write('[P->O]SP8,q_tsrs %d,nid_c %d,nid_tsrs %d,nid_radio_h %x,nid_radio_l %x,'
                                         'q_sleepssion %d, m_type %d\n' % (dic_atp2ato_pkt[8][0],
                                                                           dic_atp2ato_pkt[8][1],
                                                                           dic_atp2ato_pkt[8][2],
                                                                           dic_atp2ato_pkt[8][3],
                                                                           dic_atp2ato_pkt[8][4],
                                                                           dic_atp2ato_pkt[8][5],
                                                                           dic_atp2ato_pkt[8][6]))
                            if 7 in dic_atp2ato_pkt.keys():
                                if dic_atp2ato_pkt[7][3] == 13:
                                    fw.write('[P->O]SP7,nid_bg %d,t_middle %d,d_pos_adj %d,nid_xuser %d,q_scale %d,'
                                             'q_platform %d,q_door %d,n_d %d,d_stop %d\n' % (dic_atp2ato_pkt[7][0],
                                                                                            dic_atp2ato_pkt[7][1],
                                                                                            dic_atp2ato_pkt[7][2],
                                                                                            dic_atp2ato_pkt[7][3],
                                                                                            dic_atp2ato_pkt[7][4],
                                                                                            dic_atp2ato_pkt[7][5],
                                                                                            dic_atp2ato_pkt[7][6],
                                                                                            dic_atp2ato_pkt[7][7],
                                                                                            dic_atp2ato_pkt[7][8]))
                                else:
                                    fw.write('[P->O]SP7,nid_bg %d,t_middle %d,d_pos_adj %d,nid_xuser 0,q_scale 0,'
                                             'q_platform 0,q_door 0,n_d 0,d_stop 0\n' % (dic_atp2ato_pkt[7][0],
                                                                                         dic_atp2ato_pkt[7][1],
                                                                                         dic_atp2ato_pkt[7][2]))
                            if 'sc' in dic_msg.keys():
                                sc = dic_msg['sc']
                                fw.write('stoppoint:jd=%s ref=%s ma=%s\n' % (g_o_jd, g_o_stn_dis, g_o_ma))
                                fw.write('SC{%s %s %s %s %s %s %s %s %s %s}t %s %s %s %s,%s} f %s %s %s -12} p1 2}CC\n'
                                        % (sc[0], sc[1], sc[2], sc[3], sc[4], sc[5], sc[6], sc[7], sc[8], sc[9],
                                            sc[10], sc[11], sc[12], sc[13], g_stop_use, g_ato_stop_err, sc[14],
                                           g_q_platform))
                            # MVB 数据
                            if dic_mvb['tcms2ato']:
                                fw.write(dic_mvb['tcms2ato']+'\n')
                            if dic_mvb['ato2tcms_state']:
                                fw.write(dic_mvb['ato2tcms_state']+'\n')
                            if dic_mvb['ato2tcms_ctrl']:
                                fw.write(dic_mvb['ato2tcms_ctrl']+'\n')

                            fw.write('---CORE_TARK CY_E %s,%s---\n' % (t_ato, n_cycle))  # 显示周期尾
                    elif ret_sig == -2:     # 当解析出启机记录时
                        trans_part = trans_part+1
                        path_write = tmp_path_write.replace('.txt', str(trans_part)+'.txt')  # 创建新的文件
                        break
                    else:
                        pass   # 否则直接跳过
                # 将缓冲写入当前文件
                fw.flush()
            # 检查是否为文件分割还是其他执行
            if ret_sig == -2:
                pass    # 其他情况均在遍历中执行完，ret_sig为0，-1，1
            else:
                break


# 指定基础路径，每次调用前删除DataFilesTrans文件目录
keyWords = 'DataFiles'  # 文件关键信息，文件夹
basePath = os.path.abspath(os.path.dirname(__file__))
files = os.listdir(basePath)

# 当已经存在转义路径时直接退出
if keyWords + 'Trans' in files:
    print("转义路径存在，先删除路径，避免数据丢失！")
else:
    # 搜索记录板数据路径并创建转义后的路径
    for fileName in files:
        fullPath = os.path.join(basePath, fileName)
        if os.path.isdir(fullPath):
            # 搜索关键字所在的路径
            if keyWords == os.path.basename(fullPath):
                basePath = fullPath  # 更新基础文件路径
                try:
                    # 创建镜像的转义路径
                    copy_file_dir(fullPath, fullPath.replace(keyWords, keyWords+'Trans'))
                except Exception as err:
                    print(err)
                break

    # 搜索指定关键路径下所有记录文件
    recordFileList = []
    # 获取所有记录文件
    recordFileList = get_file_list(recordFileList, basePath, '.txt')

    print('*'*10+'文件遍历'+'*'*10)
    # 创建线程队列
    thList = []
    # 遍历记录文件
    for recordFile in recordFileList:
        print(recordFile)
        # 按照之前创建目录规则，创建新的文件名
        trans_file = recordFile.replace('.txt', '_trans.txt').replace(keyWords, keyWords+'Trans', 1)   # 定义转换后的文件名称
        # 对每个转换文件过程创建线程
        t = threading.Thread(target=trans_content, args=(recordFile, trans_file))  # 添加内容
        thList.append(t)
    print('*'*10+'开启线程'+'*'*10)
    tStart = time.time()
    # 开启线程
    for th in thList:
        th.start()
        print('th-'+ th.name)
        th.join()
    tStop = time.time()
    print('耗时 %d' % (tStop-tStart))


