import threading
from time import sleep

# semaphore


def do_something(i: int = 0):
    sleep(1)


threads = []
for i in range(5):
    threads.append(threading.Thread(target=do_something, args=(i,)))
    threads[i].start()  # launch thread

for t in threads:
    t.join()  # wait for thread to be done
