import common.motion
import time
import multiprocessing
from common.init import *
from common.comm import comm



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
    com = comm(Inet=ns['serverAdr'],send_port=ns['serverPort'],listen_port=ns['listenPort'])
    commThread = threading.Thread(target=com.listen)
    commThread.start()
    lprint("commThread started")
    commThread.join()
    lprint("Program finished...")
    Delta1.disableTorque()




