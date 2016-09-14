import random
import logging
import threading
import time
import socket
import struct

class Node:
	'A node in the network'
		
	def __init__(self, ip):
		# self.ip = socket.gethostbyname(socket.gethostname())
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

		server_address = ('localhost', 12233)
		
		# building package
		probable_key = random.getrandbits(32)
		data = (1, probable_key)
		s = struct.Struct('! B I')
		packed_data = s.pack(*data)

		try:
			# Send data
			logging.debug('Sending "%s"' % packed_data)
			sent = sock.sendto(packed_data, server_address)

			# Receive response
			logging.info('Waiting answer of network about next...')
			data, server = sock.recvfrom(4096)
			
			# unpacking data 
			s = struct.Struct('! B B I B B B B I B B B B')
			unpacked_data = s.unpack(data)
			print 'Unpacked Values:', unpacked_data
			
			if(unpacked_data[1] == 1):
				print 'DATA IGUAL A 1'
			elif (unpacked_data[1] == 0):
				print 'DATA IGUAL A 0'

		finally:
			logging.info('Closing socket...')
			sock.close()
			logging.info('Socket closed...')

		### TODO

	def leave(self):
		logging.info('Leaving network...')
	
	def lookup(self):
		logging.info('Launch look up...')
		return

 	def update(self):
		logging.info('Executing update...')


	def listener(self):
		logging.info('Creating server...')
		# Create a TCP/IP socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		# Bind the socket to the port
		server_address = (self.ip, self.port)
		logging.debug('Starting up on %s port %s ...' % server_address)
		
		# sock.bind((socket.gethostname(), 80))
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

# Configuration of log messages
logging.basicConfig(level  = logging.DEBUG,
                    format = '[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )
