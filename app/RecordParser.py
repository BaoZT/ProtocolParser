from CommonParse import BytesStream


def escapReverse(stream=str):

    ori_bytes_str = stream[2:(len(stream)-2)]

    if '7E' in ori_bytes_str:
        idx1 = ori_bytes_str.index('7E')
        if idx1 % 2 == 0:
           print('error!')
        else:
            pass

    for idx in range(0,len(ori_bytes_str),2):
        tmp = ori_bytes_str[idx:idx+2]
        if '7D' == tmp:
            ori_bytes_str = ori_bytes_str[:idx+1] + ori_bytes_str[idx+3:]
        else:
            pass
    return '7E'+ori_bytes_str+'7F'


streamReverseEsc = escapReverse('7EC929180002568000EB5EF2E613D5A1DCE5CDE000033200C8198074002408A01680003DF8A020951BAAAA366600000000000000AA0000000204A8DD500042011FFFFFFFF8000000000001A02DBFFFFFFFFFFFFFFFFFFFFFFFCEE7F7500EE7F75006C107082308230C0000053CEE7D5F3B30E44444444444440000000C800FCEE7F9C100022A7A6155546CCC0000000001540002AAAB555580000000000000000000000000007F')

item = BytesStream(streamReverseEsc)
msg_head_width = [8, 8, 10, 2, 1, 32, 32, 32, 32, 16, 3]
str_head_name = ['escap_head', 'nid_msg', 'l_msg', 'nid_modle', 'q_standby', 'n_cycle',
                 't_ato', 't_atoutc', 'm_pos', 'v_speed', 'm_atomode']
print('*'*30 + 'MSG_HEAD '+'*'*30)
for idx, content in enumerate(msg_head_width):
    print(str_head_name[idx] + ':' + str(item.getSegmentByIndex(item.curBitsIndex, msg_head_width[idx])))
    #print('bitoffset ' + str(item.curBitsIndex))


print('*'*30 +'MSG_CONTENT '+'*'*30)
while item.curBytesIndex < (len(item.getStreamInBytes())-2):
    nid = item.getSegmentByIndex(item.curBitsIndex, 8)
    print('nid:' + str(nid))
    l_pkt = item.getSegmentByIndex(item.curBitsIndex, 13)
    print('l_pkt:' + str(l_pkt))
    if nid < 9:
        print('content:' + hex(item.getSegmentByIndex(item.curBitsIndex, l_pkt - 21)))
    else:
        if nid == 25:
            print('rp_start_train:' + str(item.getSegmentByIndex(item.curBitsIndex, 1)))
            print('rp_final_station:' + str(item.getSegmentByIndex(item.curBitsIndex, 1)))
            print('rp_q_pl_legal:' + str(item.getSegmentByIndex(item.curBitsIndex, 1)))
            print('rp_pl_update:' + str(item.getSegmentByIndex(item.curBitsIndex, 32)))
            rp_pl_num = item.getSegmentByIndex(item.curBitsIndex, 2)
            print('rp_pl_num:' + str(rp_pl_num))
            for rp_cnt in range(rp_pl_num):
                print('-' * 15 + 'PKT_CONTENT '+ str(rp_cnt) + '-' * 15)
                print('rp_ob_sys_time:' + str(item.getSegmentByIndex(item.curBitsIndex, 32)))
                print('rp_wayside_time:' + str(item.getSegmentByIndex(item.curBitsIndex, 32)))
                print('rp_pl_legal_arrival_time:' + str(item.getSegmentByIndex(item.curBitsIndex, 32)))
                print('rp_pl_legal_depart_time:' + str(item.getSegmentByIndex(item.curBitsIndex, 32)))
                print('rp_pl_legal_arrival_track:' + str(item.getSegmentByIndex(item.curBitsIndex, 24)))
                print('rp_pl_legal_depart_track:' + str(item.getSegmentByIndex(item.curBitsIndex, 24)))
                print('rp_pl_legal_skip:' + str(item.getSegmentByIndex(item.curBitsIndex, 2)))
                print('rp_pl_legal_task:' + str(item.getSegmentByIndex(item.curBitsIndex, 2)))
            print('-' * 21 + '-' * 21)
            print('rp_pl_out_time:' + str(item.getSegmentByIndex(item.curBitsIndex, 1)))
            print('rp_pl_stn_state:' + str(item.getSegmentByIndex(item.curBitsIndex, 2)))
            print('rp_pl_track_balise:' + str(item.getSegmentByIndex(item.curBitsIndex, 24)))
            print('rp_pl_track_plan:' + str(item.getSegmentByIndex(item.curBitsIndex, 24)))
            print('rp_pl_in_use:' + str(item.getSegmentByIndex(item.curBitsIndex, 2)))
            print('rp_pl_valid:' + str(item.getSegmentByIndex(item.curBitsIndex, 1)))
            print('rp_pl_output_arr_time:' + str(item.getSegmentByIndex(item.curBitsIndex, 32)))
            print('rp_pl_output_depart_time:' + str(item.getSegmentByIndex(item.curBitsIndex, 32)))
            print('rp_pl_output_skip:' + str(item.getSegmentByIndex(item.curBitsIndex, 2)))
            print('rp_pl_output_task:' + str(item.getSegmentByIndex(item.curBitsIndex, 2)))
        elif nid == 80:
            print('base_ver:' + str(item.getSegmentByIndex(item.curBitsIndex, 32)))
            print('proj_ver:' + str(item.getSegmentByIndex(item.curBitsIndex, 32)))
            print('coast_delay:' + str(item.getSegmentByIndex(item.curBitsIndex, 8)))
            print('tract_delay:' + str(item.getSegmentByIndex(item.curBitsIndex, 8)))
            print('brake_h_delay:' + str(item.getSegmentByIndex(item.curBitsIndex, 8)))
            print('brake_l_delay:' + str(item.getSegmentByIndex(item.curBitsIndex, 8)))
            print('l_door_dis:' + str(item.getSegmentByIndex(item.curBitsIndex, 12)))
            print('ed_error:' + str(item.getSegmentByIndex(item.curBitsIndex, 12)))
            print('train_8:' + str(item.getSegmentByIndex(item.curBitsIndex, 10)))
            print('train_17:' + str(item.getSegmentByIndex(item.curBitsIndex, 10)))
            print('sdu_pulse:' + str(item.getSegmentByIndex(item.curBitsIndex, 8)))
            print('wheel_size:' + str(item.getSegmentByIndex(item.curBitsIndex, 11)))
            print('use_pulse1:' + str(item.getSegmentByIndex(item.curBitsIndex, 1)))
            print('use_pulse2:' + str(item.getSegmentByIndex(item.curBitsIndex, 1)))
            print('sensor_from:' + str(item.getSegmentByIndex(item.curBitsIndex, 2)))
            print('atp_comm_timeout:' + str(item.getSegmentByIndex(item.curBitsIndex, 16)))
            print('tcms_timeout:' + str(item.getSegmentByIndex(item.curBitsIndex, 16)))
            print('recon_time:' + str(item.getSegmentByIndex(item.curBitsIndex, 16)))
            print('ramp_cal:' + str(item.getSegmentByIndex(item.curBitsIndex, 1)))
            print('vrh_coast:' + str(item.getSegmentByIndex(item.curBitsIndex, 1)))
            print('l_stop_win:' + str(item.getSegmentByIndex(item.curBitsIndex, 8)))
        elif nid == 54:
            print('v_ato_cmd:' + str(item.getSegmentByIndex(item.curBitsIndex, 16)))
            print('v_atp_cmd:' + str(item.getSegmentByIndex(item.curBitsIndex, 16)))
            print('ctrl_machine:' + str(item.getSegmentByIndex(item.curBitsIndex, 6)))
            print('adj_ramp:' + str(item.getSegmentByIndex(item.curBitsIndex, 8)))
            print('adj_es_ramp:' + str(item.getSegmentByIndex(item.curBitsIndex, 8)))
            print('v_s_target:' + str(item.getSegmentByIndex(item.curBitsIndex, 16)))
            print('o_s_target:' + str(item.getSegmentByIndex(item.curBitsIndex, 32)))
            print('lvl_raw:' + str(item.getSegmentByIndex(item.curBitsIndex, 8)))
            print('lvl_filter_b:' + str(item.getSegmentByIndex(item.curBitsIndex, 8)))
            print('lvl_filter_p:' + str(item.getSegmentByIndex(item.curBitsIndex, 8)))
            print('lvl_filter_ramp:' + str(item.getSegmentByIndex(item.curBitsIndex, 8)))
            print('lvl_filter_wind:' + str(item.getSegmentByIndex(item.curBitsIndex, 8)))
            print('lvl_filter_gfx:' + str(item.getSegmentByIndex(item.curBitsIndex, 8)))
            print('lvl_filter_out:' + str(item.getSegmentByIndex(item.curBitsIndex, 8)))
            print('q_ato_cutoff:' + str(item.getSegmentByIndex(item.curBitsIndex, 4)))
            print('o_es_pos:' + str(item.getSegmentByIndex(item.curBitsIndex, 32)))
            print('v_es_speed:' + str(item.getSegmentByIndex(item.curBitsIndex, 16)))
            print('o_ma:' + str(item.getSegmentByIndex(item.curBitsIndex, 32)))
        elif nid ==21:
            n_ssp = item.getSegmentByIndex(item.curBitsIndex, 5)
            print('n_ssp:' + str(n_ssp))
            for ssp_cnt in range(n_ssp):
                print('-' * 15 + 'PKT_CONTENT '+ str(ssp_cnt) + '-' * 15)
                print('ssp_pos:' + str(item.getSegmentByIndex(item.curBitsIndex, 32)))
                print('d_ssp:' + str(item.getSegmentByIndex(item.curBitsIndex, 32)))
                print('v_ssp:' + str(item.getSegmentByIndex(item.curBitsIndex, 16)))
            print('-' * 21 + '-' * 21)
            n_tsr = item.getSegmentByIndex(item.curBitsIndex, 5)
            print('n_tsr:' + str(n_tsr))
            for tsr_cnt in range(n_tsr):
                print('-' * 15 + 'PKT_CONTENT '+ str(tsr_cnt) + '-' * 15)
                print('tsr_pos:' + str(item.getSegmentByIndex(item.curBitsIndex, 32)))
                print('l_tsr:' + str(item.getSegmentByIndex(item.curBitsIndex, 32)))
                print('v_tsr:' + str(item.getSegmentByIndex(item.curBitsIndex, 16)))
            n_ramp = item.getSegmentByIndex(item.curBitsIndex, 5)
            print('n_ramp:' + str(n_ramp))
            for ramp_cnt in range(n_ramp):
                print('-' * 15 + 'PKT_CONTENT '+ str(ramp_cnt) + '-' * 15)
                print('ramp_pos:' + str(item.getSegmentByIndex(item.curBitsIndex, 32)))
                print('d_ramp:' + str(item.getSegmentByIndex(item.curBitsIndex, 32)))
                print('ramp:' + str(item.getSegmentByIndex(item.curBitsIndex, 8)))
            n_stn = item.getSegmentByIndex(item.curBitsIndex, 5)
            print('n_stn:' + str(n_stn))
            for stn_cnt in range(n_stn):
                print('-' * 15 + 'PKT_CONTENT '+ str(stn_cnt) + '-' * 15)
                print('stn_pos:' + str(item.getSegmentByIndex(item.curBitsIndex, 32)))
                print('d_stn:' + str(item.getSegmentByIndex(item.curBitsIndex, 32)))
        else:
            print('content:' + hex(item.getSegmentByIndex(item.curBitsIndex, l_pkt - 21)))

    print('Bytesoffset:%d bitoffset:%d' % (item.curBytesIndex, item.curBitsIndex))
    print('\n')

# 结尾打印
print('next index B: ' + hex(item.getSegmentByIndex((item.curBytesIndex+1)*8, 8)))
print('end:' + hex(item.getSegmentByIndex((len(item.getStreamInBytes())-1)*8, 8)))

print('allB: ' + str(len(item.getStreamInBytes())))