from pathlib import Path
data = bytearray(Path('dead_test.bin').read_bytes())
checksum = 0
for i in data:
  checksum = checksum ^ i
data[0x1ff9] = checksum
with open("dead_test.bin", "wb") as binfile:
    binfile.write(data)
print("Checksum added.")
