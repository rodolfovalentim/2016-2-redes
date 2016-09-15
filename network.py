## Codigo principal
import struct
import binascii

def process_join ():
	print 'teste'

def process_leave ():
	print 'teste'

def process_lookup ():
	print 'teste'

def process_update ():
	print 'teste'

def make_pkt(method, id_node, id_ant, ip_ant, id_prox, ip_prox):
	if method == 1:
		values = (method, id_node)
		s = struct.Struct('! B I')
		return s.pack(*values)
	elif method == 2:
		ip_ant_form = ip_ant.split('.')
		ip_prox_form = ip_prox.split('.')
		if(len(ip_ant_form) != 4 or len(ip_prox_form) != 4):
			Logging.error('Wrong IP pattern')
			return
		values = (method, id_node, id_ant, 
				int(ip_ant_form[0]), int(ip_ant_form[1]), 
				int(ip_ant_form[2]), int(ip_ant_form[3]),  
				id_prox, 
				int(ip_prox_form[0]), int(ip_prox_form[1]), 
				int(ip_prox_form[2]), int(ip_prox_form[3]),)
		print(values)
		s = struct.Struct('! B I I B B B B I B B B B')
		return s.pack(*values)
	elif method == 3 or method == 4:
		ip_origin_form = ip_ant.split('.')
		if(len(ip_origin_form) != 4):
			Logging.error('Wrong IP pattern')
			return
		values = (method, id_node, int(ip_origin_form[0]), int(ip_origin_form[1]), 
				int(ip_origin_form[2]), int(ip_origin_form[3]), id_prox)
		s = struct.Struct('! B I B B B B I')
		return s.pack(*values)
	else:
		logging.error('Package type not found')

def read_pkt(packed_pkt):
	hex_data = binascii.hexlify(packed_pkt)
	text_string = hex_data.decode('utf-8')
	method = int(text_string[:2])
	print(method)

	# # tem que pegar apenas os dois primeiros
	# if method == 128:
	# 	s = struct.Struct('! B B I B B B B I B B B B')
	# elif method == 129:
	# 	s = struct.Struct('! I B')
	# elif method == 130:
	# 	s = struct.Struct('! B I I B B B B')
	# elif method == 131:
	# 	s = struct.Struct('! B B I')
	# return s.unpack(packed_pkt)

hostname = socket.gethostbyname(socket.gethostname())
node = Node(hostname)
node.join('192.168.1.142')
