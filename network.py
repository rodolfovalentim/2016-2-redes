from node import *
import logging

# 192.168.1.235
node = None
default_port = 12233

def create():
    pass
    node.create()
def join():
    pass
    contact_ip = raw_input('IP of your contact in the network: ')

    while(True)
        (, , ip_sucessor) = node.lookup(node.key, (contact_ip, default_port))
        if(not node.join(ip_sucessor))
            node.get_new_key()
            continue
        if(not node.update())
            node.get_new_key()
            continue
        break

def leave():
    pass
    #leave
def lookup():
    pass
    #recebe input
    #lookup
def update():
    pass
    #lookup

def keyboard():
    while True:
        nb = raw_input('< CREATE / JOIN / LEAVE / LOOKUP / UPDATE / EXIT > Choose:')
        if (nb == 'CREATE'):
            logging.info('node.create()')
        elif (nb == 'JOIN'):
            logging.info('node.join()')
        elif (nb == 'LEAVE'):
            logging.info('node.leave()')
        elif (nb == 'LOOKUP'):
            logging.info('node.lookup()')
        elif (nb == 'UPDATE'):
            logging.info('node.update()')
        elif (nb == 'EXIT'):
            break
        else:
            logging.error('Option not find')
    logging.error('Exiting')

ip = raw_input('Your IP: ')
node = Node(ip)
