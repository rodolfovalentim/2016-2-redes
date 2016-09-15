import struct
import binascii
import random

id = random.getrandbits(32)
values = (1, 2, 3, 4, 5, 6)
s = struct.Struct('! B B B B B B')
packed_data = s.pack(*values)

print 'Original values:', values
print 'Format string  :', s.format
print 'Uses           :', s.size, 'bytes'
print 'Packed Value   :', binascii.hexlify(packed_data)

s = struct.Struct('! 6B')
unpacked_data = s.unpack(packed_data)
print 'Unpacked Values:', unpacked_data[2:]

print ''.join(unpacked_data)