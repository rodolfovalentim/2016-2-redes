from node import *

node = Node('127.0.0.1')
(key_sought, key_sucessor, ip_sucessor) = node.lookup(1, ('127.0.0.1', 12244))
#error = node.join() # manda join pro sucessor
#if (!error):
#    node.update() # faz update do antecessor
