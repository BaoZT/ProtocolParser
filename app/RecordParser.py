from CommonParse import BytesStream


def iner_escape_reverse(stream=str):

    ori_bytes_str = stream[2:(len(stream)-2)]

    if '7E' in ori_bytes_str:
        idx1 = ori_bytes_str.index('7E')
        if idx1 % 2 == 0:
           print('fatal error!')
        else:
            pass

    for idx in range(0, len(ori_bytes_str), 2):
        tmp = ori_bytes_str[idx:idx+2]
        if '7D' == tmp:
            ori_bytes_str = ori_bytes_str[:idx+1] + ori_bytes_str[idx+3:]
        else:
            pass
    return '7E'+ori_bytes_str+'7F'


streamReverseEsc = iner_escape_reverse('7EC96D18002338880DD20BB2ED151F59DF263AF9090B09022908683C784599901A44EF931D7C00DE82FC7C8C0412AF954AA00001248000000000154000000040957CAA00073433116102540BED000000003405B7FFFFFFFFFFFFFFFFFFFFFFF9E07436F9E07436F8CC17A277C8EAAE0075F83E4346277C98EBE006F417E429E6C1071F2321592BFBF80000F03A1B7D5FEBFFFFEBEBFFFC0000157B083E8F03A428C0022BFA61554A000000000000015400022687555580000000000000000000000000000C175880B000B0E6FC4C5CF0000E4CC560780B95001400287A832C04F8B4115315602BB4546C7315E02BB454B773F050CE8C0620058727A98AC0F2C827829824ABB4547D5E1315602BB4546C7315E02BB454B772198AF015DA2A5BB98B2035DA2A7D5FB68C887080DD20BB4037478C4BB4547D5E0BB454B76BB4546C7315E03315602C037478C4BB4547E0BB454FF6BB454B77316407315E032662ACFFFFFFFC80E09EAD00E09EAD3018974B527D5E83A8060372FCD6084242009BA1EE04B5000000053AB30C0EF935820868DAC8633602B08000FFFFFFFFFFFFFFFFFFFFFFFF001C0E034001CD0CE800011A63C06E5F9AF86FC277407F')

item = BytesStream(streamReverseEsc)
msg_head_width = [8, 8, 10, 2, 1, 32, 32, 32, 32, 16, 3]
str_head_name = ['escap_head', 'nid_msg', 'l_msg', 'nid_modle', 'q_standby', 'n_cycle',
                 't_ato', 't_atoutc', 'm_pos', 'v_speed', 'm_atomode']
print('*'*30 + 'MSG_HEAD '+'*'*30)
for idx, content in enumerate(msg_head_width):
    print(str_head_name[idx] + ':' + str(item.get_segment_by_index(item.curBitsIndex, msg_head_width[idx])))
    #print('bitoffset ' + str(item.curBitsIndex))


print('*'*30 +'MSG_CONTENT '+'*'*30)
while item.curBytesIndex < (len(item.get_stream_in_bytes())-2):
    nid = item.get_segment_by_index(item.curBitsIndex, 8)
    print('nid:' + str(nid))
    l_pkt = item.get_segment_by_index(item.curBitsIndex, 13)
    print('l_pkt:' + str(l_pkt))
    if nid < 9:
        if nid == 0:
            print('hear_beat:' + str(item.get_segment_by_index(item.curBitsIndex, 8)))
            print('door_mode(MOMC):' + str(item.get_segment_by_index(item.curBitsIndex, 2)))
            print('door_mode(AOMC):' + str(item.get_segment_by_index(item.curBitsIndex, 2)))
            print('other:' + str(item.get_segment_by_index(item.curBitsIndex, 32*8 - 12)))

        else:
            print('content:' + hex(item.get_segment_by_index(item.curBitsIndex, l_pkt - 21)))
    else:
        if nid == 25:
            print('rp_start_train:' + str(item.get_segment_by_index(item.curBitsIndex, 1)))
            print('rp_final_station:' + str(item.get_segment_by_index(item.curBitsIndex, 1)))
            print('rp_q_pl_legal:' + str(item.get_segment_by_index(item.curBitsIndex, 1)))
            print('rp_pl_update:' + str(item.get_segment_by_index(item.curBitsIndex, 32)))
            rp_pl_num = item.get_segment_by_index(item.curBitsIndex, 2)
            print('rp_pl_num:' + str(rp_pl_num))
            for rp_cnt in range(rp_pl_num):
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

    print('Bytesoffset:%d bitoffset:%d' % (item.curBytesIndex, item.curBitsIndex))
    print('\n')

# 结尾打印
print('next index B: ' + hex(item.get_segment_by_index((item.curBytesIndex + 1) * 8, 8)))
print('end:' + hex(item.get_segment_by_index((len(item.get_stream_in_bytes()) - 1) * 8, 8)))

print('allB: ' + str(len(item.get_stream_in_bytes())))