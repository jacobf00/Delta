import threading

def lprint(*a,**b):
    with lock:
        print(*a,**b)


lock = threading.Lock()


