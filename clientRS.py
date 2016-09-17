from node import *

ip = raw_input('Your IP: ')
node = Node(ip)
node.create()
node.expected_pkt[0] = True
node.expected_pkt[1] = True
node.expected_pkt[2] = True
node.expected_pkt[3] = True
node.listener()
