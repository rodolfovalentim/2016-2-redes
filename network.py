from node import *
import random

node = Node('192.168.1.100')
node.lookup(1, '192.168.1.142', 12233)
node.setAlive()
t = threading.Thread(target=node.listen)
t.start()