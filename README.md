# behringer_pro800_py_tools

This is a really symples python module to converte SYSEX files into CSV and viceversa. It was done in my
spare time and did not pay to much attention to format nor documentation

## Usage
There is expample command on the source level.

## Preset Verion note
The current sysex_2_csv_convert function, reads the preset version and udpates all presets prior version 111.
It also apples the offset correction to the LFO Amount that was introduces for all presets after version 1.3.7.

It should do the same as 1.4.1 does. 
