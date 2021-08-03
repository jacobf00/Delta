import os
import time
import queue
import threading
'''contains initialized variables vital for the program'''

lock = threading.Lock()

def lprint(*a,**b):
    with lock:
        print(*a,**b)

toServerQueue = queue.Queue(50)

ns = {}

ns['serverAdr'] = '10.6.1.26'
ns['serverPort'] = 5001
ns['listenPort'] = 5002
ns['serverMessageHandlerRunning'] = True
ns['commRunning'] = True
ns['encryptionEnabled'] = True



