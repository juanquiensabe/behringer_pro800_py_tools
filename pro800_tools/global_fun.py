#!/usr/bin/python3 

import  sys, struct
SEPARATOR = ','


def write_8bit_to_str(data, len, idx):
    line_=''
    for i in range(len):
        line_ += str(data[idx])     
        line_ += SEPARATOR
        idx += 1

    return [idx, line_]

def write_16bit_to_str(data, len, idx):
    line_=''
    for i in range(len):
        line_ += str(data[idx] | (data[idx + 1] << 8))     
        line_ += SEPARATOR
        idx += 2

    return [idx, line_]

def write_32bit_to_str(data, len,  idx):
    line_=''
    for i in range(len):
        line_ += str(data[idx] | (data[idx + 1] << 8) | (data[idx + 2] << 16) | (data[idx + 3] << 24))      
        line_ += SEPARATOR
        idx += 4

    return [idx, line_]
    

def write_16bit_to_str_LFOAMT(data, len, idx):
    line_=''
    for i in range(len):
        LFOAMT = (data[idx] | (data[idx + 1] << 8))
        if LFOAMT <= 2048:
            LFOAMT = 0
        else:
            LFOAMT = LFOAMT - 2048  #values taken from DEADZONE on gligli SRC

        line_ += str(LFOAMT)     
        line_ += SEPARATOR
        idx += 2

    return [idx, line_]



def read_write_8(csv_row, len, idx):
    vec_l=[]
    for i in range(len):
        vec_l.append(struct.pack('<B',int(csv_row[idx])))
        idx += 1

    return [idx, vec_l]

def read_write_16(csv_row, len, idx):
    vec_l=[]

    for i in range(len):
        data16 = struct.pack('<H',int(csv_row[idx]))
        vec_l.append(struct.pack('<B',data16[0]))
        vec_l.append(struct.pack('<B',data16[1]))
        idx += 1

    return [idx, vec_l]

def read_write_32(csv_row, len, idx):
    vec_l=[]

    for i in range(len):
        data32 = struct.pack('<I',int(csv_row[idx]))
        vec_l.append(struct.pack('<B',data32[0]))
        vec_l.append(struct.pack('<B',data32[1]))
        vec_l.append(struct.pack('<B',data32[2]))
        vec_l.append(struct.pack('<B',data32[3]))
        idx += 1

    return [idx, vec_l]