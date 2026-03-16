# notes
Random unorganised notes taken while learning cpp

# Initializations (default, direct, copy, list)
# container.insert()
# insert() efficiency (pre-allocate vs allocate on the fly)
# Threads
# implicit instantiation of undefined template
# name shadowing

# -------------------------------------------------------------------------------------------------
# Initializations + Constructions

## Initializations
```cpp
class MarketDataClient {...};
MarketDataClient client;   // already constructs the object => calls the default constructor
// client = MarketDataClient(); // this is not required => infact this creates a temp MarketDataClient obj then moves it into client
// MarketDataClient client = MarketDataClient(); // same thing => copy elision helps to prevent creating the temp MarketDataClient though; effectively same as MarketDataClient client;
```
- default initialization: `MarketDataClient client;` -> obj is created without args => calls the default constructor
- direct initialization: `std::thread t(worker);` -> construct t directly by calling the std::thread constructor with args (worker)
- copy initialization: `std::thread t = std::thread(worker);` -> construct t in a temp then move created thread into t
    equivalently:
    1. std::thread tmp(worker);
    2. std::thread t(std::move(tmp));
    * note that this is still considered copy initialization PURELY coz of the syntax & not because of the inherent steps under the hood
    * but what happens here is actl considered `move construction`!!
- list initialization (Brace Initialization)
    avoids narrowing conversions
    std::vector<int> v{1,2,3};
    int x{3.14}; // ❌ compile error (narrowing)

## Constructions
- Move Construction
    - `std::vector<int> ans = std::move(nums);`
    - so now nums is empty
    
    * internally:
    * (b.ptr = a.ptr, b.size = a.size) __-becomes->__ (a.ptr = nullptr, a.size = 0)
* transfer ownership of internal resources => faster coz its not copying!!

Assignment (not construction)
MarketDataClient client;
client = MarketDataClient();
operator=(MarketDataClient&&)
assignment happens after construction.


## copy initialization e.g.
what does vector<int> ans = nums; do?
```cpp
std::vector<int> ans = nums; // copy initialization syntax BUT => compiler after cpp17 will do vector(const vector&) => copies over the elemnts to the actual storage place rather than a temp
std::vector<int> ans(nums); // direct initialization

// both creates a new vector by COPYING nums!!
// 1. allocate MEM for ans
// 2. copy each element from nums to ans
```

is it because its copy by value, so when i change the element in ans, it doesnt change it in nums
[cling]$ nums
(std::vector<int, allocator<int> > &) { 2, 2, 3 }
[cling]$ v
(std::vector<int> &) { 1, 2, 3 }
[cling]$ 
as can be seen from here?
<!-- can see that OG array is not affected since it is just COPY-ing elements over!! -->

# -------------------------------------------------------------------------------------------------
# container.insert()
what does container.insert() do?
```cpp
ans.insert(ans.end(), nums.begin(), nums.end()); // insert adds elements into a container at a specified position
// iterator insert(iterator pos, InputIt first, InputIt last);
// return value of insert => iterator

// insert into ans
// at position ans.end() => the end of the ans vector
// copy elements from range nums.begin() to nums.end() => if u think about it, its just elements from the nums vector
// key word is COPY
```

# -------------------------------------------------------------------------------------------------
# insert() efficiency (pre-allocate vs allocate on the fly)
This 2 version when compared, why is the 1st one faster?
## version 1
```cpp
vector<int> ans;
ans.reserve(nums.size() * 2); // already allocates enough space
ans.insert(ans.end(), nums.begin(), nums.end());
ans.insert(ans.end(), nums.begin(), nums.end()); // just needs to copy/ move elements into the storage space
```

## version 2
```cpp
vector<int> ans = nums; // allocates enough space for nums first & copy those n elements
ans.insert(ans.end(), nums.begin(), nums.end()); // then continue need to reallocate for this insert method, & shift n elements from the first buffer first
return ans;
```

# -------------------------------------------------------------------------------------------------
# implicit instantiation of undefined template
ISSUE: encountered the red squibbly error in compilation: "implicit instantiation of undefined template"
std namespace is defined across many headers, not just 1
each header adds specific components into std namespace
i.e. <vector> adds std::vector to std namespace
templates live in headerse coz the compiler must see the full implementation when generating types
but if the <vector> template was not included, the std namespace would not know vector exists maybe `template<class T> class vector { ... };` but not the entire definition

* sometimes there are forward declarations in other header files via `#include <something>` hence it throws the error "implicit instantiation of undefined template"

SOLUTION: #include <vector>

# -------------------------------------------------------------------------------------------------
# name shadowing (this keyword)
when we actually need to use `this` keyword

```cpp
class OrderBook {
    int x;
public:
    void setX(int x) {
        this->x = x;
    }
};
```

# -------------------------------------------------------------------------------------------------
# Threads
1. C style `pthreads`
2. Modern Cpp threading `std:: thread`


## example C code
```c
#include <pthread.h>
#include <stdio.h>

// worker function
void* worker(void* arg) {
    printf("hello from thread\n");
    return NULL;
}

int main() {
    // create thread
    pthread_t thread; 
    pthread_create(&thread, NULL, worker, NULL);
    pthread_join(thread, NULL);

    return 0;
}

```

## questions regarding C threads (pthreads)
- is does thread have default initiailization?
    - NO => C has no constructors (doesnt support classes)
    - so there is no default initialization like in cpp
    `pthread_t thread;` jsut allocate space, but leave variable uninitialized
- for c, why thread address passed into create() but not join()?
    - `pthread_create(&thread, ...)` -UTH-> roughly `*thread = kernel_thread_id;`, basically assigns a kernel thread to our thread variable at this address
    - fn signature: `int pthread_create(pthread_t *thread, const pthread_attr_t *attr, void*(start_routine)(void*), void *arg)`
- what is `void*` in return type & parameter type? `void* worker(void* arg)`
    - `void*` exists coz there is no generics/ templates in C
        - i.e. `void*` was useful when assigning returned space from mallo
        `void* malloc(size_t size_in_bytes);` => since malloc is used to create an array of MEM for any type
        `int* arr = malloc(sizeof(int)*10);`
    - for pthread workers `void* worker(void* arg)`
    ```c
    // allows for any type of arg
    worker(int*)
    worker(struct*)
    worker(CustomObject*) ...

    //i.e.
    typedef struct {
        int a;
        int b;
    } Params;

    void* worker(void* arg) {
        Params* p = (Params*) arg // cast the arg to use the params properly; if u dont cast, compilation error as compiler cant recognise that there is a & b member variables
        printf("%d %d\n", p->a, p->b);
    }

    // then
    Params params = {1,2};
    pthread_create(&thread, NULL, worker, &params);
    ```
    - compiler doesnt know the layout of the memory => "layout of the memory" -> struct memebers are accessed by offsets in MEM
    ```c
    typedef struct {
        int a;
        int b;
    } Params;
    ```
    memory layout:
    Params
    +--------+
    | a (4Bytes) |
    +--------+
    | b (4Bytes) |
    +--------+
    a → offset 0
    b → offset 4 == `p->b` == `*(p+4)`
    * thus when compiler doesnt know the type, its not able to compute the offsets & retrieve the correct member variables

## example Cpp code
```cpp
#include <thread>
// #include <iostream> // for std::cout
#include <fmt/core.h>

// free function
void worker() {
    fmt::print("Hello from thread\n");
}
int main() {
    std::thread t(worker); // creates thread with direct initialization
    t.join();
}

// member function
class MarketDataClient {
public:
    void connect() {
        ws_thread_ = std::thread(&MarketDataClient::websocket_listener, this); // initialize the thread
private:
    void websocket_listener();
    std::thread ws_thread_;
```

## questions regarding cpp code
- why do i need to take in __address__ for member fn & __this__?
    
    __free fn__
    - free function => doesnt belong to any object, thread can call it directly
    
    __member fn__
    - thread needs both the __&Class::member_fn__ & __this obj__ to call it on
    - __&Class::member_fn__: why do i pass in __&Class::member_fn__ instead of just __Class::member_fn__
        - `&Class::member_fn` returns a pointer to a member fn => not a normal fn pointer
        - member function pointer type `void (MarketDataClient::*)()` which is what `std::thread(ptr, obj_to_exec_on)` takes in for ptr
        - `void (MarketDataClient::*)()` 1. means pointer to a member fn, 2. belonging to MarketDataClient, 3. that returns void, & 4. takes no params
        - `void (*f)();` <= free fn pointer type
        i.e.
        ```cpp
        void worker() {}
        void (*some_ptr)() = worker;
        some_ptr(); // calls worker
        ```
    - then when thread combines it with __this obj__, it calls `(this->*websocket_listener)()`

    * good to know:
    * member fns have hidden param this: i.e. `void websocket_listener(MarketDataClient* this, ...)` => its like python's self
        - compiler sees `MarketDataClient::websocket_listener(this, ...)` during execution
    * normal functions are not pointers
        -> although, a function name can auto convert(decay) to a fn pointer
        -> type of `worker` is `void ()`, type of pointer pointing to it is `void (*)()`
        -> compiler auto converts worker -> &worker
        - `void (*f)() = worker` == `void (*f)() = &worker`

# Scopes, namespace & MEM mgmt
qns: does scope & namespace mean the same thing in cpp? i.e. if i use the namespace std i am using that scope & can bring invariables from there?
is the memory management also reflective of this?
i.e. if i declare a plain enum, its on the data segment whereas if its for std::, actually they would also be on the data segment just a different scope?

- scope is the region of code where a name is visible
- namespace is a __named scope__ for identifiers (can call types, functions, variables from that scope)
- i.e.
    ```cpp
    namespace math {
        int add(int a, int b) { return a + b; }
    }

    // doesnt change scope, simply tells the compiler when looking up names, also search the `std` namespace!
    using namespace std;
    // allows u to write
    cout << "hello" // instead of std::cout

    // #include <vector>
    ```
- scope & namespace have nth to do with MEM mgmt
    - x & y are both global variables => both go into data segment MEM
    ```cpp
    namespace A { int x = 10; }
    int y = 20;
    ```
- `enum Color { RED, GREEN, BLUE };` does not allocate MEM at all! => compile-time constants