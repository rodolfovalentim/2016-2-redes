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

def keyboard():
    while True:
        nb = raw_input('< CREATE / JOIN / LEAVE / LOOKUP / UPDATE / EXIT > Choose:')
        if (nb == 'CREATE'):
            pass
        elif (nb == 'JOIN'):
            pass
        elif (nb == 'LEAVE'):
            node.leave()
            break
        elif (nb == 'LOOKUP'):
            pass
        elif (nb == 'UPDATE'):
            pass
        elif (nb == 'EXIT'):
            break
        else:
            logging.error('Option not find')
    logging.error('Exiting')

ip = raw_input('Your IP: ')
node = Node(ip)
t = threading.Thread(name='Listener', target=node.listener)
t.start()
join()
keyboard()
node.kill_listener()
