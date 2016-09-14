import socket
import sys
import struct
import binascii
import random

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 12233)

values = (1, random.getrandbits(32))
s = struct.Struct('B I')
packed_data = s.pack(*values)

try:
    # Send data
    print >>sys.stderr, 'sending "%s"' % packed_data
    sent = sock.sendto(packed_data, server_address)

    # Receive response
    print >>sys.stderr, 'waiting to receive'
    data, server = sock.recvfrom(4096)
    print >>sys.stderr, 'received "%s"' % packed_data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()