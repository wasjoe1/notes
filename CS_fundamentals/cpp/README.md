# CPP

## Description
This folder contains my personal notes for any programs/ concepts related to the C++ language

__Expectation__
- predictable performance
- MEM discipline
- cache awareness

__Style guide__
Google C++ style guide: https://google.github.io/styleguide/cppguide.html
* I am following this style guide to ensure consistency, readbility & maintainability of any C++ code I will write in the future.

__C++ books__
- effective modern C++ by scott meyers
- The C++ programming language by bjarne stroustrup
- C++ concurrency in Action by Anthony williams

__Curriculum__
Foundation:
1. object lifetimes
2. RAII
3. move semantics
4. const-correctness
5. references vs pointers

Performance & memory:
1. stack vs heap
2. cache lines & false sharing
3. alignment & padding
4. branch prediction
* what every programmer should know about memory
* optimized C++ kurt guntheroth

Concurrency & lock free basics:
1. atomics
2. memory ordering
3. lock-free queues
4. contention trade-offs
* C++ concurrency in action
* benchmark p99+ & not averages???

Systems thinking(not specific to C++):
- OS scheduling
- NUMA effects
- CPU pinning
- syscall cost
* OS affects latency of processes

## Learnings so far
- compilers
- std out
- vectors (declaration, initialization, access, modification, range constructors)
- for loop (index-based, range-based)
- arrays (ptr to 1st ele, ptr to entire arr)
