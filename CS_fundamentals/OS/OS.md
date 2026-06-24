# file descriptors, open file descriptions, inodes (pointer & number) / sockets, ports

- file descriptor           => int
- open file descriptions    => struct
- inodes                    => struct
- sockets                   => struct
- ports                     => logical identifiers

=> port is not a kernel object, but a socket is (it is the equivalent of an inode);
    - a socket is just a network struct created by the OS to handle read and write operations from a remote client/ server (by a process); characterized by its local IP + port & remote IP + port & protocol (TCP / UDP)
    - a port is not a physical address nor location in MEM; its a 16 bit int number that acts as a _logical identifier_ inside the OS. it doesnt exist in isolation, it only becomes active when a socket claims it; a process requests to use a port by binding a socket to it
=> layer abstraction: Process → FD table (file descriptors) → Open file table (open file descriptions `struct file`) → Inode (or socket, etc.)
=> FD & FD table: given an FD int, which _open file description_ `struct file` does this point to
=> open file table contains entries called open file descriptions (each entry is 1 open file description; represented by a struct file in the kernel)
=> It stores info like: File offset (for read/write), Access mode (O_RDONLY, etc.), Flags, Pointer to the underlying inode or socket, Reference count
=> on fork, child can share the same open file description
    => they share the same socket object i.e. both processes are listening on the same listen socket and can accept connections from the socket
    => kernel maintains a queue of pending connections for that socket
    => when there is a parallel accept() (i.e. 2 accept() called), both enter the kernel, sleeping on the same wait queue
    => when a new connection arrives, kernel wakes exactly 1 of the waiting accept() calls
    => that 1 process gets the connection while the other stays sleeping
    => thundering herd problem => previously linux systems would wake all accept() calls, and the rest would need to go back to sleep (this wastes CPU cycles 99 syscalls + context switch + 99 mode transitions)
    => modern linux systems keep accept() connections on a wait queue => so it only wakes 1 process up

## epoll

epoll_create - creates an epoll instance (persistent state managed by linux kernel)
epoll_ctl - adds or removes sockets you want to monitor
epoll_wait - app waits on this function, kernel blocks calling thread & returns when there is actual I/O activity

`epoll_ctl(ADD, fd, ...)` - registering fd to epoll instance & enqueuing callback function to socket's waitqueue:
- kernel first checks if fd is already registered with epoll instance via RB tree lookup
_`epitem`_
- kernel creates a struct called `epitem` containing:
    - `struct rb_node rbn` - used for red black tree
    - `struct list_head rdllink` - used for the ready list; hooks it on to the ready list
    - `struct eventpoll *ep` - ptr to epoll instance
- the `epitem` (epoll item) is added to the epoll instance's red-black tree; the key of the RB tree uses a composite key _file reference_ && _FD number_ (`struct file *` + `int fd`)
    * composite key is done to break tie when 2 nodes have the same `struct file *`
* FD is used because epoll instance is also process speicifc (i.e. if forked(), epoll instance is duplicated & all previous FDs point to the same file references in the open file description table)

_`ep_poll_callback`_
- kernel initializes a wait-queue entry `wait_queue_entry_t` which contains a pointer to a kernel callback function named ep_poll_callback
    * this entry is placed into the socket's internal wait-queue head `sk_sleep`

=> RB tree is touched during FD registration

when data arrives on a TCP stream:
- network hardware triggers an OS interrupt
- kernel handles this by waking up socket's waitqueue
    * socket's waitqueue contains multiple callbacks `ep_poll_callback` which was was previously registered by each epoll instance
- epoll's callback function is executed
- `epitem` pushed onto epoll's ready list (`rdllist`) -> via `list_add(&epitem->rdllink, &ep->rdllist)`
- epoll_wait() drains rdllist & returns

=> RB tree is never touched during the data arrival's hotpath

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

