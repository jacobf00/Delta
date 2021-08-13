import os
import time
import queue
import threading
import logging
'''contains initialized variables vital for the program'''

logging.basicConfig(filename='Delta/data/runtime.log',level=logging.INFO)

lock = threading.Lock()

def lprint(*a,**b):
    with lock:
        logging.info(*a,**b)
        print(*a,**b)

toServerQueue = queue.Queue(50)

ns = {}

ns['serverAdr'] = '10.6.1.26'
ns['serverPort'] = 5001
ns['listenPort'] = 5002
ns['commRunning'] = True
ns['encryptionEnabled'] = True



