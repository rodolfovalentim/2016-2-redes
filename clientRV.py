from node import *
import threading
import time
default_port = 12233

def join():
    contact_ip = raw_input('IP of your contact in the network: ')

    while(True):
        ip_sucessor = node.lookup(node.key, (contact_ip, default_port))
        logging.info(ip_sucessor)
        if(not node.join(ip_sucessor[2])):
            node.get_new_key()
            continue
        if(not node.update()):
            node.get_new_key()
            continue
        break

ip = raw_input('Your IP: ')
node = Node(ip)
t = threading.Thread(name='Listener', target=node.listener)
t.start()
join()
node.kill_listener()
