import threading
from comm import comm
lock = threading.Lock()

ns = {}

ns['serverAdr'] = '10.6.1.26'
ns['serverPort'] = 5001
ns['listenPort'] = 5002
ns['serverMessageHandlerRunning'] = True
com = comm(Inet=ns['serverAdr'],send_port=ns['serverPort'],listen_port=ns['listenPort'])

def lprint(*a,**b):
    with lock:
        print(*a,**b)