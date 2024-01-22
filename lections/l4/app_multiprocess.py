import multiprocessing
from time import sleep

some_data = multiprocessing.Value('i', 0)


def worker(i):
    # processes does not share data with each other,
    # instead they copy variables on start?
    sleep(1)


def increment(cnt):
    for _ in range(10_000):
        with cnt.get_lock():  # lock shared value
            cnt.value += 1


if __name__ == '__main__':
    processes = []
    # for i in range(5):
    #     p = multiprocessing.Process(target=worker, args=(i,))
    #     processes.append(p)
    #     p.start()  # same as with threads
    # for p in processes:
    #     p.join()  # same as with threads
    for i in range(5):
        p = multiprocessing.Process(target=increment, args=(some_data,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
