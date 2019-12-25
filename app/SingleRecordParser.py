from CommonParse import BytesStream
from app.BaseMethod import iner_escape_reverse

streamReverseEsc = iner_escape_reverse('7EC943980030A4B013009A52EFD81A31E686BE910A230902290A1843C4D741901A44F3435F48000AD90C853C0412B6155542CCC000000000000015400000004095B0AA00098C35FFFFFFFF0BF9000000003405B7FFFFFFFFFFFFFFFFFFFFFFF9E7B51CD1E7B51CD0CC17A279A10B94000B944E4346279A1AFA400056C86429E6C107214F21592BF7F40000F3DA8E681C1C1C1C1C1C1C000018F64852CF3DAB5780022A00615554333200000000015400022823555460000000000000000000000000000625D2D49FA0EA01812FA8878210A2009C36ED812D400000012F2BD303CD0D55821A36103BFFFCAC20000000967700006771BFFFFFFFC005A56B100098C35A000061213025F510F73988BEF07F')
if streamReverseEsc == '':
    print("err stream, can not analysis!")
item = BytesStream(streamReverseEsc)
msg_head_width = [8, 8, 10, 2, 1, 32, 32, 32, 32, 16, 3]
str_head_name = ['escap_head', 'nid_msg', 'l_msg', 'nid_modle', 'q_standby', 'n_cycle',
                 't_ato', 't_atoutc', 'm_pos', 'v_speed', 'm_atomode']

print('*'*30 + 'MSG_HEAD '+'*'*30)
for idx, content in enumerate(msg_head_width):
    print(str_head_name[idx] + ':' + str(item.get_segment_by_index(item.curBitsIndex, msg_head_width[idx])))
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

    # 在下一次监测前，判断退出
    if item.curBitsIndex >= len(item.get_stream_in_bytes()) * 8 - 1 - 8 - 8:   # 减去第一个8代表尾巴7F，第二个代表一个字节内
        break

    print('Bytesoffset:%d bitoffset:%d' % (item.curBytesIndex, item.curBitsIndex))
    print('\n')

# 结尾打印
print('next index B: ' + hex(item.get_segment_by_index((item.curBytesIndex + 1) * 8, 8)))
print('end:' + hex(item.get_segment_by_index((len(item.get_stream_in_bytes()) - 1) * 8, 8)))

print('allB: ' + str(len(item.get_stream_in_bytes())))