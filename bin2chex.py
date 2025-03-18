#!/usr/bin/python3 

import sys 

symbols_per_line = 24

shellcode_sources = ""
shellcode_sources += "unsigned char shellcode[] = \n"
with open(sys.argv[1], "rb") as fh:
    cnt = 0
    while True:
        if cnt == 0:
            shellcode_sources += '"'

        data = fh.read(1)
        if data == b'':
            break

        shellcode_sources += "\\x" + data.hex()

        cnt += 1
        if cnt == symbols_per_line:
            shellcode_sources += '"\n'
            cnt = 0

shellcode_sources += ('";\n' if cnt != 0 else ";\n")

print(shellcode_sources)
