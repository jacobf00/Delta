# import Delta
# import motion
import time
import socket
import threading
import multiprocessing

manager = multiprocessing.Manager()
ns = manager.dict()
messageLock = threading.Lock()

ns['serverAdr'] = '10.6.1.26'
ns['serverPort'] = 5001

