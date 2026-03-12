# DB implementation notes
This notes cover how a DB is typically implemented to ensure ACID properties.
Atomicity - 1 transaction is a single unit (all or nth)
Consistency - ensures all predefinedrules are satisfied (no invalid data) => different from CAP's consistency
Isolation - 1 transaction does not affect another
Durability - data is not loss during system crash (for committed transactions)

# DB implementation
# THREAD POOL efficiency & implementation

# -------------------------------------------------------------------------------------------------
# DB implementation
- locks
- MEM non-corruption mechanism

## how to prevent MEM corruption
howt to avoid corruption? corruption mainly occurs when multiple threads modify shared resources 2 main ways:
1. sync mechanisms (tackle race conditions)
2. buffer pool (single instance of pg in-MEM)

### 1. sync mechanisms
spin lock -> for pg metadata => dont need to wait too long to receive
mutex -> transaction manager => prevent CPU wastage
rw latch ->  B-tree nodes => allow many readers & 1 writer to write back the dirty pg

* buffer pool metadata: 
* pg latch 
* WAL buffer metadata
* transaction isolation
    - requires a lock manager
    - has a lock table
    ```
    Lock table
    ---------
    Row 10 → owned by T1
    Row 25 → owned by T2
    ```
    - if another transaction reqs `row 10` => this transaction waits

full process:
Transaction starts
        ↓
Lock manager acquires row lock (mutex protected structure)
    => `row table has a lock here` ensuring each transaction checks row table at 1 time; since they might edit the same row, if not they can continue accessing
    => multiple transactiosn can edit rows, just not the same row!!
        ↓
Traverse B-tree index
        ↓
Acquire page latch (rw latch)
        ↓
Modify page in buffer pool
        ↓
Append WAL record (spinlock protects WAL buffer)
        ↓
Release page latch
        ↓
Commit transaction
        ↓
Release row lock

### 2. buffer pool
- instead of workers allocating random mem or writing directly to disk pages
- DB manages a fixed pool of pages in RAM => workers will operate on these in RAM
- this shared MEM is also called `buffer pool` (managed MEM)
- worker threads access page with latches(light weight mutex)

i.e. 
Thread A loads page 10
Thread B loads page 10
Thread A updates row
Thread B updates row
* so now 2 different copies of pg 10 are in MEM => corruption of data
=> buffer pool ensures exactly 1 in-MEM copy of each disk page!!

* flow: thread wants to update row -> get page in `buffer pool` -> acquire page latch -> modify MEM -> release latch -> write record to WAL (1. write to in-MEM WAL 2. flush in-MEM WAL to disk) -> transaction commit -> pg stays dirty in buffer pool -> bg flusher eventually writes page to disk
* WAL must be written b4 page flush
* the WAL also has a buffer in MEM
    - b4 a transaction can commit, WAL buffer must be flushed to the disk
    - to guarantee durability, DB must fsync the WAL to disk (flush the entries of in-MEM WAL to disk)
    - this is better coz entire commits of page (8Kb) is bigger than WAL entry (50 bytes max?)
* flush WAL vs transaction commit
    - commit - DB declares the transaction permanently successful & durable
    - a logical state change, not a disk op
    - can have indiv commits OR group commits
        - flush once (multiple entries)
        - multiple commits
        ```
        T1 commit
        T2 commit
        T3 commit
        ```
    - page write is not required for durability later on
    - e.g. entry `update row id=10 balance=500`
* thread pooling prevents thread creation over head => but dont prevent MEM corruption!!

main concepts:
- latches -> protect in-MEM structures (light weight mutex)
- locks -> protect transaction isolation
- buffer pool -> controlled MEM mgmt
- WAL -> crash recovery

common latch types:
- spinlock => repeatedly checks the lock until it becomes avail => thread doesnt slp, spins on the CPU (BUSY wait)
    => not good if lock is held for long
    => used when lock is expected to be microseconds
- light weight mutex => allows thread to slp if lock is unavail
    => used for longer CS
- read-write latch => allows multiple readers but only 1 writer
    => all readers need to wait
    => use for read heavy workloads

# -------------------------------------------------------------------------------------------------
# THREAD POOL efficiency & implementation
# why is a thread pool efficient?
- reusability:
    - less overhead (CPU & MEM)
    - no creation & desctruction of threads for every single task
- back pressure:
    - if tasks arrive faster than they can be processed, q holds them safely without over using resources
    - system wont try to spawn 10k thread & crash due to OOMem error
- improvement in response time/ latency:
    - threads has no initialization time
- controlled concurency:
    - bound # of active threads
    - reduce context switching
- (CONSIDERATION) Thread pool size:
    - CPU bound tasks => pool size best set to # of CPU cores
    - IO bound tasks => increase pool size more than # core since tasks dont often fully utilize CPU (2-4 times usually good)
    - manage resources => dont let system create unlimited threads, can overwhelm CPU/ MEM


# thread pool implementation
- thread pool - pre-created set of worker threads
    - if u create new threads every single time => alot of overhead => constant creation & destuction is inefficient
- task queue is required to hold submitted tasks until a worker is free
- producer-consumer architecture
- how is it implemented UTH
    - task queue (via subimt(task)) holds task in FIFO
    - worker threads (consumers) run a continuous while loop & calls queue.take() => sleeps if no task, 0 CPU used

```python
# XX WRONG IMPLEMENTATION XX
while (True):
    task = queue.take() # blocking, if nothing it sleeps here
    
    __poll for available thread__ # blocking as well, if no available threads, sleep here too => idk what data structure should be used for worker threads though??? is it also a queue? though a queue would mean a busy thread blocks a free thread
    
    thread.run_task(task)
```
* we actually dont need to POLL FOR THREADS => we just need to have each thread await the task (they will go to sleep if there isnt a task)

```python
# roughly CORRECT IMPLEMENTATION
# This is what each Worker Thread does internally
class Worker(Thread):
    def run(self):
        while True:
            # 1. Block here until a task is available in the queue
            # The OS puts the thread to 'sleep' so it uses 0% CPU
            task = task_queue.get() 
            
            # 2. Execute the task
            task.execute()
            
            # 3. Task is done; loop back to get() and wait again
```
