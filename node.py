import random
import logging
import threading
import time
import socket
import struct

class Node:
	'A node in the network'
		
	def __init__(self, ip):
		self.ip = ip
		self.key = None
		self.port = 12333
		self.ip_next = None
		self.key_next = None
		self.ip_prev = None
		self.key_prev = None

	def create(self):
		logging.info('Creating network...')
		self.key = random.getrandbits(32)
		self.ip_next = self.ip
		self.key_next = self.key
		self.ip_prev = self.ip
		self.key_prev = self.key
		logging.debug('Network created. IP = (%s:%s) | Key = %s' % (self.ip, self.port, self.key))

	def join(self, contact_ip):
		logging.info('Joining network...')
		# Create a UDP socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		server_address = (contact_ip, 12233)

		values = ('abcd',)
		s = struct.Struct('s')
		packed_data = s.pack(*values)

		try:
			# Send data
			logging.debug('Sending "%s"' % packed_data)
			sent = sock.sendto(packed_data, server_address)

		finally:
			logging.info('Closing socket...')
			sock.close()
			logging.info('Socket closed...')

		### TODO

	def leave(self):
		logging.info('Leaving network...')
	
	def lookup(self):
		logging.info('Launch look up...')

	def update(self):
		logging.info('Executing update...')


	def listener(self):
		logging.info('Creating server...')
		# Create a TCP/IP socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		# Bind the socket to the port
		server_address = (self.ip, 12233)
		logging.debug('Starting up on %s port %s ...' % server_address)
		
		sock.bind(server_address)
		logging.info('Server binded')
		
		while True:
			logging.info('Waiting to receive message')
			data, address = sock.recvfrom(4096)

			logging.debug('Received %s bytes from %s' % (len(data), address))

			s = struct.Struct('4s')
			unpacked_data = s.unpack(data)
			logging.info(unpacked_data)

			if data:
				sent = sock.sendto(data, address)
				logging.debug('Sent %s bytes back to %s' % (sent, address))
		logging.info('Exiting')


logging.basicConfig(level  = logging.DEBUG,
                    format = '[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

node = Node('localhost')
node.create()
node.leave()
node.lookup()
node.update()
t = threading.Thread(name = 'server', target = node.listener)
t.start()