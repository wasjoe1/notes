# My understanding
the way aync loop executes is by having a asyncio event loop that runs on 1 thread, and this event loop runs asynchronous tasks(coroutines), switching between the tasks during I/O bound wait operations => will not execute in parallel

# My intuition as to why channels are sync-safe
the invariant is that as long as the data to be mutated is passed to the expected coroutine for usage, the race condition would not exist and hence making channels very useful

# Exact conditions for synchronization
A go channel provides 3 guarantees:
1. Happens-before synchronization
A send on a channel happens-before the corresponding receive. This is a memory ordering guarantee,

i.e. 
```GO
// 1st coroutine
x = 10
ch <- struct{}{}   // send
// next coroutine
<-ch               // receive
fmt.Println(x)     // guaranteed to see x == 10
```

2. Blocking enforces mutual exclusion
For an unbuffered channel:
Sender blocks until receiver is ready
Receiver blocks until sender is ready
This enforces synchronization at the language runtime level, even across multiple OS threads.

3. Channels move ownership, not just data
Idiomatic Go treats values sent on a channel as:
- no longer owned by the sender
- exclusively owned by the receiver
=> hence only 1 goroutine mutates the values at a time
=> ownership transfer is serialized by the channel (data+ownership becomes sequential)