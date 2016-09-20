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

    attempt = 1
    while(attempt < 4):
        logging.info("Attempt %s/3 to join network", attempt)
        ip_sucessor = node.lookup(node.key, (contact_ip, node.port))
        if(node.timeout[2]):
            attempt = attempt + 1
            continue
        if(not node.join(ip_sucessor[2])):
            node.get_new_key()
            attempt = attempt + 1
            continue
        if (node.timeout[0]):
            break
        if(not node.update()):
            attempt = attempt + 1
            node.get_new_key()
            continue
        if (node.timeout[3]):
            break
        logging.info("Successfully joined to network")
        node.set_mask(0, True)
        node.set_mask(1, True)
        node.set_mask(2, True)
        node.set_mask(3, True)
        global state
        state = 1
        break

def leave():
    node.set_mask(0, False)
    node.set_mask(1, False)
    node.set_mask(2, False)
    node.set_mask(3, False)
    node.leave()
    global state
    state = 0

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
    global state
    while True:
        if (state == 0):
            nb = raw_input('< CREATE / JOIN / INFO / EXIT > Choose:\n')
            if (nb == 'CREATE' or nb == 'create' ):
                create()
                state = 1
            elif (nb == 'JOIN' or nb == 'join' ):
                join()
            elif (nb == 'INFO' or nb == 'info' ):
                info()
            elif (nb == 'EXIT' or nb == 'exit' ):
                exit()
                break
            else:
                logging.warning('Option not find')
        else:
            nb = raw_input('< LEAVE / LOOKUP / UPDATE / INFO / LIST > Choose:')
            if (nb == 'LEAVE' or nb == 'leave' ):
                leave()
            elif (nb == 'LOOKUP' or nb == 'lookup' ):
                lookup()
            elif (nb == 'UPDATE' or nb == 'update' ):
                update()
            elif (nb == 'INFO' or nb == 'info' ):
                info()
            elif (nb == 'LIST' or nb == 'list' ):
                list_nodes()
            else:
                logging.warning('Option not find')
    logging.info('Exiting')

state = 0
ip = raw_input('Your IP: ')
node = Node(ip)
start_listener()
start_keyboard()
