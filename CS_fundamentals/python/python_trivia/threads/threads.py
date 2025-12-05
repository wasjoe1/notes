#!usr/bin/env python3

# Threads are the smallest unit of processing that can be scheduled by an
# operating system.

import threading
import time
# Threads
threads = [] # have a pool of threads
def func(num):
    print("start: ", num)
    time.sleep(2)
    print("end: ", num)

# Create and start a thread for each function
for i in range(100):
    thread = threading.Thread( target=func, args=(i,) )
    thread.start()
    threads.append(thread)  # Keep track of the threads

# Wait for all threads to complete
for thread in threads:
    thread.join()
print("end of execution")

# ------------------------------------------------
# Using thread pool
from concurrent.futures import ThreadPoolExecutor

def worker(num):
    print(f'Thread {num} is working')

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=4) as executor:  # Create a pool with 4 threads
        executor.map(worker, range(10))  # Run `worker` on a list of inputs