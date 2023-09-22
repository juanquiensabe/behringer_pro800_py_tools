#!/usr/bin/python3 

import  sys, struct

header = [0xf0, 0x00, 0x20, 0x32, 0x00, 0x01, 0x24, 0x00, 0x78]
MAX_SYS_LEN = 256

def decode_sysex_msg(file):

    inpos = 12
    outpos = 0
    buffer = []
    len = 0

    #check header
    data = []
    for i in range(9):
        data.append(ord(file.read(1)))

    if header != data:
        while ord(file.read(1)) != 0xf7 :
            data = []
        return [-1 , 0, buffer]

    # address first byte is data 9
    data = []
    data.append(ord(file.read(1)))
    data.append(ord(file.read(1)))

    add = data[0] + (data[1] << 8)

    while inpos < MAX_SYS_LEN:
        chunkHdr = ord(file.read(1))
        if chunkHdr==0xf7:
            break

        for x in range(0,7):

            if x > MAX_SYS_LEN:
                break

            data = ord(file.read(1))
            if data==0xf7:
                break

            buffer.append(data  | (((chunkHdr & (1 << x)) > 0) << 7))
            outpos += 1

        if data==0xf7:
            break

    return [outpos, add, buffer] 


def encode_sysex_msg(vec):
    vec_enc = []

    #first 11 bytes are unecoded
    for i in range(11):
        vec_enc += vec[i]

    inpos = 11
    cnt = 0
    while 1:
        chunkHdr = 0
        vec_enc7 = []
        x_l=0
        for x in range(7):
            x_l = x
            if (vec[inpos] == b'\xf7') & (inpos >= 151):
                break

            if ord(vec[inpos]) & ord(b'\x80'):
                chunkHdr = chunkHdr | (1<<x)

            vec_enc7.append(ord(vec[inpos]) & ord(b'\x7f'))

            inpos += 1
  

        vec_enc += struct.pack('B',chunkHdr)

        for i in range(len(vec_enc7)):
            vec_enc += struct.pack('B',vec_enc7[i]) 


        if vec[inpos] == b'\xf7':
            vec_enc += (b'\xf7')
            break

    return [vec_enc, inpos]