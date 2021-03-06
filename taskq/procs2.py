# procs2.py
import multiprocessing as mp
from base import fib


def worker(inputq, outputq):
    while True:
        work = inputq.get()
        if work is None:
            break

        fn, args = work
        res = fn(*args)
        outputq.put(res)


if __name__ == '__main__':
    N = 35
    NUM_WORKERS = 4

    tasks = mp.Queue()
    results = mp.Queue()
    for i in range(NUM_WORKERS):
        tasks.put((fib, (N, )))

    for i in range(NUM_WORKERS):
        mp.Process(target=worker, args=(tasks, results)).start()

    for i in range(NUM_WORKERS):
        results.get()

    for i in range(NUM_WORKERS):
        tasks.put(None)
