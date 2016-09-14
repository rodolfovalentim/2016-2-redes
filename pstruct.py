import struct
import binascii
import random

id = random.getrandbits(32)
values = (1, random.getrandbits(32))
s = struct.Struct('! B I')
packed_data = s.pack(*values)

print 'Original values:', values
print 'Format string  :', s.format
print 'Uses           :', s.size, 'bytes'
print 'Packed Value   :', binascii.hexlify(packed_data)

s = struct.Struct('! B I')
unpacked_data = s.unpack(packed_data)
print 'Unpacked Values:', unpacked_data