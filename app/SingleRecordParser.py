from CommonParse import BytesStream
from app.BaseMethod import iner_escape_reverse

streamReverseEsc = iner_escape_reverse('7EC9355800220D980D4D94F2F1534291DADAFC51081209022908303827866028194600A002A91794C5280FC0412BF000000000000000000000000000000004095F8AA0005D21DFFFE02B10BE2000000003405B7D5FFFFFFFFFFFFFFFFFFFFFFF9DBDAAFB1DBDAAFB00022A0660000000000000000001540002257D5D555460000000000000000000000000000625D2D49FA0EA0180D477DF0210817D5FE183D0013540000001007D5EB303B5B655821A35214BFFFCAC20000001D998000175A48001EA0C8003E93010005D21DA000043F2C01A8EFBEFD324CE207F')
if streamReverseEsc == '':
    print("err stream, can not analysis!")
item = BytesStream(streamReverseEsc)
msg_head_width = [8, 8, 10, 2, 1, 32, 32, 32, 32, 16, 3]
str_head_name = ['escap_head', 'nid_msg', 'l_msg', 'nid_modle', 'q_standby', 'n_cycle',
                 't_ato', 't_atoutc', 'm_pos', 'v_speed', 'm_atomode']

print('*'*30 + 'MSG_HEAD '+'*'*30)
for idx, content in enumerate(msg_head_width):
    print(str_head_name[idx] + ':' + str(item.fast_get_segment_by_index(item.curBitsIndex, msg_head_width[idx])))
    #print('bitoffset ' + str(item.curBitsIndex))


print('*'*30 +'MSG_CONTENT '+'*'*30)
# 解析内容
while item.curBitsIndex < len(item.get_stream_in_bytes()) * 8 - 1:
    nid = item.get_segment_by_index(item.curBitsIndex, 8)
    print('nid:' + str(nid))
    l_pkt = item.get_segment_by_index(item.curBitsIndex, 13)
    print('l_pkt:' + str(l_pkt))
    if nid < 9:
        print('content:' + hex(item.get_segment_by_index(item.curBitsIndex, l_pkt - 21)))
    else:
        if nid == 25:
            print('rp_start_train:' + str(item.get_segment_by_index(item.curBitsIndex, 1)))
            print('rp_final_station:' + str(item.get_segment_by_index(item.curBitsIndex, 1)))
            print('rp_q_pl_legal:' + str(item.get_segment_by_index(item.curBitsIndex, 1)))
            print('rp_pl_update:' + str(item.get_segment_by_index(item.curBitsIndex, 32)))
            rp_pl_num = item.get_segment_by_index(item.curBitsIndex, 2)
            print('rp_pl_num:' + str(rp_pl_num))
            for rp_cnt in range(0):
                print('-' * 15 + 'PKT_CONTENT '+ str(rp_cnt) + '-' * 15)
                print('rp_ob_sys_time:' + str(item.get_segment_by_index(item.curBitsIndex, 32)))
                print('rp_wayside_time:' + str(item.get_segment_by_index(item.curBitsIndex, 32)))
                print('rp_pl_legal_arrival_time:' + str(item.get_segment_by_index(item.curBitsIndex, 32)))
                print('rp_pl_legal_depart_time:' + str(item.get_segment_by_index(item.curBitsIndex, 32)))
                print('rp_pl_legal_arrival_track:' + str(item.get_segment_by_index(item.curBitsIndex, 24)))
                print('rp_pl_legal_depart_track:' + str(item.get_segment_by_index(item.curBitsIndex, 24)))
                print('rp_pl_legal_skip:' + str(item.get_segment_by_index(item.curBitsIndex, 2)))
                print('rp_pl_legal_task:' + str(item.get_segment_by_index(item.curBitsIndex, 2)))
            print('-' * 21 + '-' * 21)
            print('rp_pl_out_time:' + str(item.get_segment_by_index(item.curBitsIndex, 1)))
            print('rp_pl_stn_state:' + str(item.get_segment_by_index(item.curBitsIndex, 2)))
            print('rp_pl_track_balise:' + str(item.get_segment_by_index(item.curBitsIndex, 24)))
            print('rp_pl_track_plan:' + str(item.get_segment_by_index(item.curBitsIndex, 24)))
            print('rp_pl_in_use:' + str(item.get_segment_by_index(item.curBitsIndex, 2)))
            print('rp_pl_valid:' + str(item.get_segment_by_index(item.curBitsIndex, 1)))
            print('rp_pl_output_arr_time:' + str(item.get_segment_by_index(item.curBitsIndex, 32)))
            print('rp_pl_output_depart_time:' + str(item.get_segment_by_index(item.curBitsIndex, 32)))
            print('rp_pl_output_skip:' + str(item.get_segment_by_index(item.curBitsIndex, 2)))
            print('rp_pl_output_task:' + str(item.get_segment_by_index(item.curBitsIndex, 2)))
        elif nid == 80:
            print('base_ver:' + str(item.get_segment_by_index(item.curBitsIndex, 32)))
            print('proj_ver:' + str(item.get_segment_by_index(item.curBitsIndex, 32)))
            print('coast_delay:' + str(item.get_segment_by_index(item.curBitsIndex, 8)))
            print('tract_delay:' + str(item.get_segment_by_index(item.curBitsIndex, 8)))
            print('brake_h_delay:' + str(item.get_segment_by_index(item.curBitsIndex, 8)))
            print('brake_l_delay:' + str(item.get_segment_by_index(item.curBitsIndex, 8)))
            print('l_door_dis:' + str(item.get_segment_by_index(item.curBitsIndex, 12)))
            print('ed_error:' + str(item.get_segment_by_index(item.curBitsIndex, 12)))
            print('train_8:' + str(item.get_segment_by_index(item.curBitsIndex, 10)))
            print('train_17:' + str(item.get_segment_by_index(item.curBitsIndex, 10)))
            print('sdu_pulse:' + str(item.get_segment_by_index(item.curBitsIndex, 8)))
            print('wheel_size:' + str(item.get_segment_by_index(item.curBitsIndex, 11)))
            print('use_pulse1:' + str(item.get_segment_by_index(item.curBitsIndex, 1)))
            print('use_pulse2:' + str(item.get_segment_by_index(item.curBitsIndex, 1)))
            print('sensor_from:' + str(item.get_segment_by_index(item.curBitsIndex, 2)))
            print('atp_comm_timeout:' + str(item.get_segment_by_index(item.curBitsIndex, 16)))
            print('tcms_timeout:' + str(item.get_segment_by_index(item.curBitsIndex, 16)))
            print('recon_time:' + str(item.get_segment_by_index(item.curBitsIndex, 16)))
            print('ramp_cal:' + str(item.get_segment_by_index(item.curBitsIndex, 1)))
            print('vrh_coast:' + str(item.get_segment_by_index(item.curBitsIndex, 1)))
            print('l_stop_win:' + str(item.get_segment_by_index(item.curBitsIndex, 8)))
        elif nid == 54:
            print('v_ato_cmd:' + str(item.get_segment_by_index(item.curBitsIndex, 16)))
            print('v_atp_cmd:' + str(item.get_segment_by_index(item.curBitsIndex, 16)))
            print('ctrl_machine:' + str(item.get_segment_by_index(item.curBitsIndex, 6)))
            print('adj_ramp:' + str(item.get_segment_by_index(item.curBitsIndex, 8)))
            print('adj_es_ramp:' + str(item.get_segment_by_index(item.curBitsIndex, 8)))
            print('v_s_target:' + str(item.get_segment_by_index(item.curBitsIndex, 16)))
            print('o_s_target:' + str(item.get_segment_by_index(item.curBitsIndex, 32)))
            print('lvl_raw:' + str(item.get_segment_by_index(item.curBitsIndex, 8, sign=1)))
            print('lvl_filter_b:' + str(item.get_segment_by_index(item.curBitsIndex, 8, sign=1)))
            print('lvl_filter_p:' + str(item.get_segment_by_index(item.curBitsIndex, 8, sign=1)))
            print('lvl_filter_ramp:' + str(item.get_segment_by_index(item.curBitsIndex, 8, sign=1)))
            print('lvl_filter_wind:' + str(item.get_segment_by_index(item.curBitsIndex, 8, sign=1)))
            print('lvl_filter_gfx:' + str(item.get_segment_by_index(item.curBitsIndex, 8, sign=1)))
            print('lvl_filter_out:' + str(item.get_segment_by_index(item.curBitsIndex, 8, sign=1)))
            print('q_ato_cutoff:' + str(item.get_segment_by_index(item.curBitsIndex, 4)))
            print('o_es_pos:' + str(item.get_segment_by_index(item.curBitsIndex, 32)))
            print('v_es_speed:' + str(item.get_segment_by_index(item.curBitsIndex, 16)))
            print('o_ma:' + str(item.get_segment_by_index(item.curBitsIndex, 32)))
        elif nid == 21:
            n_ssp = item.get_segment_by_index(item.curBitsIndex, 5)
            print('n_ssp:' + str(n_ssp))
            for ssp_cnt in range(n_ssp):
                print('-' * 15 + 'PKT_CONTENT '+ str(ssp_cnt) + '-' * 15)
                print('ssp_pos:' + str(item.get_segment_by_index(item.curBitsIndex, 32)))
                print('d_ssp:' + str(item.get_segment_by_index(item.curBitsIndex, 32)))
                print('v_ssp:' + str(item.get_segment_by_index(item.curBitsIndex, 16)))
            print('-' * 21 + '-' * 21)
            n_tsr = item.get_segment_by_index(item.curBitsIndex, 5)
            print('n_tsr:' + str(n_tsr))
            for tsr_cnt in range(n_tsr):
                print('-' * 15 + 'PKT_CONTENT '+ str(tsr_cnt) + '-' * 15)
                print('tsr_pos:' + str(item.get_segment_by_index(item.curBitsIndex, 32)))
                print('l_tsr:' + str(item.get_segment_by_index(item.curBitsIndex, 32)))
                print('v_tsr:' + str(item.get_segment_by_index(item.curBitsIndex, 16)))
            n_ramp = item.get_segment_by_index(item.curBitsIndex, 5)
            print('n_ramp:' + str(n_ramp))
            for ramp_cnt in range(n_ramp):
                print('-' * 15 + 'PKT_CONTENT '+ str(ramp_cnt) + '-' * 15)
                print('ramp_pos:' + str(item.get_segment_by_index(item.curBitsIndex, 32)))
                print('d_ramp:' + str(item.get_segment_by_index(item.curBitsIndex, 32)))
                print('ramp:' + str(item.get_segment_by_index(item.curBitsIndex, 8)))
            n_stn = item.get_segment_by_index(item.curBitsIndex, 5)
            print('n_stn:' + str(n_stn))
            for stn_cnt in range(n_stn):
                print('-' * 15 + 'PKT_CONTENT '+ str(stn_cnt) + '-' * 15)
                print('stn_pos:' + str(item.get_segment_by_index(item.curBitsIndex, 32)))
                print('d_stn:' + str(item.get_segment_by_index(item.curBitsIndex, 32)))
        else:
            print('content:' + hex(item.get_segment_by_index(item.curBitsIndex, l_pkt - 21)))

    # 在下一次监测前，判断退出
    if item.curBitsIndex >= len(item.get_stream_in_bytes()) * 8 - 1 - 8 - 8:   # 减去第一个8代表尾巴7F，第二个代表一个字节内
        break

    print('Bytesoffset:%d bitoffset:%d' % (item.curBytesIndex, item.curBitsIndex))
    print('\n')

# 结尾打印
print('next index B: ' + hex(item.get_segment_by_index((item.curBytesIndex + 1) * 8, 8)))
print('end:' + hex(item.get_segment_by_index((len(item.get_stream_in_bytes()) - 1) * 8, 8)))

print('allB: ' + str(len(item.get_stream_in_bytes())))