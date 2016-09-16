import random
import logging
import threading
import time
import socket
import struct

cod_request_join = 0
cod_request_leave = 1
cod_request_lookup = 2
cod_request_update = 3

cod_answer_join = 128
cod_answer_leave = 129
cod_answer_lookup = 130
cod_answer_update = 131

shouldIBeAlive = False
expecting_lookup = False
pending_loopup = []