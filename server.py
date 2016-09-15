import socket
import sys
import struct
import binascii
import random

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('192.168.1.100', 12233)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

while True:
    print >>sys.stderr, '\nwaiting to receive message'
    data, address = sock.recvfrom(4096)
    
    print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)

    s = struct.Struct('! B I')
    unpacked_data = s.unpack(data)
    print >>sys.stderr, unpacked_data
    
    if data:
		values = (1, 1, random.getrandbits(32), 120, 1, 1, 2, random.getrandbits(32), 120, 1, 1, 3)
		s = struct.Struct('! B B I B B B B I B B B B')
		packed_data = s.pack(*values)

		print 'sent: ', values
		sent = sock.sendto(packed_data, address)
		print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)