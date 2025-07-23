from pathlib import Path
import sys
import crcmod

fpath = Path(sys.argv[1])
data = bytearray(fpath.read_bytes())

# for i in data:
#  print(hex(0x100+i)[3:], end='')
# print()

crc16 = crcmod.mkCrcFun(0x11021, rev=False, initCrc=0x0000, xorOut=0x0000)
print(f"{hex(crc16(data) + 0x10000)[3:]} {fpath.name}")
