# import Delta
# import motion
import time
import socket
import threading
import multiprocessing
from comm import comm

#manager = multiprocessing.Manager()
ns = {}
lock = threading.Lock()

ns['serverAdr'] = '10.6.1.26'
ns['serverPort'] = 5001
ns['listenPort'] = 5002


if __name__ == '__main__':
    com = comm(Inet=ns['serverAdr'],send_port=ns['serverPort'],listen_port=ns['listenPort'])
    clientData = com.listen()
    print("received " + clientData + " from " + com.inet)

