import socket
import sys
import struct
import binascii
import random
from node import *
import threading

node = Node('192.168.1.142')
node.create()
for i in range(8):
	node.expected_pkt[i] = True
node.listener()
