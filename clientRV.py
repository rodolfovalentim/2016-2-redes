from node import *
import threading

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
node.set_mask(7)
node.set_mask(6)
node.set_mask(5)
node.set_mask(4)
t = threading.Thread(name='Listener', target=node.listener)
t.start()
join()
