from node import *

node = Node('192.168.1.100')
(ant_addr, suc_addr) = node.lookup(1, '192.168.1.142', 12233)
error = node.join() # manda join pro sucessor
if (!error):
    node.update() # faz update do antecessor
