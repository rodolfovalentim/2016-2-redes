import random
import logging
import threading
import time
import socket
import struct

class Node:
	'A node in the network'
	cod_join_request = 0
	cod_leave_request = 1
	cod_lookup_request = 2
	cod_update_request = 3

	cod_join_answer = 128
	cod_leave_answer = 129
	cod_lookup_answer = 130
	cod_update_answer = 131

	recv_data = None

	expected_pkt = [False, False, False, False, False, False, False, False]

	def __init__(self, ip):
		self.ip = ip
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

		contact_address = (contact_ip, self.port) #change self.port to default_port

		# building package
		data = (self.cod_join_request, self.key)

		s = struct.Struct('! B I')
		packed_data = s.pack(*data)

		# Send join message and wait for answer
		self.sender(contact_address, packed_data)
		self.expected_pkt[4] == True
		while not self.expected_pkt[4]:
			pass

		return self.recv_data

	def process_join_request(self, pkt, address):
		logging.info('Join Received')
		s = struct.Struct('! B I')
		unpacked_data = s.unpack(pkt)
		error_code = 1

		condition = unpacked_data[1] == self.key or unpacked_data[1] == self.key_next or unpacked_data[1] == self.key_prev

		if(condition):
			error_code = 0

		ip_prev_fmt = self.ip_prev.split('.')
		ip_next_fmt = self.ip.split('.')
		data = (self.cod_join_answer, error_code,self.key, int(ip_next_fmt[0]), int(ip_next_fmt[1]), int(ip_next_fmt[2]), int(ip_next_fmt[3]),self.key_prev, int(ip_prev_fmt[0]), int(ip_prev_fmt[1]), int(ip_prev_fmt[2]), int(ip_prev_fmt[3]))
		s = struct.Struct('! B B I B B B B I B B B B')
		packed_data = s.pack(*data)

		logging.debug(data)
		if not condition:
			self.ip_prev = address[0]
			self.key_prev = unpacked_data[1]

		self.sender(address, packed_data)

	def process_join_answer(self, pkt, address):
		# unpacking data
		s = struct.Struct('! B B I B B B B I B B B B')
		unpacked_data = s.unpack(pkt)

		logging.debug('Unpacked Values: %s', (unpacked_data))

		if (unpacked_data[1] == 1):
			logging.info('Information about next node obtained. Should update previous node...')
			logging.info('Information about next node obtained. Should update next node...')
		elif (unpacked_data[1] == 0):
			logging.error('Key already exist. Try again...')
			return False
		else:
			logging.error('Unknown error. Verify connection or package string pattern!')

		self.key_next = unpacked_data[2]
		self.ip_next = str(unpacked_data[3]) + '.' + str(unpacked_data[4]) + '.' + str(unpacked_data[5]) + '.' + str(unpacked_data[6])
		self.key_prev = unpacked_data[7]
		self.ip_prev = str(unpacked_data[8]) + '.' + str(unpacked_data[9]) + '.' + str(unpacked_data[10]) + '.' + str(unpacked_data[11])

		return True

	def leave(self):
		logging.info('Leaving network...')

		contact_address = ((self.ip_prev, self.port), (self.ip_next, self.port))

		# building package
		ip_prev_form = self.ip_prev.split('.')
		ip_next_form = self.ip_next.split('.')

		if(len(ip_prev_form) != 4 or len(ip_next_form) != 4):
			Logging.error('Wrong IP pattern')
			return

		values = (self.cod_leave_request, self.key, self.key_next,
				int(ip_next_form[0]), int(ip_next_form[1]),
				int(ip_next_form[2]), int(ip_next_form[3]),
				self.key_prev,
				int(ip_prev_form[0]), int(ip_prev_form[1]),
				int(ip_prev_form[2]), int(ip_prev_form[3]),)

		s = struct.Struct('! B I I B B B B I B B B B')
		packed_data = s.pack(*values)

		for i in range(2):
			self.sender(contact_address[i], packed_data)
			self.expected_pkt[5] = True

			while not self.expected_pkt[5]:
				pass

			logging.debug('Receive %s', self.recv_data)

		return

	def process_leave_request(self, pkt, address):
		pass

	def process_leave_answer(self, pkt, address):
		pass

	def update(self):
		logging.info('Executing update...')

		contact_address = (self.ip_prev, self.listen_port)

		# building package
		ip_fmt = self.ip.split('.')

		if (len(ip_fmt) != 4):
		    logging.error('Wrong IP pattern')
		    return

		data = (self.cod_request_update, self.key, self.key, int(ip_fmt[0]),
		        int(ip_fmt[1]), int(ip_fmt[2]), int(ip_fmt[3]))

		s = struct.Struct('! B I I B B B B')
		packed_data = s.pack(*data)

		self.sender(contact_address, packed_data)
		self.expected_pkt[7] = True

		while not self.expected_pkt[7]:
			pass

		return self.recv_data

	def process_update_request(self, pkt, address):
		logging.info('Update received...')

		#build package
		s = struct.Struct('! B I I B B B B')
		unpacked_data = s.unpack(pkt)
		received_key = unpacked_data[2]
		received_ip = str(unpacked_data[3]) + '.' + str(unpacked_data[4]) + '.' + str(unpacked_data[5]) + '.' + str(
		    unpacked_data[6])

		contact_address = (received_ip, self.port)

		# building package
		ip_fmt = self.ip.split('.')

		if (len(ip_fmt) != 4):
		    logging.error('Wrong IP pattern')
		    return
		error_code = None
		# Error verification
		if received_key == self.key or received_key == self.key_next or received_key == self.key_prev:
		    error_code = 0
		else:
		    self.ip_next = received_ip
		    self.key_next = received_key
		    error_code = 1
		data = (self.cod_answer_update, error_code, self.key)

		s = struct.Struct('! B B I')
		packed_data = s.pack(*data)

		# Send package
		self.sender(contact_address, packed_data)
		return None

	def process_update_answer(self, pkt, address):
	    logging.info('Update response recieved...')
	    s = struct.Struct('! B B I')
	    unpacked_data = s.unpack(pkt)

	    if unpacked_data[1] == 0:
	        logging.error('Update error from %s' % unpacked_data[2])
	    else:
	        logging.debug('%s successfully apdated' % unpacked_data[2])

	    return unpacked_data[1], unpacked_data[2]

	def lookup(self, key_sought, contact_address):
		logging.info('Looking up...')

		# building package
		ip_fmt = self.ip.split('.')

		if(len(ip_fmt) != 4):
			logging.error('Wrong IP pattern')
			return

		data = (self.cod_lookup_request, self.key, int(ip_fmt[0]), int(ip_fmt[1]),
				int(ip_fmt[2]), int(ip_fmt[3]), key_sought)

		s = struct.Struct('! B I B B B B I')
		packed_data = s.pack(*data)

		# Send lookup message and wait for answer
		self.sender(contact_address, packed_data)
		self.expected_pkt[6] = True

		while not self.expected_pkt[6]:
			pass

		return self.recv_data

	def process_lookup_request(self, packed_data, address):
		s = struct.Struct('! B I B B B B I')
		unpacked_data = s.unpack(packed_data)
		key_sought = unpacked_data[6]

		data = None
		dest_ip = None
		if ((key_sought >= self.key and (key_sought < self.key_next or self.key_next < self.key)) or (self.key_next < self.key and key_sought<self.key_next)):
			ip_fmt = self.ip_next.split('.')
			data = (self.cod_lookup_answer, key_sought, self.key_next, int(ip_fmt[0]), int(ip_fmt[1]), int(ip_fmt[2]), int(ip_fmt[3]))
			s = struct.Struct('! B I I B B B B')
			dest_ip = str(unpacked_data[2]) + '.' + str(unpacked_data[3]) + '.' + str(unpacked_data[4]) + '.' + str(unpacked_data[5])
		else:
			data = unpacked_data
			dest_ip = self.ip_next
			s = struct.Struct('! B I B B B B I')

		packed_data = s.pack(*data)
		contact_address = (dest_ip, self.port)
		self.sender(contact_address, packed_data)

		return

	def process_lookup_answer(self, pkt, address):
		logging.info('Processing look up answer...')
		s = struct.Struct('! B I I B B B B')
		unpacked_data = s.unpack(pkt)

		key_sought = unpacked_data[1]
		key_sucessor = unpacked_data[2]
		ip_sucessor = str(unpacked_data[3]) + '.' + str(unpacked_data[4]) + '.' + str(unpacked_data[5]) + '.' + str(unpacked_data[6])

		logging.debug('Receive from LookUp: Key = "%s" IP = "%s"' % (key_sucessor, ip_sucessor))

		return (key_sought, key_sucessor, ip_sucessor)

	def sender(self, contact_address, packed_data):
		server_address = (self.ip, self.port)

		logging.info('Creating socket...')
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind(server_address)

		try:
			# Send data
			logging.debug('Sending "%s" to %s' % (packed_data, contact_address))
			sent = sock.sendto(packed_data, contact_address)
		finally:
			# Closing socket
			logging.info('Closing socket...')
			sock.close()
			logging.info('Socket closed...')

	def listener(self):
		logging.info('Creating server...')
		server_address = (self.ip, self.port)

		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind(server_address)
		sock.setblocking(0)
		logging.debug('Starting up on %s port %s ...' % server_address)

		data = None
		address = None
		answered = False
		for i in range(8):
				answered = answered or self.expected_pkt[i]

		for i in range(8):
			answered = answered or self.expected_pkt[i]

		logging.info('Waiting to receive message...')

		while answered:
			try:
				data, address = sock.recvfrom(4096)
				pattern = '!' + str(len(data)) + 'B'
				s = struct.Struct(pattern)
				cod_message = s.unpack(data)[0]

				logging.debug('Received %s bytes from %s. Code-%s' % (len(data), address,cod_message))

				if (self.expected_pkt[0] and (cod_message == self.cod_join_request)):
					self.process_join_request(data, address)
				elif (self.expected_pkt[1] and cod_message == self.cod_leave_request):
					self.process_leave_request(data, address)
				elif (self.expected_pkt[2] and cod_message == self.cod_lookup_request):
					self.process_lookup_request(data, address)
				elif (self.expected_pkt[3] and cod_message == self.cod_update_request):
					self.process_update_request(data, address)
				elif (self.expected_pkt[4] and cod_message == self.cod_join_answer):
					self.recv_data = self.process_join_answer(data, address)
					self.expected_pkt[4] = False
				elif (self.expected_pkt[5] and cod_message == self.cod_leave_answer):
					self.recv_data = self.process_leave_answer(data, address)
					self.expected_pkt[5] = False
				elif (self.expected_pkt[6] and cod_message == self.cod_lookup_answer):
					self.recv_data = self.process_lookup_answer(data, address)
					self.expected_pkt[6] = False
				elif (self.expected_pkt[7] and cod_message == self.cod_update_answer):
					self.recv_data = self.process_update_answer(data, address)
					self.expected_pkt[7] = False
				else:
					logging.error('Unknown code message')
			except:
				pass

			answered = False
			for i in range(8):
				answered = answered or self.expected_pkt[i]

		sock.close()
		logging.info('Closing listener')
		return

# Configuration of log messages
logging.basicConfig(level  = logging.DEBUG,
                    format = '[ %(levelname)-6s] (%(threadName)-8s) %(message)s',
                    )
