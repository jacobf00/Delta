import os
import time
from common.lock_print import *
import queue

'''contains initialized variables vital for the program'''

toServerQueue = queue.Queue(50)

ns = {}

ns['serverAdr'] = '10.6.1.26'
ns['serverPort'] = 5001
ns['listenPort'] = 5002
ns['serverMessageHandlerRunning'] = True
ns['commRunning'] = True
ns['encryptionEnabled'] = True



