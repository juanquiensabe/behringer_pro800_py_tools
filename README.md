# behringer_pro800_py_tools

This is a really simple python module that converts SYSEX files into CSV and vice versa. It was done in my
spare time and I did not pay to much attention to format nor documentation

## Usage
There is expample command on the source level. The command is used as follow:

***python3 sysex_conv.py PRO800_Factory_Presets_Dump.syx***

### The 2 main functions are:

***sysex2csv_conv(in_file_name, csv_file_name)***

***csv2sysex_conv(csv_file_name, conv_file_name)***


## Preset Version Note
The current sysex2csv_conv function, reads the preset version and updates all presets to version 111.
It also applies the offset correction to the LFO Amount that was introduced inversion 1.3.7, for older presets.

It should do the same as 1.4.1 does. 
