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
	expected_pkt = [False, False, False, False, False, False, False, False]

	def __init__(self, my_ip):
		self.ip = my_ip
		self.key = random.getrandbits(32)
		self.port = 12233
		self.ip_next = None
		self.key_next = None
		self.ip_prev = None
		self.key_prev = None

	def __str__(self):
		return str(self.ip) + ', ' + str(self.key) + ', ' + str(self.port) + ', ' + str(self.ip_next) + ', ' + str(self.key_next)

	def setShouldIBeAlive(self, value):
		self.shouldIBeAlive = value

	def getShouldIBeAlive(self):
		return self.shouldIBeAlive

	def create(self):
		logging.info('Creating network...')
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


	def lookup(self, key_sought, ip_contact, port_contact):
		logging.info('Launch look up...')
		server_address = (self.ip, self.port)
		contact_address = (ip_contact, port_contact)

		logging.info('Creating socket...')
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind(server_address)

		# building package
		ip_fmt = self.ip.split('.')

		if(len(ip_fmt) != 4):
			logging.error('Wrong IP pattern')
			return

		data = (self.cod_request_lookup, self.key, int(ip_fmt[0]), int(ip_fmt[1]),
				int(ip_fmt[2]), int(ip_fmt[3]), key_sought)

		s = struct.Struct('! B I B B B B I')
		packed_data = s.pack(*data)

		try:
			# Send data
			logging.debug('Sending "%s" to %s' % (packed_data, contact_address))
			sent = sock.sendto(packed_data, contact_address)

		finally:
			logging.info('Closing socket...')
			sock.close()
			logging.info('Socket closed...')

 	def update(self):
		logging.info('Executing update...')

	def process_lookup_request(self, pkt):
		packed_data = pkt
		s = struct.Struct('! B I B B B B I')
		unpacked_data = s.unpack(*packed_data)
		key_sought = unpacked_data[6]

		data = None
		dest_ip = None
		if ((key_sought >= self.key and (key_sought < self.key_next or self.key_next < self.key)) or (self.key_next < self.key and key_sought<self.key_next)):
			ip_fmt = self.ip_next.split('.')
			data = (self.cod_answer_lookup, key_sought, self.key_next, int(ip_fmt[0]), int(ip_fmt[1]), int(ip_fmt[2]), int(ip_fmt[3]))
			s = struct.Struct('! B I I B B B B')
			dest_ip = str(unpacked_data[2]) + '.' + str(unpacked_data[3]) + '.' + str(unpacked_data[4]) + '.' + str(unpacked_data[5])
		else:
			data = unpacked_data
			dest_ip = self.ip_next
			s = struct.Struct('! B I B B B B I')

		packed_data = s.pack(*data)

		server_address = (self.ip, self.port)
		logging.info('Creating socket...')
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind(server_address)

		try:
			# Send data
			contact_address = (dest_ip, self.port)
			logging.debug('Sending "%s" to %s' % (data, contact_address))
			sent = sock.sendto(packed_data, dest_add)
			self.expecting_lookup = True

		finally:
			logging.info('Closing socket...')
			sock.close()
			logging.info('Socket closed...')

	def process_my_lookup(self, pkt):
		s = struct.Struct('! B I I B B B B')
		unpacked_data = s.unpack(pkt)

		key_sought = unpacked_data[1]
		key_sucessor = unpacked_data[2]
		ip_sucessor = str(unpacked_data[3]) + '.' + str(unpacked_data[4]) + '.' + str(unpacked_data[5]) + '.' + str(unpacked_data[6])

		logging.debug('Receive from LookUp: Key = "%s" IP = "%s"' % (key_sucessor, ip_sucessor))

		return (key_sought, key_sucessor, ip_sucessor)

	def process_join_request(self, pkt):
		s = struct.Struct('! B I')
		unpacked_data = s.unpack(*pkt)
		lookup(self.ip, self.key, unpacked_data[1])

	def process_leave_request(self):
		print('passou')

	def process_update_request(self):
		print('passou')

	def process_my_update(self):
		print('passou')

	def listen(self, pkt_type):
		logging.info('Creating server...')
		server_address = (self.ip, self.port)

		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind(server_address)
		sock.setblocking(0)
		logging.debug('Starting up on %s port %s ...' % server_address)

		data = None
		address = None
		answered = False
		logging.info('Waiting to receive message...')

		while not answered :
			try:
				data, address = sock.recvfrom(4096)
				logging.debug('Received %s bytes from %s' % (len(data), address))
				pattern = '!' + str(len(packed_pkt)) + 'B'
				s = struct.Struct(pattern)
				cod_message = s.unpack(packed_pkt)[0]

				if (cod_message == pkt_type):
					self.process_join_request(packed_pkt, address)
					answered = True
				elif (cod_message == pkt_type):
					self.process_leave_request()
					answered = True
				elif (cod_message == pkt_type):
					self.process_lookup_request(packed_pkt)
					answered = True
				elif (cod_message == pkt_type):
					self.process_update_request()
					answered = True
				elif (cod_message == pkt_type):
					logging.warning('Join answer not expected. Ignoring...')
					answered = True
				elif (cod_message == pkt_type):
					logging.warning('Leave answer not expected. Ignoring...')
					answered = True
				elif (cod_message == pkt_type):
					logging.info('Answer lookup')
					self.process_my_lookup(packed_pkt)
					answered = True
				elif (cod_message == pkt_type):
					self.process_my_update()
					answered = True
				else:
					logging.error('Unknown code message')
			except:
				pass

		sock.close()
		logging.info('Closing listener')

# Configuration of log messages
logging.basicConfig(level  = logging.DEBUG,
                    format = '[ %(levelname)-6s] (%(threadName)-8s) %(message)s',
                    )
