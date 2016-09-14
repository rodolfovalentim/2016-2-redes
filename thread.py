import logging
import threading
import time
import socket
import struct

logging.basicConfig(level  = logging.DEBUG,
                    format = '[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

def worker():
    logging.debug('Starting')
    while True:
    	var_input = input("Entre uma letra!")
    	if (var_input == 9):
    		break
    	print var_input
    logging.debug('Exiting')



t = threading.Thread(name = 'input', target = server)
w = threading.Thread(name = 'worker', target = worker)

w.start()
t.start()