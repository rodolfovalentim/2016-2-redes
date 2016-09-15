import random
import logging
import threading
import time
import socket
import struct

class Node:
	'A node in the network'
	cod_request_join = 0
	cod_request_leave = 1
	cod_request_lookup = 2
	cod_request_update = 3

	cod_answer_join = 128
	cod_answer_leave = 129
	cod_answer_lookup = 130
	cod_answer_update = 131

	shouldIBeAlive = False
	expecting_lookup = False

	def __init__(self, my_ip):
		self.ip = my_ip
		self.key = None
		self.port = 12233
		self.ip_next = None
		self.key_next = None
		self.ip_prev = None
		self.key_prev = None

	def __str__(self):
		return str(self.ip) + ', ' + str(self.key) + ', ' + str(self.port) + ', ' + str(self.ip_next) + ', ' + str(self.key_next)

	def setAlive(self):
		self.shouldIBeAlive = True

	def setDeath(self):
		self.shouldIBeAlive = False

	def getLife(self):
		return self.shouldIBeAlive

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
		
		server_address = (self.ip, self.port)
		contact_address = (contact_ip, self.port)
		
		logging.info('Creating socket...')
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind(server_address)

		# building package
		probable_key = random.getrandbits(32)
		data = (self.cod_request_join, probable_key)

		s = struct.Struct('! B I')
		packed_data = s.pack(*data)

		try:
			# Send data
			logging.debug('Sending "%s"' % packed_data)
			sent = sock.sendto(packed_data, contact_address)

			# Receive response
			logging.info('Waiting answer of network about next...')
			data, server = sock.recvfrom(4096)
			
			# unpacking data 
			s = struct.Struct('! B B I B B B B I B B B B')
			unpacked_data = s.unpack(data)
			
			# TODO launch error se nao for no padrao
			logging.debug('Unpacked Values: %s', (unpacked_data))
			
			if (unpacked_data[1] == 1):
				logging.info('Information about next node obtained. Updating previous node...')
				self.update()
			elif (unpacked_data[1] == 0):
				logging.warning('Key already exist. Trying again...')
				logging.info('Trying again with new key...')
				sock.close()
				node.join(contact_ip)
				return
			else :
				logging.error('Unknown error. Verify connection or package string pattern!')
	
			self.key = probable_key
			self.key_next = unpacked_data[2]
			self.ip_next = str(unpacked_data[3]) + '.' + str(unpacked_data[4]) + '.' + str(unpacked_data[5]) + '.' + str(unpacked_data[6])
			self.key_prev = unpacked_data[7]
			self.ip_prev = str(unpacked_data[8]) + '.' + str(unpacked_data[9]) + '.' + str(unpacked_data[10]) + '.' + str(unpacked_data[11])

		finally:
			logging.info('Closing socket...')
			sock.close()
			logging.info('Socket closed...')

	def leave(self):
		logging.info('Leaving network...')
		
		server_address = (self.ip, self.port)
		prev_address = (self.ip_prev, self.port)
		next_address = (self.ip_next, self.port)
		
		logging.info('Creating socket...')
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind(server_address)

		# building package
		ip_prev_form = self.ip_prev.split('.')
		ip_next_form = self.ip_next.split('.')

		if(len(ip_prev_form) != 4 or len(ip_next_form) != 4):
			Logging.error('Wrong IP pattern')
			return

		values = (self.cod_request_leave, self.key, self.key_next, 
				int(ip_next_form[0]), int(ip_next_form[1]), 
				int(ip_next_form[2]), int(ip_next_form[3]),
				self.key_prev, 
				int(ip_prev_form[0]), int(ip_prev_form[1]), 
				int(ip_prev_form[2]), int(ip_prev_form[3]),) 

		s = struct.Struct('! B I I B B B B I B B B B')
		packed_data = s.pack(*values)

		#TODO - TRATAMENTO DE RESPOSTA DO LEAVE

		try:
			# Send data
			logging.debug('Sending "%s"' % packed_data)
		 	sent = sock.sendto(packed_data, prev_address)
		 	sent = sock.sendto(packed_data, next_address)
		finally:
			logging.info('Closing socket...')
		 	sock.close()
		 	logging.info('Socket closed...')

		
	def lookup(self, contact_ip, key):
		logging.info('Launch look up...')
		server_address = (self.ip, self.port)
		contact_address = (contact_ip, self.port)
		
		logging.info('Creating socket...')
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind(server_address)

		# building package
		ip_fmt = self.ip.split('.')
		
		if(len(ip_fmt) != 4):
			logging.error('Wrong IP pattern')
			return

		data = (self.cod_request_lookup, self.key, int(ip_fmt[0]), int(ip_fmt[1]), 
				int(ip_fmt[2]), int(ip_fmt[3]), key)

		s = struct.Struct('! B I B B B B I')
		packed_data = s.pack(*data)

		try:
			# Send data
			logging.debug('Sending "%s"' % packed_data)
			sent = sock.sendto(packed_data, contact_address)
			self.expecting_lookup = True

		finally:
			logging.info('Closing socket...')
			sock.close()
			logging.info('Socket closed...')

	def process_lookup_request(self):
		

		
 	def update(self):
		logging.info('Executing update...')

	def read_pkt(self, packed_pkt):
		pattern = '!' + str(len(packed_pkt)) + 'B'
		s = struct.Struct(pattern)
		cod_message = s.unpack(packed_pkt)[0]
		
		if cod_message == self.cod_request_join:
			self.process_join_request()
		elif cod_message == self.cod_request_leave:
			self.process_leave_request()
		elif cod_message == self.cod_request_lookup:
			self.process_lookup_request()
		elif cod_message == self.cod_request_update:
			self.process_update_request()
		elif cod_message == self.cod_answer_join:
			logging.warning('Join answer not expected. Ignoring...')	
		elif cod_message == self.cod_answer_leave:
			logging.warning('Leave answer not expected. Ignoring...')
		elif cod_message == self.cod_answer_lookup:
			self.process_my_lookup()
		elif cod_message == self.cod_answer_update:
			self.process_my_update()
		else:
			logging.error('Unknown code message')


	def listen(self):
		logging.info('Creating server...')
		server_address = (self.ip, self.port)

		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind(server_address)
		sock.setblocking(0)		
		logging.debug('Starting up on %s port %s ...' % server_address)
		
		data = None
		address = None

		logging.info('Waiting to receive message')
		while self.getLife():
			try:
				data, address = sock.recvfrom(4096)
				logging.debug('Received %s bytes from %s' % (len(data), address))
				self.read_pkt(data)
			except:
				pass	

		sock.close()
		logging.info('Closing listener')

	def process_join_request(self):
		print('passou')

	def process_leave_request(self):
		print('passou')


	def process_update_request(self):
		print('passou')

	def process_my_lookup(self):
		print('passou')

	def process_my_update(self):
		print('passou')


# Configuration of log messages
logging.basicConfig(level  = logging.DEBUG,
                    format = '[ %(levelname)-6s] (%(threadName)-8s) %(message)s',
                    )