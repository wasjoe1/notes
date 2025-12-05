#!/usr/bin/env python3
# note: A coroutine is a specialized version of a Python generator function

# a coroutine is a function that can suspend its execution before reaching return,
# and it can indirectly pass control to another coroutine for some time.

import asyncio

async def count(num): # vs def
    print(f"{num}:", "One")
    await asyncio.sleep(1) # vs time.sleep()
    print(f"{num}:","Two")

async def main():
    # await asyncio.gather(count(), count(), count()) # => single event loop/ coordinator coordinates all the count(), lets other count() exec
    res = await asyncio.gather(*[count(i) for i in range(50)])
    print()

if __name__ == "__main__":
    import time
    s = time.perf_counter() # single time stamp
    
    asyncio.run(main()) # runs main in an event loop that allows async tasks in main() to execute concurrently
    # executes all count() calls concurrently in a single threaded event loop
    
    elapsed = time.perf_counter() - s # end time stamp
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")

# Execute:
# $ python3 countasync.py
# One
# One
# One
# Two
# Two
# Two
# countasync.py executed in 1.01 seconds.

# ----------------------------------------
# import time

# def count():
#     print("One")
#     time.sleep(1)
#     print("Two")

# def main():
#     for _ in range(3):
#         count()

# if __name__ == "__main__":
#     s = time.perf_counter()
#     main()
#     elapsed = time.perf_counter() - s
#     print(f"{__file__} executed in {elapsed:0.2f} seconds.")

# Execute:
# $ python3 countsync.py
# One
# Two
# One
# Two
# One
# Two
# countsync.py executed in 3.01 seconds.