import random
import logging
import threading
import time
import socket
import struct

class Node:
	'A node in the network'
	cod_request_join = 0
	def __init__(self, ip):
		# self.ip = socket.gethostbyname(socket.gethostname())
		self.ip = ip
		self.key = None
		self.port = 12333
		self.ip_next = None
		self.key_next = None

	def create(self):
		logging.info('Creating network...')
		self.key = random.getrandbits(32)
		self.ip_next = self.ip
		self.key_next = self.key
		logging.debug('Network created. IP = (%s:%s) | Key = %s' % (self.ip, self.port, self.key))

	def join(self, contact_ip):
		logging.info('Joining network...')
		# Create a UDP socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		server_address = ('localhost', 12233)
		# building package
		probable_key = random.getrandbits(32)
		data = (cod_request_join, probable_key)

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
			# TODO launch error se não for no padrão
			print 'Unpacked Values:', unpacked_data
			
			if (unpacked_data[1] == 1):
				logging.info('Information about next node obtained. Updating previous node...')
				self.update()
			elif (unpacked_data[1] == 0):
				logging.warning('Key already exist. Trying again...')
				logging.info('Trying again with new key...')
				sock.close()
				node.join(contact_ip)
			else :
				logging.error('Unknown error. Verify connection!')

			self.key_next = unpacked_data[2]

			self.ip_next = str(unpacked_data[3]) + '.' + str(unpacked_data[4]) + '.' 
					     + str(unpacked_data[5]) + '.' + str(unpacked_data[6])

			ip_prev = str(unpacked_data[8]) + '.' + str(unpacked_data[9]) + '.' 
					+ str(unpacked_data[10]) + '.' + str(unpacked_data[11])


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
		server_address = ('localhost', 12233)
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
