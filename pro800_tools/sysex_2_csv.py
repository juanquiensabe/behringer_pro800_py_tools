#!/usr/bin/python3 

import  sys

from pro800_tools import *


strings_vector =[
'Number',
'Storage Magic',
'Version',
'OSCA.Frequency',
'OSCA.Volume',
'OSCA.PW',
'OSCB.Frequency',
'OSCB.Volume',
'OSCB.PW',
'OSCB.Fine Frequency',
'VCF.Cutoff',
'VCF.Resonance',
'VCF.Env Amount',
'VCF.Release',
'VCF.Sustain',
'VCF.Decay',
'VCF.Attack',
'VCA.Release',
'VCA.Sustain',
'VCA.Decay',
'VCA.Attack',
'PolyMod.Filter env',
'PolyMod.Osc B',
'LFO.Frequency',
'LFO.Amount',
'General.Glide',
'VCA.Velocity',
'VCF.Velocity',
'OSCA.Saw',
'OSCA.Tri',
'OSCA.Square',
'OSCB.Saw',
'OSCB.Tri',
'OSCB.Square',
'OSCB.Sync',
'PolyMod.Freq A',
'PolyMod.Filter cutoff',
'LFO.Shape',
'LFO.Speed',
'LFO.Targets',
'VCF.Keyboard mod',
'VCF.Env Lin_Exp',
'VCF.Env Fast_Slow',
'VCA.Env Lin_Exp',
'General.Unison',
'General.Pitchbend target',
'General.Modwheel range',
'OSCA.Freq pot mode',
'OSCB.Freq pot mode',
'LFO.Modulation delay',
'LFO.Vibrato frequency',
'LFO.Vibrato amount',
'General.Unison detune',
'General.Modwheel target',
'General.Vibrato target',
'Chord.Voice 1',
'Chord.Voice 2',
'Chord.Voice 3',
'Chord.Voice 4',
'Chord.Voice 5',
'Chord.Voice 6',
'Chord.Voice 7',
'Chord.Voice 8',
'Tuning.C',
'Tuning.C#',
'Tuning.D',
'Tuning.D#',
'Tuning.E',
'Tuning.F',
'Tuning.F#',
'Tuning.G',
'Tuning.G#',
'Tuning.A',
'Tuning.A#',
'Tuning.B',
'General.Noise',
'VCA.Aftertouch',
'VCF.Aftertouch',
'VCA.Env Fast_Slow',
'Arp_Seq.Arp mode',
'General.Name',
'LFO.Aftertouch amount',
'General.Voice Spread',
'General.Keyboard tracking ref',
'General.Glide mode',
'General.Pitchbend range']


PRE_NAME_LEN = 16  #including zero byte
PRE_NUM_PARA = 81
SEPARATOR = ','
NEW_LINE = 0x0a

storage_magit =[0xA5, 0x16, 0x61, 0x00]
header = [0xf0, 0x00, 0x20, 0x32, 0x00, 0x01, 0x24, 0x00, 0x78]
pre_add = [0x10, 0x03]
preset_no =100
new_ver = 111




def parse_data_to_csvline(data, address, len, output_file):
    idx = 0
    line_ = ''

    line_string = ''
    line_string += str(int(address) )     #Number
    line_string += SEPARATOR

    # storage magic
    [idx,line_] = write_32bit_to_str(data, 1, idx)
    line_string += line_

    #version
    version = data[idx]
    line_string += str(new_ver)
    line_string += SEPARATOR
    idx += 1

    
    #16 bit data 0 to 20 values
    [idx,line_] = write_16bit_to_str(data, 21, idx)
    line_string += line_
    
    # LFO Amount is 21
    if version < 111:
        [idx,line_] = write_16bit_to_str_LFOAMT(data, 1, idx)
    else:
        [idx,line_] = write_16bit_to_str(data, 1, idx)

    line_string += line_

    #16 bit data 22 to 24 values
    [idx,line_] = write_16bit_to_str(data, 3, idx)
    line_string += line_

    # 8 bit data 25 to 45
    [idx,line_] = write_8bit_to_str(data, 21, idx)
    line_string += line_
    

    #16 bit data 46 to 49 values
    [idx,line_] = write_16bit_to_str(data, 4, idx)
    line_string += line_

    #for verion 9 there is no BMP!!!
    

    # 8 bit data 51 to 60
    [idx,line_] = write_8bit_to_str(data, 10, idx)
    line_string += line_
    

    # 32 bit data 61 to 72 values
    [idx,line_] = write_32bit_to_str(data, 12, idx)
    line_string += line_
    

    #16 bit data 73 to 75 values
    [idx,line_] = write_16bit_to_str(data, 3, idx)
    line_string += line_
    

    # 8 bit data 76 to 77
    [idx,line_] = write_8bit_to_str(data, 2, idx)
    line_string += line_
    

    # name string data 78 to 93
    idx_cpy = idx
    for i in range(16):
        if version < 109:
            line_string += chr(0)
        else:
            if data[idx] == 0x00:
                break
            line_string += chr(data[idx])
    
        idx += 1

    line_string += SEPARATOR
    
    if version > 109:
        idx = (16+idx_cpy)

    #LFO AT amount
    if version < 110:
        data_t = [0, 0]
        [idx_t,line_] = write_16bit_to_str(data_t, 1, 0)
    else:
        [idx,line_] = write_16bit_to_str(data, 1, idx)
    
    line_string += line_

    #voice spread, keyboar tracking and glide mode
    if version < 111:
        data_t = [0,0]
        [idx_t,line_] = write_8bit_to_str(data_t, 1, 0)
        line_string += line_
        data_t = [3,0]
        [idx_t,line_] = write_8bit_to_str(data_t, 1, 0)
        line_string += line_
        data_t = [0,0]
        [idx_t,line_] = write_8bit_to_str(data_t, 1, 0)
        line_string += line_
    else:
        [idx,line_] = write_8bit_to_str(data, 3, idx)
        line_string += line_

    #pitch bend range
    if version < 111:
        key_ref = 12 << 11
        data_t = [key_ref & 0xff, key_ref >> 8]
        [idx_t,line_] = write_16bit_to_str(data_t, 1, 0)
    else:
        [idx,line_] = write_16bit_to_str(data, 1, idx)


    line_string += line_

    line_string += '\n'
    output_file.write(line_string)



def sysex2csv_conv(input_sys_file, out_csv_file):

    in_file_name = input_sys_file
    out_file_name =out_csv_file
    try:
        out_file = open(out_file_name, 'w')
    except:
        sys.exit('Cannot write output file')

    try:
        input_sys_file = open(in_file_name,'rb')
    except:
        sys.exit('Cannot find sysex file' + in_file_name)


    #write header
    headr_line = ''
    for i in range(len(strings_vector)):    
        headr_line += strings_vector[i]

        if i < (len(strings_vector)-1):
            headr_line += SEPARATOR

    headr_line += '\n'
    out_file.write(headr_line)


    length = 0
    address = 0
    buffer = []

    for i in range(preset_no): #preset_no
        param_cnt = 0
        [length, address, buffer] = decode_sysex_msg(input_sys_file)
        parse_data_to_csvline(buffer, address, length, out_file)


    out_file.close()