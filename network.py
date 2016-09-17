from node import *
import logging

# 192.168.1.235

def join():
    pass
def leave():
    pass
def lookup():
    pass
def update():
    pass

def keyboard():
    while True:
        nb = raw_input('< JOIN / LEAVE / LOOKUP / UPDATE / EXIT > Choose:')
        if (nb == 'JOIN'):
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

keyboard()
