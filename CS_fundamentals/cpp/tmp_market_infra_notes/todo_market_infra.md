# Miscellaneous notes

TODO:
- research (Architecture, Coinbase APIs, Opimizations, Resources)
- create coinbase exchange account
- build POC => connect to exchange first (FIX's API endpoint)

DOING:
DONE:

# -------------------------------------------------------------------------------------------------
# Structure

- Orderbook class
- Feedhandler class
- WebsocketClient class
    - connect() - connect to exchange server via API url (TCP + SSL + WS)
    - send(string) - send message
    - read() - read message from socket into buffer & consumes message

* feedhandler.run()
    1. calls the websocket run(session)
    2. session (method from feedhandler that runs: ws.connect(), do_subscribe(), & do_read_loop())
        - ws.connect() - websocket connects
        - do_read_loop() - ws.read() + on_message() => read from websocket & publishes to consumers
        - do_subscribe() - iterates all registered subscriptions + writes out subscription messages via ws.write()

# -------------------------------------------------------------------------------------------------
# MACROS

all projects / learnings todo:
- _LearnCpp.com_ - RAII, move semantics, const correctness, templates basics & STL containers [current]
- _market order engine_ [current]
- _build redis clone_ - using socket knowledge, write real C++, then publish it. post it to r/cpp or #include<C++> discord asking for review
- _contribute to ClickHouse?_  => comments on design not syntax

goals/ guidelines to achieve in order market project:
- lock free data structures: lock-free ring buffer (SPSC/ MPSC queues)
- cache-aware design (false sharing + cache line alignment)
- avoid dynamic allocation in the hot path
- branch prediction
- low latency networking (kernel bypass/ raw sockets awareness)
- benchmarking (using perf, valgrind, cachegrind) => use ns level latency
    (methodology in benchmarking)
    - std::chrono or RDTSC for latency measurement (RDTSC is more precise)
    - measure percentiles, not averages - p50, p99, p99.9 => tail latency is what matters
    - warm up b4 measuring (cold cache skews everything)
    - pin threads to cores (pthread_setaffinity) when benchmarking
    - compile with -02 or -03 & state this in README

benchmark of importance:
- how fast is orderbook update (add, cancel, modify) => <500ns is respectable, <200ns is good
- lock free queue between feed handler & orderbook?? (SPSC ring buffer round trip) => <100ns
- matching engine order insert + match => <1 micro sec for toy, < 200ns for optimized

cpp specific macros:
- move semantics, RAII, const correctness, template basics, STL containers
- template metaprogramming basics
- volatile vs std::atomic vs memory fences
- constexpre, inline, compiler optimizations (-02/-03)
- when to use `unique_ptr` vs raw pointers (& why sometimes HFT uses neither)

# -------------------------------------------------------------------------------------------------
# others

orderbook project
- core orderbook + feed handler working end-to-end against real coinbase data
- clean README explaining architeture, design & latency
- basic benchmarks
- compiles cleanly & has clear build story

what to do to show understanding:
- extend orderbook with latency benchmarks
- lock-free ring buffer implementation?? => whats ring buffer & whats the use of it?? => coordinates access using atomics instead of mutexes
- matching engine => whats the difference between this & an orderbook & if my understanding is correct why is this necessary on the client side??

things worth doing that arent re-inventing the wheel:
1. data structure choice & reasoning
    - std::array of price levels with a known range instead of std::map
        => cache locality O(1) vs O(logn)
        => array wastes MEM but faster; map is flexible but pointer chasing kills cache
2. MEM layout
    - algin order structs to cache lines (alignas(64))
        => measure b4 & after with `perf state`, show the cache miss reduction
3. avoid dynamic allocation in the hot path??
    - pre-allocate an object pool for orders
    - show that removing new/ delete from the update loop drops latency
4. branch prediction???
    - annotate likely/ unlikely brnaches ([[likely]] in cpp20)
    - shows that an if/ else reorder based on message frequency improved throughput
* idrk what 3 & 4 are

possible projects to look into:
- clickhouse - open source column oriented SQL DB designed for OLAP (online analytical processing), allows generating analytical data reports in real-time
    built for modern hardware & desgined from scratch when C++20/ 23 was introduced (uses the latest features)
- MySQL - (30+ years old) => not so good as it contains complex hybrid ancient procedural C & newer object-oriented C++
- MongoDB - => not so good as its packed with deeply nested custom libraries
- folly - meta's core lib of C++ components, containing high performance alternatives to the C++ std lib
- velox - meta's C++ DB acceleration engine
- envoy project - graduate project serving as gold standard for large-scale enterprise-grade cloud native C++ architecture
- abseil - google's open source collection of core C++ lib code to augment C++ std lib
- serenityOS - systems-level programming written in modern C++
* Pull request tab, check `is:pr` `is:merged`, then `label:architecture` or `label:refactor` as those include

Books — most concrete:

Building Low Latency Applications with C++ — Sourav Ghosh. This is the closest thing to a concrete HFT system architecture walkthrough that's publicly available. Walks through feed handler, orderbook, matching engine end to end.
C++ Concurrency in Action — Anthony Williams. For the SPSC queue and atomic memory ordering specifics.
Effective Modern C++ — Scott Meyers. For the C++ specifics firms quiz on.

Papers and whitepapers:

LMAX Disruptor whitepaper — the canonical lock-free ring buffer, directly applicable to your SPSC queue
Nasdaq ITCH protocol specification (publicly available) — shows you exactly what a real L3 feed looks like at the protocol level. More concrete than Coinbase's WebSocket docs.
CME MDP 3.0 specification (publicly available) — same for futures markets

Talks:

Timur Doumler CppCon talks on lock-free programming
Martin Thompson's talks on mechanical sympathy (cache lines, SPSC queues)
Carl Cook's CppCon 2017 talk "When a Microsecond Is an Eternity" — probably the most directly relevant public HFT talk that exists

Blogs:

mechanical-sympathy.blogspot.com — Martin Thompson, core HFT infrastructure concepts
mrice32.github.io — low latency C++ patterns
crystal.globaltrading.org — one of the few blogs written by actual HFT practitioners