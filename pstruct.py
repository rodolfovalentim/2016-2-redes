import struct
import binascii

values = (17,)
s = struct.Struct('I')
packed_data = s.pack(*values)

print 'Original values:', values
print 'Format string  :', s.format
print 'Uses           :', s.size, 'bytes'
print 'Packed Value   :', binascii.hexlify(packed_data)

s = struct.Struct('I')
unpacked_data = s.unpack(packed_data)
print 'Unpacked Values:', unpacked_data[0]