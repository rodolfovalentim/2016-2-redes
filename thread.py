import logging
import threading
import time
import socket
import struct

logging.basicConfig(level  = logging.DEBUG,
                    format = '[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

def worker():
    logging.debug('Starting')
    while True:
    	var_input = input("Entre uma letra!")
    	if (var_input == 9):
    		break
    	print var_input
    logging.debug('Exiting')

def server():
	logging.debug('Creating server...')
    # Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	# Bind the socket to the port
	server_address = ('localhost', 12233)
	logging.debug('Starting up on %s port %s ...' % server_address)
	
	sock.bind(server_address)
	logging.debug('Server binded')
	
	while True:
	    logging.debug('Waiting to receive message')
	    data, address = sock.recvfrom(4096)
	    
	    logging.debug('Received %s bytes from %s' % (len(data), address))

	    s = struct.Struct('4s')
	    unpacked_data = s.unpack(data)
	    logging.debug(unpacked_data)
	    
	    if data:
	        sent = sock.sendto(data, address)
	        logging.debug('Sent %s bytes back to %s' % (sent, address))
	logging.debug('Exiting')

t = threading.Thread(name = 'input', target = server)
w = threading.Thread(name = 'worker', target = worker)

w.start()
t.start()