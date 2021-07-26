import motion
import time
import multiprocessing
from common.tools import *
from common.init import *


#manager = multiprocessing.Manager()



# def checkServerMessage():
#     '''checks for incoming server messages until one appears and return the message'''
#     while com.currentServerMessage == "":
#         time.sleep(.1)
#     with lock:
#         clientData = com.currentServerMessage 
#         com.currentServerMessage = ""
#     return clientData




if __name__ == '__main__':
    commThread = threading.Thread(target=com.listen)
    commThread.start()
    lprint("commThread started")
    commThread.join()
    lprint("Program finished...")




