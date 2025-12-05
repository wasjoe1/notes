# FILES, ... TODO: 
# sockets (ports, sockets, file descriptors)
=> port is not a kernel object, but a socket is (it is the equivalent of a inode)
=> layer abstraction: Process → FD table → Open file table → Inode (or socket, etc.)
=> open file table contains open file descriptions (each entry is 1 open file description; represented by a struct file in the kernel)
=> It stores info like: File offset (for read/write), Access mode (O_RDONLY, etc.), Flags, Pointer to the underlying inode or socket, Reference count
=> on fork, child can share the same open file description
    => they share the same socket object i.e. both processes are listening on the same listen socket and can accept connections from the socket
    => kernel maintains a queue of pending connections for that socket
    => when there is a parallel accept() (i.e. 2 accept() called), both enter the kernel, sleeping on the same wait queue
    => when a new connection arrives, kernel wakes exactly 1 of the waiting accept() calls
    => that 1 process gets the connection while the other stays sleeping
    => thundering herd problem => previously linux systems would wake all accept() calls, and the rest would need to go back to sleep (this wastes CPU cycles 99 syscalls + context switch + 99 mode transitions)
    => modern linux systems keep accept() connections on a wait queue => so it only wakes 1 process up

--------------------------------------------------------------------------------
# SYNCHRONIZATION
# Test & Set (Busy wait mutex)
lock => shared bool variable
* has a test_and_set(lock) method
* while test_and_set(lock): is a gateway to a CS

```python
def test_set(lock):
    old_val = lock
    lock = True # set this to True so no other thread/processes can enter once you have entered
    return old_val

lock = False
while test_and_set(lock): # will only pass through if the lock is false; test for false, set to true
    pass
print("im in CS section")
```
* full implementation in ./python_implementations.py

--------------------------------------------------------------------------------
# Memory management (Virtual memory)
* segmentation scheme => solves internal fragmentation; leads to external fragmentation
    - segmentation allocates mem in variable-sized segments
    - only allocate what process needs; these segments match the exact size required by the process's logical parts (i.e. code, data or stack)
* paging scheme => solves external fragmentation; leads to internal fragmentation
    - paging breaks mem into fixed size blocks, any free frame can be used, processes dont need a single large contiguous block
    - always allocation of mem to multiple small parts
    - eliminates external fragmentation
* internal fragmentation - occurs when a process is allocated a fixed-size block of mem that is larger than it needs |-----|--wasted--|
* external fragmentation - occurs when free mem is split into many small scattered blocks, creating enough total free space but not a contiguous one for a large space request
