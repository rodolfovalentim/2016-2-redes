import socket
import sys
import struct
import binascii
import random

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('127.0.0.1', 12233)
print >>sys.stderr, 'starting up on %s port %s' % server_address

values = (130, 1, 1, 1, 1, 1, 1)
s = struct.Struct('! B I I B B B B')
packed_data = s.pack(*values)

print 'sent: ', values
sent = sock.sendto(packed_data, server_address)
print >>sys.stderr, 'sent %s bytes back to %s' % (sent, server_address)
