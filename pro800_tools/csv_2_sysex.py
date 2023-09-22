#!/usr/bin/python3 

import csv, sys, struct
from pro800_tools import *

storage_magit =[0xA5, 0x16, 0x61, 0x00]
header = [0xf0, 0x00, 0x20, 0x32, 0x00, 0x01, 0x24, 0x00, 0x78]
tail = [0xF0, 0x00, 0x20, 0x32, 0x00, 0x01, 0x24, 0x01, 0x7D, 0xF7]

first_cmds = [0xF0, 0x00, 0x20, 0x32, 0x00, 0x01, 0x24, 0x00, 0x00, 0x01, 0xF7, 0xF0, 0x00, 0x20, 0x32, 0x00, 0x01, 0x24, 0x01, 0x42, 0x41, 0x64, 0x61, 0x6D, 0x4E, 0xF7]




def extract_data_from_line(csv_row):
    vec = []
    idx = 0

    #header
    for i in range(len(header)):
        vec.append(struct.pack('B',header[i]))

    #number
    [idx, vec_l]=read_write_16(csv_row, 1, idx)
    vec += vec_l

    #magic 32 bits
    [idx, vec_l]=read_write_32(csv_row, 1, idx)
    vec += vec_l

    #version
    [idx, vec_l]=read_write_8(csv_row, 1, idx)
    vec += vec_l


    #25 time 16bit
    [idx, vec_l]=read_write_16(csv_row, 25, idx)
    vec += vec_l


    #21 time 8bit
    [idx, vec_l]=read_write_8(csv_row, 21, idx)
    vec += vec_l

 
    #4 time 16bit
    [idx, vec_l]=read_write_16(csv_row, 4, idx)
    vec += vec_l


    #10 time 8bit
    [idx, vec_l]=read_write_8(csv_row, 10, idx)
    vec += vec_l


    #12 time 32bit
    [idx, vec_l]=read_write_32(csv_row, 12, idx)
    vec += vec_l


    #3 time 16bit
    [idx, vec_l]=read_write_16(csv_row, 3, idx)
    vec += vec_l

    #2 time 8bit
    [idx, vec_l]=read_write_8(csv_row, 2, idx)
    vec += vec_l


    #string name
    name = str(csv_row[idx])

    for i in range(len(name)):
        vec.append(name[i])

    for i in range(16-len(name)):
        vec.append(struct.pack('<B',0))

    idx += 1

    #1 time 32bit  After touch
    [idx, vec_l]=read_write_16(csv_row, 1, idx)
    vec += vec_l

    #3 time 8bit;  Voice spread, keyboard tracking, glide mode
    [idx, vec_l]=read_write_8(csv_row, 3, idx)
    vec += vec_l

    #1 time 16bit, Pitch bend range
    [idx, vec_l]=read_write_16(csv_row, 1, idx)
    vec += vec_l

    #end sysex message
    vec.append(struct.pack('<B',0xf7))


    return vec




def csv2sysex_conv(input_csv_file, out_sysex_file):

    in_file_name = input_csv_file
    out_file_name = out_sysex_file

    try:
        out_file = open(out_file_name, 'wb')
    except:
        sys.exit('Cannot write output file')



    try:
        input_csv_file = open(in_file_name,'r')
    except:
        sys.exit('Cannot find csv file' + in_file_name)


    first = 1
    cnt = 0

    with input_csv_file as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if first == 1:      #ignore header
                first = 0
                continue 

            
            vec_l = []
            vec_en = []

            vec_l = extract_data_from_line(row)

            [vec_en, en_l] = encode_sysex_msg(vec_l)

            for i in range(len(vec_en)):
                out_file.write(struct.pack('B',vec_en[i]))


    out_file.close()


