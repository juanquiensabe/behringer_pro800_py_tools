#!/usr/bin/python3 

import  sys
from pro800_tools import *


if len(sys.argv) != 2: sys.exit('Invalid arguments (needs: input_file.syx')

in_file_name = sys.argv[1]
file_len = len(in_file_name) - 3
csv_file_name = in_file_name[0:file_len] + 'csv'

conv_file_name = in_file_name[0:file_len-1] + '_conv.syx'
chec_file_name = in_file_name[0:file_len-1] + '_ccheck.csv'

sysex2csv_conv(in_file_name, csv_file_name)
csv2sysex_conv(csv_file_name, conv_file_name)


#check
sysex2csv_conv(conv_file_name, chec_file_name)