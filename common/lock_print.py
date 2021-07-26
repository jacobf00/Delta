import threading

lock = threading.Lock()

def lprint(*a,**b):
    with lock:
        print(*a,**b)