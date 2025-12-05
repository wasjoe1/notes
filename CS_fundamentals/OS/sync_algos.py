# Synchronization algos

# PETERSON ALGORITHM
# TEST & SET/ TEST AND SET

# --------------------------------------------------------------------------------------------------------------
# PETERSON ALGORITHM
# concept:
    # have a "flag" that says whether u acquired the lock, and a global "turn" variable
    # flag indicates that current thread is interested in entering CS
    # turn indiacates who is allowed to enter
    # when releasing, a thread only needs to set that its not interested anymore
import threading
import time

class PetersonLock:
    def __init__(self):
        self.flag = [False, False]  # flag for each thread
        self.turn = 0                # whose turn it is

    def acquire(self, thread_id):
        other = 1 - thread_id # its either 1 or 0
        self.flag[thread_id] = True # pi wants to enter; we are interested in entering CS
        self.turn = other # set pj turn; give away to another person first

        # keep looping if its the other person's turn & is interested (flag)
        while self.flag[other] and self.turn == other:
            time.sleep(0.001) # prevent aggressive spinning
        # exits if its our turn OR other person not interested (flag)

    def release(self, thread_id):
        self.flag[thread_id] = False # no need to set turn, since thats only for when there's a contention

# --------------------------------------------------------------------------------------------------------------
# TEST & SET/ TEST AND SET
# concept:
    # to test_and_set a lock in 1 atomic operation
    # when lock is false => it is free & not acquired yet
    # enter a while loop and do an atomic action to (1) check if the lock is false [TEST] (2) set the lock if it is [SET]
    # else u keep running in a loop
import threading
import time
class Lock:
    lock = False # CLASS VARIABLE
    lock_real = threading.Lock() # acquire the real lock to make this atomic => # CLASS VARIABLE

    def acquire(self):
        '''
        acquire the lock so no one else can enter (or get stuck here since another thread is executing)
        '''
        while True:
            # make this atomic
            Lock.lock_real.acquire()
            # now this is an atomic action
            try:
                # if its not locked, acquire it and return
                if not Lock.lock:
                    Lock.lock = True
                    return
                # if its locked, sleep
                time.sleep(0.001)
            finally:
                Lock.lock_real.release()

    def release(self):
        '''
        release the lock so another thread can enter
        '''
        # acquire the lock_real so that only ur setting the lock & there wouldnt be race conditions
        with Lock.lock_real:
            Lock.lock = False
