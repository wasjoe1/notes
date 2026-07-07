# Market infra (quick notes)
# logging

specific to this project, i will use basic logging methods so that i dont introduce too much complexity first

```cpp
std::cin // stdin, fd=0 => buffered
std::cout // stdout, fd=1 => buffered
std::cerr // stderr, fd=2 => not buffered
std::clog // logging, fd=2 (shares the same fd as err) => buffered
```

- cout will print the actual message / order / data saved => outputs data to an FD
- cerr & clog will contain error messages & logging
- log messages will indicate what type they are `[INFO]` & `[ERROR]`

to redirect output from the process:
1. `./bin 2> bin.log` - redirect FD2 from the binary to the file bin.log
2. `./bin 2>&1 | tee bin.log` - redirect FD2 to file & terminal simultaneously
3. set & write to a file directly
    ```cpp
    std::ofstream log_file("bin.log", std::ios::app);
    log_file << "[INFO] Snapshot applied\n";
    ```
    `std::ofstream` - stands for output file stream -> file-writing equivalent of `std::cout`
    cout writes to fd=1; ofstream writes to a named file on disk (its from fstream)

## FDs & terminal display

default:
fd0 (stdin) -> keyboard
fd1 (stdout) -> terminal
fd2 (stderr) -> terminal

- stdout is fd1 by convention; fd1 doesnt always point to the terminal
    `./market_infra > output.txt` - this changes fd1 to point to output.txt
    `./market_infra 2> logs.log` - this changes fd2 to point to logs.log

so when doing `./market_infra 2>&1 | tee market_infra.log`
1. shell sets up a pipe between `market_infra` FD1 (stdout) & `tee` FD0 (stdin)
2. market_infra's FD1 writes to end of pipe
3. because `2>&1` now writes to the same file as FD1, it also writes to tee's FD0
4. tee reads its stdin & writes to both:
    - fd1 => terminal since tee's stdout wasnt redirected (if we really wanted to, we can redirect into another file)
    - file `market_infra.log`
    
    * tee is a separate process, spawned by the shall when using `|`
    * `bash./market_infra 2>&1 | tee market_infra.log | grep "ERROR\|WARN"` - redirection into another file; grep stays alive as a process reading from its stdin

# -------------------------------------------------------------------------------------------------
# types for price, quantity & timestamp

- price
    - usually int, not float
    - either tick index (int32_t / int64_t representing price/ tick_size) OR
        fixed-point int scaled by the instrument's decimal precision (cents)
    - floats are avoided because of rounding issues at high freq
    - allow negative values which matters for some products/ spreads
- quantity
    - typically int
    - almost always unsigned (uint32_t or uint64_t) since -ve qty is meaninigless
- timestamp
    - int64_t or uint64_t nanoseconds since epoch
    - give cheap, branch-free comparisons & avoids floating-point time drift

* kraken's docs state that price & qty are float but they generally dont mean IEEE 754 32-bit float
    they generally just mean "a number that may have a decimal point"
    - you should infer kraken's matching engine's precision by looking at the data itself
    - time is given as string, so just convert that to epoch

coding jesus's book:
```cpp
using Price = std::int32_t;
using Quantity = std::uint32_t; // modelling whoe-share equity trading (textbook style) => no fractional shares
using OrderId = std::uint64_t;
using OrderIds = std::vector<OrderId>;
```

- max number 32 bit system can produce is: `4 294 967 295`
- max price of bitcoin is `126,210.5`
    given 8 dp, `126,210.50000000`
    `12 621 050 000 000` => 2^32 bits cant hold this value, generally i will use int64_t for now
- crypto supports fractional shares (e.g. shows up to 8dps)
- crypto assets first started in 2009 (bitcoin genesis block) but Time should still be signed to allow for -ve delta
    so, justification is not for epoch range

my version:
```cpp
using Price = std::int64_t;
using Quantity = std::int64_t;
using OrderId = std::uint64_t;
using OrderIds = std::vector<OrderId>;
```

order id? int or string?
- coding jesus's int is an internal counter which he fully controls; cheap, fast to increment, great for hash maps (fastest key)
- string helps to keep original reference to the exchange when you need to modify certain orders

when building a feed handler/ client, right pattern is to:
- keep the exchange's order ID as a std::string so that u can reference it back when needed (cancels, modifies, fills)
- for fast internal lookups, map the string to the internal int id & use the int internally for matching /sorting/ cache-friendly storage
    * i will jsut use string first as a beginner

# -------------------------------------------------------------------------------------------------
# orderbook terminology

order side: bids & asks
order type: limit order, market order, stop order, ice berg order, post-only, fill-or-kill, etc. 
    (generally implementations is for limit orders)

event type: add / delete / modify

orderbook condition to fill orders: highest bid >= lowest ask
spread: highest bid - lowest ask
market depth: highest ask - lowest bid [price width measure]
"depth" - quantity/ size sitting at each price level
"deep book" - alot of resting size near the best price; has low slippage
"low slippage" - large order can execute without moving the price much
"thin book" - means size drops fast upon order; a moderate-sized order will walk through several price lvls & get a worse avg fill price

# -------------------------------------------------------------------------------------------------
# kraken API market data

snapshot:
- channel <string>; value: "level3"
- type <string>; value: "update" / "snapshot"
- data: <object[]>
    - symbol : "BTC/USD",
    - checksum : 3122590738,
    - timestamp : "2026-06-29T22:19:08.950669938Z", => the time this MD msg was generated in the matching engine (shoudl be later than the orders timestamps)
    - bids: <object[]>
    - asks: <object[]>
        - "order_id": "OQ2NK2-UZKWW-REU7OZ",
        - "limit_price": 60359.1,
        - "order_qty": 0.076,
        - "timestamp": "2026-06-29T22:19:08.265293398Z" => the time the order was inserted or amended

kraken's depth field (subscribe):
- number of price levels to be received
- if filled in `depth=10`, get top 10 bid & ask levels, each with price & aggregate size

updates:
- is streamed following the initial snapshot, no sequencing required
- L3 channel is not throttled, & updates are provided in real time
- if price level is removed from the subscribed levels (i.e. result of trades or cancels) then all orders in the next available level will _generate an add event_

to maintain book:
- after each update, the book should be truncated to your subscribed depth
- there will be no `delete` event for price levels that fall out of scope
    i.e. if u are subscribed with `depth=10` & an insert into the book results in 11 bids, you must remove the 11th worst bid => smallest on bid side, largest on ask size

notes:
- time drift in modify message - i suspect its due to modify ops takes longer, so the timestamp marks the start of that op, then the message was actually created when it was done modifying

# -------------------------------------------------------------------------------------------------
# validating orderbook

3 standard techniques (used in combination):
1. checksum validation - some L2/ L3 feed handlers sends checksum for each order event which you can check against
2. cross-referencing against independent source of truth
    => compare locally built book against other representations of the same market state (hit REST snapshot endpoint & see if they agree)
3. invariant / property-based assertions on book state
    => doesnt require external data
    => its rules that the book must always obey (i.e. best_bid >= best_ask)

# -------------------------------------------------------------------------------------------------
# to store rest_client_?

context:
- HTTP client is of stream type `beast::ssl_stream<beast::tcp_stream>` => basically a TCP connection with TLS encryption
- each tcp+tls stream is unique & we should split websocket's & http's client streams
- stream{executor_, ssl_ctx_} only takes in the executor & ssl context
    - the ssl context can be shared between the clients
    - the executor should be passed in, where the KrakenFeedHandler should OWN ITS OWN EXECUTOR
- because HTTP requests only happens when subscribe message needs to be sent,
    i am thinking whether we need to persist a rest_client_ in the feedhandler object (just like for ws_client_)?

## executor: pass by value or pass by reference

pass by value

- asio::any_io_executor is small & cheap to cpy
- type-erased handle? similar to std;:shared_ptr where there's an internal reference counting to keep underlying execution context alive
- not passing a heavy object by reference to avoid a copy; each copy just increases internal reference count
- underlying `io_context` is the shared thing
- by using reference, it adds lifetime constraint => referenced object must outlive its use

## ssl_context: pass by value or pass by reference

pass by reference

- ssl::context is heavier; stateful object holding CA certificates, verification settings, cipher ocnfigs etc.
- not cheap to copy
- multiple connections should share 1

# -------------------------------------------------------------------------------------------------
# boost::beast::http vs libcurl vs cpr

`libcurl` - underlying C engine (cpr is built on top of this)
`cpr` - c++ wrapper around libcurl; provides requests-style API (i.e. cpr::Get(cpr::url{...})) instead of libcurl's raw C interface
`Boost.Beast HTTP` - built on top of Boost.Asio

both libcurl & cpr are _blocking_
- cpr::async::GetAsync(...) doesnt make it non-blocking => just hands you back std::future & runs the blocking call on a separate std::async/ thread pool
    - std::future is a handle that eventually holds return value or an exception + the synchronization needed for .get()/ .wait()
    - std::async runs the function asynchronously in a separate thread & returns the std::future
    - dispatches work on worker threads where c++ doesnt specify whether that thread is freshly spawned or pulled from a pool => resulting in thread explosion
- requires extra OS threads, no integration with `io_context` & no way to co_await the coroutines

## blocking in non-blocking / async code?

- mixing blocking HTTP lib into an async codebase is a known anti-pattern => called out in the `Boost.Asio` docs
- introduces architecturally incompatible HTTP stack (libcurl/ cpr's blocking model) introduces unnecessary complexity
- no integration with io_context, no way to co_await
- introduces extra OS threads (further worsens performance since we pinned the thread; async io context's execution waits on this blocking thread call)
    - its not that the current execution will be faster
    - its that the thread cant do anything else due to blocking call
    - beast's await call lets the thread do something else while waiting for the network GET to be done
    FOR EXAMPLE
    given that there is 1 thread pinned for 1 feed handler
        - if u used beast (coroutine frames), the non-blocking GET call can continue executing other coroutine while waiting for this GET call, like continue to `read()` for other products
        - if u used cpr/ libcurl (std::async), the blocking GET call then becomes a real latency spike, this thread cant go & service any other things

# -------------------------------------------------------------------------------------------------
# activating NRVO for std::string types

```cpp
// WRONG example i was trying to achieve NRVO with:
asio::awaitable<const std::string&> read() { // WRONG: return by reference
    co_await ws_.async_read(buffer_, asio::use_awaitable);
    auto msg = beast::buffers_to_string(buffer_.data());
    buffer_.consume(buffer_.size());
    co_return msg;
}

asio::awaitable<void> caller() {
  std::string msg = co_await read();
  // do something with msg
}
// --------------------------------
// CORRECT example to achieve NRVO:
asio::awaitable<std::string> read() { // co_return std::string by value
    co_await ws_.async_read(buffer_, asio::use_awaitable);
    auto msg = beast::buffers_to_string(buffer_.data());
    buffer_.consume(buffer_.size());
    co_return msg;
}

asio::awaitable<void> caller() {
  std::string msg = co_await read();
  // do something with msg
  // msg string was safely moved out of the completed coroutine's frame
}
```

- note: `buffers_to_string_` returns std::string by value
    => copies buffer's bytes into a freshly-constructed object
    => msg owns its own MEM for the string
- stack-frame NRVO is not invoked here though!!
- actual mechanism uses coroutine's local state => not on the call stack
    - coroutine's state (coroutine frame) is allocated separately on the heap
    - it persists across suspension points & is destroyed when the corotuine completes OR result has been retrieved
- `co_return msg;`
    - this calls `promis.return_value()` under the hood
    - it moves msg into MEM owned by the promise obj (promise obj lives inside this coroutine frame)
- when caller calls `co_await read()`
    - awaiter's `await_resume` pulls that stored value (move operation) out from the promise's MEM
    - basically: string pointer is taken over by the caller's `msg` variable, removed from the callee's `msg` variable via the `promise`'s storage
    * 2 move is done, `co_return msg` move constructs from the local msg into the promise's internal MEM => msg treated as an rvalue
        `co_await read()` move constructs again via `await_resume()` out of the promise's storage into the caller's desination variable

# -------------------------------------------------------------------------------------------------
# co_await resolver.async_resolve(...)

i.e. `auto results = co_await resolver.async_resolve(api_url_, "443", asio::use_awaitable);`

`auto async_resolve(..., ResolveToken&& token = default_completion_token_t<executor_type>())`
- token follows asio's "completion token" pattern
- return type changes depending on the token passed as the last arg
    - callback `[](error_code ec, results_type r) {...}` => returns `void` - results delivered to your cb
    - `asio::use_future` => returns `std::future<results_type>`
    - `asio::use_awaitable` => returns `asio::awaitable<results_type>` - usable with `co_await`
    - `yield_context`

## `asio::use_awaitable`

- is a tag type passed as the completion token
- when asio sees it:
    1. suspends the coroutine at the co_await point
    2. registers a completion handler that when the resolve finishes, resume your coroutine
    3. takes the error code from the completion signature & throws a `boost::system::system_error` if its non-0
    4. takes whatever's left in the completion signature (results_type) & it becomes the value of the co_await expression
    5. thus, `co_await resolver.async_resolve(...)` -> evaluates to a <results_type> & throws on error

## DNS resolution (results = co_await resolver.async_resolve(...))

- can return multiple IPs for 1 hostname
- thus `results` is a range of results rather than a single endpoint
- each entry has `.endpoint()` (IP address + port), `.host_name()`, `.service_name()`

## co_spawn & use_awaitable

- when the completion token is `use_awaitable`, `co_spawn` doesnt immediately schedule the coroutine `start()` to start running
- it returns an `asio::awaitable<T>` representing a deferred operation
    => spawned coroutine on an executor doesnt begin executing until something `co_await`s the returned awaitable
- to consume that awaitable, you'd need to either:
    1. co_await the coroutine `co_await asio::co_spawn(ioc, start(), asio::use_awaitable);`
        => co_await only works inside a coroutine
    2. run the ioc `ioc.run();`

why doesnt the error throw when `ioc.run()` encounters an error? when using `asio::use_awaitable`

- start() awaitable was scheduled onto the executor during co_spawn
- ioc.run() then starts running these coroutines in the event queue
- `use_awaitable` mechanism
    - captures the exception into an `exception_ptr`
    - store it on the result handle (the awaitable<void> that co_spawn returns to you)
    - then rethrow it only when something `co_await`s that handle
    - if nth `co_await`s that handle, the exception just sits in that handle's internal state & gets dropped
- `ioc.run()` doesnt reach into every spawned coroutine's result state & rethrow on your behalf
    - it only throws an exception if the exception escapes the handler & is invoked as part of the queue execution
- why `rethrow()` lambda expr works?
    - rethrow isnt a "result handle to be awaited later" (unlike `asio::use_awaitable`)
    - its the completion handler
    - when start() finishes, asio invokes rethrow directly as part of processing the io_context's handler queue inside run*()

* basically the lambda expr getes called at the end by asio as a callback, whereas the
awaitable token was returned before during `co_spawn`

so unless you did:
```cpp
// assuming your inside a coroutine's body
auto handle = asio::co_spawn(ioc, start(), asio::use_awaitable);
co_await handle; // error is thrown here
```
but the issue is that:
1. in main, you cant use co_await in a non-coroutine body
2. even then you cant do `ioc.run()` & access `handle.exception` because `co_await handle;` just calls `await_resume()` under the hood
    & there is no more execution left after `ioc.run()`

# -------------------------------------------------------------------------------------------------
# threads

std::thread is the modern way (introduced in c++11) which wraps around `POSIX threads; pthread` on linux/ macOS
& `windows threads` on windows

```cpp
// c++ std way
#include <thread>
void worker_func(int id, const std::string& symbol) {...}
std::string ticker = "BTC/USD"
std::thread cpp_thread(worker_func, 42, ticker) // create & launch thread, passes 42 as the arguments

// c way: pthreads (for linux)

```

# -------------------------------------------------------------------------------------------------
# move constructor & silent deletion of copy constructor

c++11 rule in _resource owning types_
if a class declares a move constructor (or move assignment operator), the compiler will not implicitly generate a copy constructor for it
instead, the implicit copy constructor is defined as _deleted_

## declaring a deleted constructor

```cpp
// e.g. of deleted copy constructor
context(const context&) = delete;
```

## deleted vs doesnt exist

deleted & doesnt exist dont mean the same thing

- ClassName(const context&) {}; // copy constructor -> binds to lvalues (lvalues & rvalues, const & non-const)
- ClassName(context&&) {}; // move constructor -> binds to rvalues only

* if copy constructor is deleted, you can only pass in rvalues. the bottom will not work:

```cpp
WebsocketClient(const std::string& api_url, ssl::context& ssl_context, asio::any_io_executor ex)
    : ssl_context_{ssl_context}   // <-- ssl_context here is an lvalue
```

* need to explicitly convert lvalue to rvalue

```cpp
WebsocketClient(const std::string& api_url, ssl::context& ssl_context, asio::any_io_executor ex)
    : ssl_context_{std::move(ssl_context)}   // std::move(ssl_context) returns an rvalue
```

## binding a reference type variable

this means to create an alias for an existing object
* no construction is called

i.e.
`ssl::context& ssl_context_1{ssl_context_2};` is just binding a reference type variable to an existing object

# -------------------------------------------------------------------------------------------------
# boost/beast/core

`boost/beast/core` - is a convenience umbrella header that pulls in all of `boost/beast/core/*`

* should pull in each of those self-contained headers

# -------------------------------------------------------------------------------------------------
# asio::any_io_executor, asio::io_context::executor_type & strand<...>

`asio::any_io_executor` is a type eased wrapper where it can hold raw `io_context::executor_type` & `strand<...>`


# -------------------------------------------------------------------------------------------------
# global scope

- In C++, the global scope is reserved for declarations and definitions
- cannot write standalone "procedural" instructions.

# -------------------------------------------------------------------------------------------------
# environment variable table

environment variable table - is a POSIX-level concept

when setting global env variables, you are essentially adding key-value pairs into this env variable table
- c++: `dotenv::load(env_path);`
- bash: `export key=value`

* variables can be used in the current & child processes

# -------------------------------------------------------------------------------------------------
# POSIX

misconceptions:
its the interface between the actual OS implementation and hardware?
its a guideline to building OSes?
NO

POSIX - is a standard defined by the IEEE computer society to ensure SW compatibility between different OS
    => it ensures app level software that calls different key components get the same behavior no matter the OS (OS that follows POSIX standards)
    => it sits between the OS kernel & app software

# -------------------------------------------------------------------------------------------------
there are these 3 different ssl headers, whats the difference?

- #include <boost/beast/ssl.hpp>
- #include <boost/beast/websocket/ssl.hpp>
- #include <boost/asio/ssl/context.hpp>

## #include <boost/asio/ssl/context.hpp>

layer: transport layer (TCP/ TLS)
purpose: manage baseline OpenSSL configs & credentials
function: configure TLS certs, private keys, & verification modes
usage: used to initialize security settings b4 making any connections

## #include <boost/beast/ssl.hpp>

layer: app layer (HTTPS)
purpose: provide stream wrapper to pass standard HTTP traffic over TLS
function: combines standard boost.adio TCP sockets with SSL context
usage: used when building HTTPS client / server to send HTTP reqs

## #include <boost/beast/websocket/ssl.hpp>

layer: app layer (WSS)
purpose: provide stream wrapper to pass 2 way WS traffic over TLS
function: wraps websocket protocol layer around `boost::beast::ssl`
usage: used when building low latency ws communications

# -------------------------------------------------------------------------------------------------
# overloading operator functions

there are 2 ways to overload operator functions
1. free function - add support for new data types without touching the original ostream class
2. member function - created for builtin types; since builtin types never change (hence built directly into the std::ostream class defn)

```cpp
namespace std {
  class ostream {
  public:
    // 2. member function
    ostream& operator<< (int val);
    ostream& operator<< (double val);
  }
  // 1. free function
  ostream& operator<<(ostream& os, const char* s);
}
```

# -------------------------------------------------------------------------------------------------
# array syntax

```cpp
int main(int argc, char* argv[]) {...}
```

int arr[5] - this means array of 5 ints
int* arr_ptrs[5] - this means array of 5 int pointers
int (*ptr)[5]

* note that putting * next to a variable name decalres that its a pointer
    BUT compiler reads types using operator precedence & square brackets [] have higher priority than asterisk *
    - hence int* ptr => makes ptr a pointer, where address holds an int
    - int (*ptr)[5] => makes ptr a pointer, where address holds an int array
    - int *ptr[5] => [] makes ptr an array, where array holds elements of type int pointers
    - int **ptr[5] => [] makes ptr an array, where array holds elements of type int pointers to pointers

- why does the array parameter in functions not need to take in a fixed amount of elements?
    => in c++, whenever an array is passed into a function, it auto decays into a pointer to its first element
i.e. `int sum_array(int numbers[])`
compiler decays it to: `int sum_array(int* numbers)`
the effect?
- the function doesnt know the size => need to pass the size of the array in as well
    `int sum_array(int numbers[], int size) {...}`

# -------------------------------------------------------------------------------------------------
# kraken connection

- tried to connect to L3 order API using coinbase exchange API
- Exchange APIs however only allowed institutional investors to register & get API keys
- hence i found kraken API (kraken's exchange servers) which are open to public retail traders

## subscibe process

- get API key & API private key (via create API on their website)
- POST a auth token via auth URL endpoint
    - generate HMAC signature using urlpath, nonce, & api private kay / api secret
    - header: place api_key & genereate HMAC in header as API-Key & API-Sign respectively
    - body: data contains nonce
    - res: token
- WS subscribe message
    - method: subscribe
    - params:
        channel: level3
        symbol: "BTC/USD"
    - snapshot: true
    -token: token (previously generated)
- data should start streaming in: json.loads(raw)

# -------------------------------------------------------------------------------------------------
# thread pinning

thread pinning during testing / production - means to pin a thread to a specific core (dont allow the OS to move your thread to different cores)

1. eliminate OS thread context switch ⇒ moving thread from 1 core to another requires saving state of registers from 1 core and loading them into registers of the other core before resuming execution
2. maximize L1/ L2 cache hits ⇒ every core has their own ultra fast L1/ L2 cache and if you change core, core 2’s cache is empty (cold) requiring code to pull data from slow main RAM (random access memory that is situated on the mother board still but outside of the chip)

* note that every core has its own physical set of registers
* in hyper-threading, each logical thread within that core even has its own dedicated registers (advanced)

## CPU affinity

setting CPU affinity(aka CPU pinning) is the process of binding a SW program to run on a designated processor core, preventing OS from moving it around

thread pinning is just a specific application of CPU affinity but there are other ways to manage affinity at different levels of execution

- thread pinning (most granular)
- process affinity (standard level)
- interrupt affinity (HW level)

* affinity - strong liking for something

## thread pin code (linux)

```cpp
void pin_thread_to_core(int core_id) {
    // pins the thread first during thread creation (before running anything)
    // C++ does not expose a portable affinity API -> normal thread operations like create, join, detach etc. are standardized
        // whereas CPU affinity is not BECOZ, CPU affinity is a OS scheduling concept & different OSes expose different mechanisms for it
        // linux uses pthread_setaffinity_np
        // windows uses SetThreadAffinityMask
        // macos odesnt really support hard affinity the same way
        // portable => 1 API, same call across all platforms
    cpu_set_t cpuset; // is a bit mask in MEM, 1 bit per logical CPU on the system
    CPU_ZERO(&cpuset); // clears every bit to 0 => no core selected
    CPU_SET(core_id, &cpuset); // sets bit number of `core_id` to 1 in that bitmask (only that core is allowed)

    pthread_t current_thread = pthread_self(); // returns a handle (pthread_t) => the current thread executing this right now
    // pthread_t is a handle for a kernel-scheduled thread of execution
    int rc = pthread_setaffinity_np(current_thread, sizeof(cpu_set_t), &cpuset); // actual syscall-backed step, which tells the OS that this thread is only allowed to run on the cores that have been marked in this bitmask
    if (rc != 0) {
        throw std::runtime_error("Failed to set thread affinity: " + std::to_string(rc));
    }
}
```

- `pthread_setaffinity_np` is specific to linux platforms & compilation can only be done on linux; build process will fail on mac & windows
    - on ubuntu (clang++ or g++), my cpp code is linking against glibc where the symbol `pthread_setaffinity_np` exists
    - on mac (clang++), is compiling against apple's libsystem/ libc not glibc, hence `pthread_setaffinity_np` doesnt exist
    * pure c++ code needs a C lib underneath because C++ standard lib (i.e. new/ delete std::vector etc.) is built on top of the C standard lib itself like malloc, printf etc.

# -------------------------------------------------------------------------------------------------
# coroutines, strands, io_context & threads

coroutines, strands, io_context & threads
    // co_spawn is the thing that actually creates separate coroutines to be run => potentially in parallel
    // multiple coroutines can co_spawn on a single executor, and executing that executor with multiple threads will allow coroutines to run in parallel
    // ex1 = get_executor() returns the raw executor & coroutines submitted to io_context's is queued onto its internal ready-queue with no extra constraint
    // [strand], however, is a wrapper around ex1, submit through strand, put on the same queue, but now has constraints
    // you can co_spawn multiple co_routines on the same strand but that means that a unit of work can only occur for this collection of coroutines when no other coroutine from this strand is running
    // this means 
    // i.e. you could have 1 strand for coinbase => coinbase has orderbook coroutine, DB coroutine, sockets coroutine => and they should never run tgt
        // by putting all these coroutines on the same strand, they can interleave but never execute at the same time
        // if we are given multiple threads, if A in strad1 is still running on thread 1, B in strand1 cant run even if thread 2 is ready

    // multiple strands can take advantage of multiple threads
    // but you cant pin a strand to a specific thread (strands are a scheduling/ exclusivity construct not some that the OS knows)
    and its designed such that any thread can come & pick it up
    // if 1 strand is more busy while the others are all idle, more threads will begin servicing the strand1
    // HOWEVER, this doesnt mean strand1 starts working in parallel => remember, 1 strand can only work in sequence due to it executing 1 handler at a time
    // the benefit comes from switching to another thread to continue execution when 1 thread gets busy (i.e. you pinned thread1 to core1, and this thread1 was later used by another function after the coroutine gives up execution, then this current coroutine with thread2 and thread3 and decide to use thread2 to continue executing)
    // it benefits not because of parallelism but because it now has more resources which its allowed to use to execute (less waiting for resumption between steps)

# -------------------------------------------------------------------------------------------------
# stackful coroutines vs stackless coroutines

What you described—storing specific pieces of a frame—is actually how C++20 stackless coroutines work!
C++20 (Stackless): The compiler looks at your function, finds your local variables, and creates a tiny custom object on the heap just to hold those variables.
It does not create a real stack.
This is why C++20 cannot yield from inside a nested function like helper(); it doesn't have a real stack to track the nesting.

Boost (Stackful): Allocates a real, full-sized memory stack (on the heap).
It can nest functions as deeply as regular C++ because it uses standard CPU stack mechanisms,
just shifted to a private block of memory (private block of MEM is on the heap).

* note:
    - both can pause & resume the coroutine execution (thats the adv of having async code)
    - main diffference is that stackful coroutine can execute a nested function & yield all the way out to the nested function because it has a stack
        vs stackless coroutines cant call an inner function & yield all the way out

## stackful coroutines mechanism

- Saves the callee-saved registers (rbx, rbp, r12–r15 on x86-64) plus the current rsp onto the coroutine's own stack
- Loads rsp to point at a completely different stack — wherever the io_context's resumption point left off
- Restores that other context's saved registers
- Jumps

where it lives: separate mmap'd region => `mmap` (or custom allocator supplied)
* same region as thread's stack but usually done by the OS/ pthreads at thread execution
* hence not part of the same MEM & encounters alot of TLB miss/ page fault + cache-cold jump

* this is similar to a thread context switch where registers swap out actual data between different stack regions
    just minus the trip through the kernel, no syscall, no schduler, no privilege change
    => its called "user-space context switch" or fiber switch

## stackless coroutines mechanism

- no second stack
- at compile time, compiler looks at coroutine & figures out where each locals are alive across each `co_await` point
- those locals get stored in heap-allocated coroutine frame
- just a jump-table dispatch to the right line at each coroutine function call during `handle.resume()`

where it lives: Heap => `operator new`

* even lighter weight "context switch" => no rsp pivot, no manual register-file save/ restore, no second region to warm up
    really just uses the heap MEM of the current control block's MEM & jumps to different memory addresses to continue execution
* rsp pivot - stack pointer register gets repointed to a different stack
    on x86-64, rsp(stack pointer) is a CPU register that holds the MEM address of "the top of the current stack"
    `mmap`'d stack are different for different coroutines
    hence `jump_fcontext` runs & yanks the stack pointer sideways to point to an entirely different MEM region

## more elaboration

First, correcting the "stack vs heap" framing slightly:
Stackful coroutines: everything about that coroutine — its call frames, locals, the works — lives on its own dedicated mmap'd stack region, for the entire time it runs. Every local variable, every nested function call inside it, all of it is stack memory, same as normal code, just on a different physical stack than the thread that spawned it.
Stackless (C++20) coroutines: most of the coroutine's execution is on the ordinary thread stack, exactly like a regular function call. The heap allocation only happens once — for the coroutine frame, which holds just the subset of locals that are alive across a co_await point. Code between suspension points runs on the normal stack like anything else. So it's not "stackless coroutines live on the heap" — it's "stackless coroutines store their across-suspension state on the heap, and otherwise behave like normal stack-based code."
Now, the actual cost — it's two independent things, not one:
1. Mechanism cost (exists regardless of locality)
Stackful: every single switch unconditionally saves/restores the full callee-saved register set (~8-14 registers), because jump_fcontext has no idea what your code actually needs — it's a generic assembly routine, compiled once, used for every coroutine.
Stackless: the compiler generated your specific coroutine's resume logic with full knowledge of exactly which 2 or 3 variables survive across that particular co_await. It spills only those — sometimes nothing. Resuming is a plain indirect call, no register-file shuffle at all.
So even with infinite cache, hot everything, zero memory-locality penalty — stackful still does strictly more work per switch, because it's a generic mechanism vs. a compiler-tailored one.
2. Locality cost (the part you picked up on)
This is the separate, often larger effect: stackful jumps to a physically isolated chunk of address space (the other stack) that may be cold — TLB miss, page fault on first touch, cold cache line. Stackless stays near the heap's general allocation traffic, which tends to already be warm from normal program activity.
So to directly answer you: locality is one of the two reasons, not the whole reason. Even in a hypothetical world where both stacks were equally warm in cache, stackful would still be doing more work per switch — it's paying a fixed "I don't know what you need, so I'll save everything" tax that stackless coroutines simply don't have, because the compiler already did that analysis for them at compile time. Locality then stacks an additional, data-dependent penalty on top of that fixed cost.

what is a mmap'd stack region?
why is the heap allocation for stackless coroutines only happen once? doesnt it need to keep accessing the heap everytime? or is it that once its allocated, you always have that address stored in your local context and its easy to jump to? but i thought that in itself is expensive to do

5:01 AM

Disentangled allocation versus access costs in coroutine memory management
Disentangled allocation versus access costs in coroutine memory management
Two separate things to unpack — let's take them one at a time.

What "mmap'd" means

mmap is a system call — your program asks the OS kernel for a chunk of virtual address space. Normally your process's memory comes from two main sources: the heap (managed by malloc/new, which itself got its underlying memory from the OS via brk or mmap calls made earlier and now just hands out pieces of it), and the stack (set up by the OS/runtime when a thread is created).

When Boost.Context creates a stackful coroutine, it explicitly calls mmap again, asking for a brand-new, separate region — typically with flags like MAP_PRIVATE | MAP_ANONYMOUS, meaning "give me memory not backed by any file, just zeroed pages" — and often a guard page at one end (a page deliberately marked non-accessible, so if the coroutine's stack overflows into it, you get an immediate, loud segfault instead of silently corrupting whatever memory happened to be next door). That region becomes the coroutine's entire stack — every local variable and call frame inside that coroutine lives there, completely separate from the thread's normal stack and separate from the heap.

One more detail relevant to the "expensive" theme: the OS doesn't actually back those pages with physical RAM at mmap time — it just reserves the address range. Physical pages get assigned lazily, on first touch (a page fault the kernel handles transparently). That's part of why a freshly spawned stackful coroutine's first jump tends to be relatively more expensive than later jumps to the same stack — the early touches are triggering real page faults, not just cache misses.

Why the heap allocation only happens once — this is the key thing to untangle

You're right that the coroutine's heap-allocated frame gets accessed every time it resumes. But accessing memory you already have the address to is a completely different — and much cheaper — operation than allocating memory.

Allocating (operator new / malloc) means asking the allocator to find you a free block: walk free lists, maybe split a chunk, maybe ask the OS for more pages if the arena's exhausted, update bookkeeping metadata. This is genuinely nontrivial work — tens to hundreds of nanoseconds, sometimes more.
Accessing memory you already have a pointer to is just: read or write at that address. Same cost as touching any field of any heap-allocated object you've ever used — a std::vector's backing array, a member of a std::unique_ptr<Foo>, anything. It's a load/store instruction, full stop.
Here's the actual sequence for a C++20 coroutine:

First call — the compiler-generated code runs operator new once, gets back an address, stores it inside a coroutine_handle (which is, underneath, just a raw pointer — 8 bytes).
Every subsequent resume — you (or the executor) call handle.resume(). That's a function call through a stored pointer to the frame, which internally just jumps to whatever line index was saved as "where I suspended" and continues executing — reading/writing the frame's contents exactly like reading/writing any other heap object's fields.
So nothing re-allocates on each resume. The frame was carved out of the heap once, and every resume just reuses that same address.

On your last worry — "isn't jumping to a stored address itself expensive?"

No, and this is the crux of the whole comparison. An indirect call/jump through a stored pointer — handle.resume(), calling a std::function, calling a virtual method, calling through any function pointer — is one of the most ordinary, cheap operations a CPU does. It's a single indirect-jump instruction; modern CPUs even have branch predictors specifically for indirect jumps that get quite good at predicting the target if it's called repeatedly from the same site. That's nowhere near the same category of cost as jump_fcontext's switch, which isn't one jump — it's saving 8-14 registers, overwriting rsp to point at a different memory region entirely, then restoring 8-14 registers, then jumping.

So the asymmetry you were sensing is real, just attached to the wrong cause. It's not "heap access is cheap because the address is stored" — accessing through a stored address is cheap regardless of whether the memory is heap or stack. The actual asymmetry is: stackless resume = one indirect jump to memory you already own and have likely touched before; stackful switch = full register save/restore plus a pivot to a different memory region that may need fresh page faults the first few times you touch it.

## overall

the jump to the address for continued execution `handle.resume()`
is cheaper than saving & restoring 8-14 registers, then jumping in `jump_fcontext`

# -------------------------------------------------------------------------------------------------
# lambda expressions (lambda functions)

`auto func = [...](...) mutable/noexcept -> T {...}`

1. [...] - capture clause; specifies which variables from the surrounding scope are available inside the lamdba
    - [] - captures nothing
    - [&] capture all local variables by reference
    - [=] capture all local variables by value (copy)
    - [x, &y] capture x by value & y by reference
2. (...) - parameter clause; parameter list for lambda function
3. mutable/ noexcept - (optional) specifiers; by default is non-mutable & can throw exceptions
    - mutable => allows you to mutate the captured variables (includes variables that you passed in as values)
    - noexcept => requires you to catch any error raised inside the lambda, else program immediately stops at the lambda function & doesnt do stack unwinding to find the next closest catch statement
4. -> T     - return type of lambda function; optional becoz compiler can deduce type via return statement
5. {...}    - function body

## examples

```cpp
// Capture clause [...] - by value or reference
int multiplier = 3;
// captured by value (makes a copy of multiplier at this moment)
auto multiply_copy = [multiplier](int x) { return x * multiplier; };
// captured by reference (reflects changes to multiplier)
auto multiply_ref = [&multiplier](int x) { return x * multiplier; };
multiplier = 5; 
multiply_copy(2) // still uses 3 -> returns 6
multiply_ref(2) // uses the updated 5 -> returns 10

// Specifiers (mutate)
int count = 0;
// Without 'mutable', 'count++' would throw a compiler error
auto incrementor = [count]() mutable {
    count++; // increments the same count that was copied; doesnt increment the outer count => think of this as a HiddenLambda class that stores a member variable for each captured variable
    std::cout << count << std::endl;
};
incrementor(); // prints 1
incrementor(); // prints 2
incrementor(); // prints 3
cout << count; // prints 0

// Explicitly stating return type
auto add = [](int a, int b) -> int {
    return a + b;
};

```

## important points

* type of lambda expressions are unnamed & unique; they are called anonymous closure type
* even if 2 lambdas look identical, they have different types; becoz type has no name in the src code => cant type it out explicitly (anonymous closure type)
* becuase type is unnamed, must use `auto` to deduce the unnamed type automatically

# -------------------------------------------------------------------------------------------------
# asio::co_spawn

asio::co_spawn(boost::asio::io_context ioc, net::awaitable<void> awaitable, boost::asio::detached_t net::detached/token)

boost::asio::io_context ioc - event loop driver; engine that will execute the allocated coroutines upon run()
boost::asio::awaitable<void> awaitable - cou=routine to be allocated on to the event loop
boost::asio::detached_t net::detached/token - token that defines the lifecycle & error handling strategy

what it does:
- allocates coroutine frame => reserves MEM for coroutine state, local variables, & execution points?
- attaches the coroutine to the io_context (event loop driver)
- schedules execution => queues coroutine's initial entry step into io_context's queue

# -------------------------------------------------------------------------------------------------
# Boost::asio & Boost::beast

- Boost::asio - library for async tasks in C++
- Boost::beast - lib for web-based networking (hTTP & websocket protocols)

# -------------------------------------------------------------------------------------------------
# async & coroutines in c++ 20

- creating async function: async def do_something() == net::awaitable<T> do_something()
- await a coroutine's execution: await == co_wait
- execute a coroutine with a specified executor (ioc being the executor in this case): asyncio.run(main()) == net::co_spawn(ioc, run(), net::detached) + ioc.run()

* execution only starts when you call `ioc.run`, `net::co_spawn(...)` schedules the coroutines

# -------------------------------------------------------------------------------------------------
# system design (feedhandler & websocket)

- want to keep `FeedHandler` class decoupled from `WebsocketClient` class
    => create 2 different classes
- should i instantiate WebsocketClient separately from FeedHandler? (dependency injection [Aggregation]) OR [Composition]
    [Aggregation] - has-A relationship i.e. Department has a professor, but when the department is "deleted" the professor could still exist
    [Composition] - part-of relationship; sub object cant exist without the parent i.e. a room is part of the house
    => in the current scenario, the feedhandler should be a 1:1 r/s
    => feedhandler uses a websocket but doesnt control its life time [aggregation]
- generally,
    - we instantiate `WebsocketClient` separate from the feedhandler class & pass it in as an argument
    - better decoupling
    - allows the websockClient maintain its own state: maintain its own pool of connections, retries etc.
    - feedhandler doesnt need to know the socket's configs
    - easier testing
- lifetime
    - feedhandler only holds a reference/ pointer to a websoekt, it didnt create & doesnt destroy
    - websocket can outlive the feed handler

    inject by?
    - reference - websocket must outlive feed handler   => because someone else holds the true reference
    - shared_ptr - ownership is shared which adds atomics overhead? => everyone holds a a ptr; u may or may not be the last one (need to increase / decrease counter)
    - unique_ptr - feed handler takes ownership => ownership passed directly to you (no difference from just instantiating it within the feedhandler class)

# -------------------------------------------------------------------------------------------------
# vcpkg git baseline

- acts as the strict ceiling
- when operating in manifest mode, vcpkg requires a strict defined baseline commit => else it will throw a fatal compilation error
- generally for small projects where all the packages are lined up, we just use a `builtin-baseline` in `vcpkg.json` without needing a separate `vcpkg-configuration.json`
```json
{
  "name": "my-json-project",
  "version-string": "1.0.0",
  "builtin-baseline": "3df3411b0e9f69742a78fa8cb27db4ff3c9cb597",
  "dependencies": [
    "nlohmann-json"
  ]
}
```

- the reason we have `vcpkg-configuration.json` is to accomodate larger projects where we have older versions for specific packages
```json
{
  "registries": [
    {
      "kind": "git",
      "repository": "https://github.com",
      "baseline": "deadbeef1234567890abcdef...",
      "packages": [ "internal-logger", "proprietary-crypto" ]
    }
  ]
}
```

* to get the latest commit of the vcpkg:
    - in terminal cli, use: `git ls-remote https://github.com/microsoft/vcpkg.git refs/heads/master`
    - or when in directory with `vcpkg.json` or `vcpkg-configuration.json` use: `vcpkg x-update-baseline --add-initial-baseline`

* `vcpkg x-update-baseline --add-initial-baseline`
    - works by checking ur local git clone vcpk repo (the one pointed to in my `VCPKG_ROOT`)
    - "builtin-baseline": "58950f88544e4637524dbd6a01d0317cf4cb77fc" // this is for a 2024 commit

# -------------------------------------------------------------------------------------------------
# json manipulation & json dump

```cpp
#include <nlohmann/json.hpp>

// method 1:
// Create the JSON message
nlohmann::json msg;
msg["type"] = message_type;
msg["channel"] = channel_name;
msg["product_ids"] = product_ids;
msg["jwt"] = m_token;

// json.dumps (convert json object into flat string)
return msg.dump();

// method 2:
using json = nlohmann::json;
// Create a JSON object (similar to a Python dict)
json my_dict = {
    {"name", "Alice"},
    {"age", 28},
    {"active", true}
};

// Serialize to string (equivalent to json.dumps)
std::string json_string = my_dict.dump(); // dump as a string

std::cout << json_string << std::endl;
```

# -------------------------------------------------------------------------------------------------
# websocket protocol

```python
message = {
    "type": "subscribe",
    "channel": channel_name,
    "product_ids": products
}
# mainly sets message["jwt"] = token, returns message
signed_message = sign_with_jwt(message, channel_name, products)
# parses entire message dict into JSON string & send JSON string
ws.send(json.dumps(signed_message))
```

- websockets dont use HTTP request body & headers once connection is established (HTTP only used in the HTTP handshake)
    - HTTP handshake
    initial _GET_ request sent to `wss://://coinbase.com` => contains HTTP header & body
    CB replies with _status 101_ => protocol change
    (upon success) connection stays open as a raw bi-directional TCP pipe
    - no more headers, status code, req bodies etc. (not HTTP protocol anymore)
- ws protocol wraps JSON string in a frame
- frame only has a few bytes of overhead (`bit` indicating text or binary, `few bytes` indicate length of string, `masking key`)

# -------------------------------------------------------------------------------------------------
# generating intermediate file

intermediate file - file that has substituted code from the preprocessor, but not yet been compiled

```bash
cd build
ninja src/main.cpp.i // processes the file & generate a raw file called main.cpp.i
```

when running the normal build command:
- compiler never produce this intermediate file
- because it goes straight from src code (.cpp) to to binary object files (.o) & links them into the target executable

## use compilation database to generate intermediary file

{
    "directory": "/Users/joechua/Desktop/DEV/projects_production/market_infra/build_debug",
    "command": "/usr/bin/c++ -DBOOST_CONTAINER_NO_LIB -DBOOST_CONTAINER_STATIC_LINK -DBOOST_CONTEXT_EXPORT=\"\" -DBOOST_CONTEXT_NO_LIB=\"\" -DBOOST_CONTEXT_STATIC_LINK=\"\" -DBOOST_DATE_TIME_NO_LIB -DBOOST_DATE_TIME_STATIC_LINK -DPROJECT_SOURCE_DIR=\\\"/Users/joechua/Desktop/DEV/projects_production/market_infra\\\" -isystem /Users/joechua/Desktop/DEV/projects_production/market_infra/build_debug/vcpkg_installed/arm64-osx/include -g -std=gnu++20 -arch arm64 -o CMakeFiles/market_infra.dir/src/main.cpp.o -c /Users/joechua/Desktop/DEV/projects_production/market_infra/src/main.cpp",
    ...
}
- the command here is literally used to create (compilation & linking) the executable
- change -c to -E to only run the preprocessor phase
- change `CMakeFiles/market_infra.dir/src/main.cpp.o` to `-o main.i`
* as such: `-E /Users/joechua/Desktop/DEV/projects_production/market_infra/src/main.cpp -o main.i`

# -------------------------------------------------------------------------------------------------
# compile code (quickly)

`clang++ -g -std=c++17 main.cpp -o prog`

quick ez way to compile code

# -------------------------------------------------------------------------------------------------
# kill process

kill <PID>          defaults to signal 15
kill -15 <PID>      signal 15, kill with clean up (polite request)
kill -9 <PID>       signal 9, force kill

# -------------------------------------------------------------------------------------------------
# authenticate requests to the advanced trade WS API

- create secret API key (API key ID + private key)
- CDP kept the public key on their end
- python script sends subscribe

# -------------------------------------------------------------------------------------------------
# API authentication

okay so i have seen 4 ways that API authentication have been implemented so far.
1. calude: single string (single token system)
2. mongodb: public key (username) + private key (password)
3. coinbase CDP: API keyname (stirng with org & key ids) + private key (real private key)
4. coinbase exchange API: API key (username) + passphrase (password) + API secret (string used to compute hmac)

1. claude: single bearer token
    - include this token directly in the `Authorization: Bearer <token>` header
    - the server then looks it up in its DB, finds associated account & grants access
    - only sent over a secure network (TLS), where a packet sniffer cant theoretically decrypt the message
2. mongoDB: username + password
    - public key & private key are really just username & password
    - also relies on network to be secure => no asymmetric cryptography occurs
3. coinbase CDP: (key name + EC private key), placed in jwt [asymmetric]
    - sign a JWT using the EC private key
    - key name (API keyname) goes in the JWT header as the kID (key id)
    - coinbase server looks up corresponding public key by key name, verifies the signature, & grants access
    * private key is on client, while public key is with server; server decrypts signature using public key
4. coinbase exchange API: API key + passphrase + secret [symmetric]
    - no private key in this; API key (username) + passphrase (password) + secret is just some string that only you and coinbase knows
    - secret is used during the signing of the HMAC signature
    - body: to create HMAC signature, (timestamp + method + path + body) is _hashed_ using the _secret_
    - headers: _API key_ & _passphrase_ are sent as separate headers
    - but everything, your message API key + passphrase are all in there
    - will need a secure connection

# -------------------------------------------------------------------------------------------------
# dependency management (vcpkg.json & vcpkg-configurations.json)

_manifest mode_ - reads json manifest
- vcpkg.json - tells vcpkg what dependencies is required
- vcpk-congfigurations.json - tells vcpkg what registry to use & the baseline git commit we should look at
    * rather than looking at specific library versions, vcpkg's repository is maintained by microsoft where they ensure every lib then at that git hash commit is compatible with 1 another

boost website version of getting started guide (getting started with boost libs): https://www.boost.org/doc/user-guide/getting-started.html

```bash
# OLD
# according to the guide, the syntax below is used to include header only libs:
target_include_directories(my_app PRIVATE ${Boost_INCLUDE_DIRS}) # this is considered 
# and for libs that require compiled binaries, this is used:
target_link_libraries(my_app PRIVATE Boost::filesystem)

# NEW
# however, according to chat, modern CMake just use this for both cases(header-only & compiled-binaries lib) for external libs:
target_link_libraries(my_app PRIVATE Boost::filesystem)
# then this is used to include header files in my project directory
target_include_directories(market_infra PRIVATE include/)
```

- verbose explanation for market_infra project
```bash
cmake_minimum_required(VERSION 3.20)

project(market_infra)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# create compile_commands.json(compilation database) in build folder
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# find the package
# FAILS
# find_package(Boost REQUIRED CONFIG beast) # required config causes cmake to load the master BoostConfig.cmake file & imports all available boost modules & headers that vcpkg installed
    # however, because im in manifest mode, i should just use `find_package(Boost REQUIRED CONFIG)` since "all" refers to the dependecies of the project, not of all the dependencies on my mac previoulsy installed
    # however boost doesnt have individual .cmake configs for each of their components
# this also fails
# find_package(Boost REQUIRED CONFIG) # fails because cmake loads the master configuration file & bundles all header-only tools into the single targe Boost::headers
# which then you should just use 
# target_link_libraries(market_infra PRIVATE Boost::headers) # covers both asio & beast

# # so either do 1:
find_package(boost_asio REQUIRED CONFIG)
find_package(boost_beast REQUIRED CONFIG)
# # or 2:
# find_package(Boost REQUIRED COMPONENTS beast asio)

find_package(OpenSSL REQUIRED)

# create executable => always do so before you try to link libs to it
add_executable(market_infra src/main.cpp)

# now you may link it
target_link_libraries(market_infra PRIVATE Boost::asio)
target_link_libraries(market_infra PRIVATE Boost::beast)
target_link_libraries(market_infra PRIVATE OpenSSL::SSL)
target_link_libraries(market_infra PRIVATE OpenSSL::Crypto)
```

## CMake configure / cmake --preset

during configure stage:
1. vcpkg reads vcpkg.json
2. vcpkg downloads & installs boost & openssl
3. CMake processes CMakeLists.txt
4. find_package() locates the newly installed libs
5. CMake genereates the build rules (ninja/ makefile)
* whenever you edit CMakeLists.txt, you will need to re-run cmake --presets again (i.e. changing the way you compile the binaries)

* build stage is where:
    - pre-processor
    - compilation of individual .cpp files
    - linking

## cmake version

- on my ubuntu OS:
    - my cmake version is 3.28.3.
    - i thought this was old since (iirc) the cmake version on my mac was 4.X.X+
    - apparently cmake (3.28.3) is not considered old for standard linux dev
    - its the default package shipped with ubuntu 24.04 LTS
    - use the command `lsb_release -a` to check Ubuntu OS version
        No LSB modules are available.
        Distributor ID: Ubuntu
        Description:    Ubuntu 24.04.3 LTS
        Release:        24.04
        Codename:       noble
    * note that when building projects, you will see that vcpkg might install newer versions of CMake into its own cache dir to use strictly for building project's libs
        => doesnt replace system's global Cmake
        => project libs are downloaded in to vcpkg_installed in the build folder

## vcpkg repo out of sync

* error due to vcpkg git repo is out-of-sync
```bash
error: while checking out baseline from commit 'b216ddff25a1f432870e6c340ce79357049ef86e', failed to `git show` versions/baseline.json. This may be fixed by fetching commits with `git fetch`.
```
* resolve is to pull commits as vcpkg refers to your local repo's commits and uses baseline commit for reference
    => no commit, no ability to install packages accordingly

# -------------------------------------------------------------------------------------------------
# Boost (Asio & Beast)

Boost.Asio - TCP + TLS
Boost.Beast - builds on Asio, adds HTTP + websocket
* beast handles websocket handshake & framing (App layer), Asio handles TCP + TLS (transport layer)

Asio provides SSL stream wrapper but doesnt implement SSL itself
thus, requirebeast/ssl.hpp for ssl integration (handles all the wrapping & fall back when connection doesnt have valid ssl cert etc.)


# -------------------------------------------------------------------------------------------------
# coinbase API endpoint (public CA or custom CA)

had to recap on how the SSL handshake work
key reminder: the SSL handshake is a authentication process mainly for the client to determine that the server is a trusted server

SSL handshake
- client has standard CA public key OR custom CA public key
- when client sends a 1st hello message, server needs to send back it's SSL certificate (signed by CA private key & cert contains server's public key)
- client receives this SSL cert and, (1) decypts (using CA public key) & compare hashes to determine cert is legitimate, (2) encrypts secret message with server's public key
- server then receives secret & decrypts this using its private key (ensures that server is legitimate)
- then server uses private key to encrypt secret message & send it back to client
- finally, client confirms this connection is legitimate, & both then does symmetric communication using 1 common key (faster to encrypt & decrypt)

OpenSSL
widely used open source software lib that provides the tools to encrypt data & secure communications over computer networks
dont need to re-implement the underlying logic to attach a cert, verify a cert using hash etc.
its like the http library (we dont want to re-implement all the parsing logic etc. and just get the body of a request etc.)

assumption: my assumption is that since coinbase didnt provide a Custom root certificate (custom CA cert), this means that it should be using standard CA verification
to test this:
`openssl s_client -connect fix-md.sandbox.exchange.coinbase.com:6121 -showcerts`
- dont include the _URI scheme_ `tcp+ssl://` as openssl already assumes that you are using TLS over TCP

example output:
joechua@Chuas-MacBook-Air-3 market_infra % openssl s_client -connect fix-md.sandbox.exchange.coinbase.com:6121 -showcerts 
Connecting to 44.208.3.10
CONNECTED(00000005)
depth=2 C=US, O=Amazon, CN=Amazon Root CA 1
verify return:1
depth=1 C=US, O=Amazon, CN=Amazon RSA 2048 M01
verify return:1
depth=0 CN=*.sandbox.exchange.coinbase.com
verify return:1
...

## issue: FIX API are only for institutional investors

when trying to access https://exchange.coinbase.com/ , i get the following message:
"joechua247@gmail.com does not have access to Coinbase Exchange. If you are not applying on behalf of a business, continue to Advanced Trading."

- the advanced trading API only supports REST & websocket APIs
- need to connect to websocket API and draw in data from there instead
- could potentially simulate this environment by having a client send transactions that replay what happened, then have another client trade against it(the strategy program)

* dont be confused by coinbase pro (this was the old name for coinbase advanced trading API)
* additionally it seems that the FIX endpoint is not available to retail traders anymore due to low usage

## links for exchange API
Exchange FIX API Connectivity: https://docs.cdp.coinbase.com/exchange/fix-api/connectivity
FIX message formats: https://docs.cdp.coinbase.com/exchange/fix-api/market-data#logon-35%3Da
exchange sandbox docs: https://docs.cdp.coinbase.com/exchange/introduction/sandbox
exchange sandbox: https://public-sandbox.exchange.coinbase.com/trade/BTC-EUR
create API key for coinbase exchange APIs: https://help.coinbase.com/en/exchange/managing-my-account/how-to-create-an-api-key

## links for advanced trade API
advanced trade API FAQ: https://docs.cdp.coinbase.com/coinbase-business/advanced-trade-apis/faq#what-is-advanced-trade-api (mentions that exchange API is only for institutional clients && what happened to coinbase pro)


# -------------------------------------------------------------------------------------------------
# Clangd multiple presets

faced an issue where clangd (language server) could not read the compilation database(`compile_commands.json`)
this is due to the nested folders in the `build` folder (`build/release` & `build/debug`)
clangd's `CompilationDatabase` flag in `.clangd` can only read folder path of 1 level (hence this worked for `build` before)
i have since updated the presets to use `build_debug` & `build_release`

stack overflow: https://stackoverflow.com/questions/68885293/clangd-for-vscode-with-multiple-build-directories