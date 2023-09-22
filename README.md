# behringer_pro800_py_tools

This is a really symply python module that convertes SYSEX files into CSV and viceversa. It was done in my
spare time and I did not pay to much attention to format nor documentation

## Usage
There is expample command on the source level. But the 2 main functions are:

***from pro800_tools import***

***sysex2csv_conv(in_file_name, csv_file_name)***

***csv2sysex_conv(csv_file_name, conv_file_name)***


## Preset Version note
The current sysex2csv_conv function, reads the preset version and udpates all presets to version 111.
It also applies the offset correction to the LFO Amount that was introduced inversion 1.3.7, for older presets.

It should do the same as 1.4.1 does. 
