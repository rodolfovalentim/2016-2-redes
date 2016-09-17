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
    ip_sucessor = node.lookup(int(key_input), (node.ip_next, node.port))
    logging.info('Answer lookup %s' % ip_sucessor[2])

def update():
    node.update()

def exit():
    node.kill_listener()

def start_listener():
    t = threading.Thread(name='Listener', target=node.listener)
    t.start()

def info():
    print (node)

def list_nodes():
    t = PrettyTable(['COUNT','IP', 'KEY'])
    i = 0
    key = node.key
    ip = node.ip
    while True:
        info_sucessor = node.lookup(int(key), (ip, node.port))
        t.add_row([str(i), ip, str(key)])
        i = i + 1
        key = info_sucessor[1]
        ip = info_sucessor[2]
        if (key == node.key):
            break
    print t

def start_keyboard():
    state = 0
    while True:
        if (state == 0):
            nb = raw_input('< CREATE / JOIN / INFO / EXIT > Choose:')
            if (nb == 'CREATE'):
                create()
                state = 1
            elif (nb == 'JOIN'):
                join()
                state = 1
            elif (nb == 'INFO'):
                info()
            elif (nb == 'EXIT'):
                exit()
                break
            else:
                logging.warning('Option not find')
        else:
            nb = raw_input('< LEAVE / LOOKUP / UPDATE / INFO / LIST > Choose:')
            if (nb == 'LEAVE'):
                leave()
                state = 0
            elif (nb == 'LOOKUP'):
                lookup()
            elif (nb == 'UPDATE'):
                update()
            elif (nb == 'INFO'):
                info()
            elif (nb == 'LIST'):
                list_nodes()
            else:
                logging.warning('Option not find')
    logging.info('Exiting')

ip = raw_input('Your IP: ')
node = Node(ip)
start_listener()
start_keyboard()
