from node import *
import logging

# 192.168.1.235
node = None

def create():
    node.create()
    node.set_mask(0, True)
    node.set_mask(1, True)
    node.set_mask(2, True)
    node.set_mask(3, True)

def join():
    contact_ip = raw_input('IP of your contact in the network: ')

    while(True):
        ip_sucessor = node.lookup(node.key, (contact_ip, node.port))
        logging.info(ip_sucessor)
        if(not node.join(ip_sucessor[2])):
            node.get_new_key()
            continue
        if(not node.update()):
            node.get_new_key()
            continue
        break
    node.set_mask(0, True)
    node.set_mask(1, True)
    node.set_mask(2, True)
    node.set_mask(3, True)

def leave():
    node.set_mask(0, False)
    node.set_mask(1, False)
    node.set_mask(2, False)
    node.set_mask(3, False)
    node.leave()
def lookup():
    key_input = raw_input('Type the key to look up: ')
    ip_sucessor = node.lookup(key_input, (node.ip_next, node.port))
    logging.info('Answer lookup %s' % ip_sucessor)

def update():
    node.update()

def exit()
    node.kill_listener()

def keyboard():
    while True:
        nb = raw_input('< CREATE / JOIN / LEAVE / LOOKUP / UPDATE / EXIT > Choose:')
        if (nb == 'CREATE'):
            create()
        elif (nb == 'JOIN'):
            join()
        elif (nb == 'LEAVE'):
            leave()
        elif (nb == 'LOOKUP'):
            lookup()
        elif (nb == 'UPDATE'):
            update()
        elif (nb == 'EXIT'):
            exit()
            break
        else:
            logging.error('Option not find')
    logging.error('Exiting')

ip = raw_input('Your IP: ')
node = Node(ip)
