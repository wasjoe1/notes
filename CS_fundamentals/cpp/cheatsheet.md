# -------------------------------------------------------------------------------------------------
# C++ CONCEPTS
# array<n>
- array<n> requires n to be compile-time known constant => cant be a runtime const int value
- cin >> n; array<n>; => this will never work as n is known only at runtime
- no choice have to use vector

# constexpr
- ensure var is a constant expression; compile-time evaluatable

# initialization & assignment
- initialization:
    - mandatory copy elision: URVO
    - optional copy elision: NRVO
    - move semantics: no NRVO
- assignment:
    - no copy elision, always move (temp created then moved into existing slot)

# int/ # number
- delimiters: `'` intro-ed in c++14 i.e. `long long big_num = 29'000'000`
- suffixes:
    - `LL` - no compilation error nor overflow occurs i.e. `6553601000000LL`; c++ std says compiler picks the 1st type that can hold the value
        => however its safer to use during arithmetic operations, else overflow might happen
        => becoz literal's type is picked at compile time
        => `long long a = 6553601 * 1000000` int * int (overflows b4 assignment)
        => `long long a = 6553601LL * 1000000` int promoted to LL
        * c++ does type checking from the operands inward
        * from c++17 onwards, scalars (like int) directly initializes the variable (b)
- string to int
    - `std::stoi`
    - `std::stol`
    - `std::stoll`
- string to double
    - `std::stod`
    - `std::strtod` (for low level C style)
- comparing `int` with `long long`
    => is allowed becoz of _implicit type promotion_ => int auto converted to long long

# rounding error
- always
    _correct_
    (1st: round) `std::llround(floating_type)`,
    then (2nd: cast) static_cast<to_cast_type>(val)
    * `int good_value = (int)std::round(0.29 * 1e8);` => returns 29'000'000
    _commonGotcha_
    (cast then round) `int bad_value = std::round((int)(0.29 * 1e8)); `
    * we want 0.29, but becoz 0.29 is not accurately represented in base-2(0.28999999....),
    0.28999... * 10^8 = 2899...; cast cuts of decimals, then rounding does nothing
- 0.5 & above will round up, else round down

# arithmetic operation (implicit conversion)
- c++ decides result type base on operand's type => need to explicitly cast first
- i.e. int * int => returns int (will overflow)
- i.e. int * long long => returns long long
- i.e. int * (long long)int => returns long long (explicit cast)

# friend
- has 2 use cases:
    1. grants access to private / protected members
    2. injects a name into the enclosing namespace, but only findable via ADL (argument dependent lookup) and not ordinary unqualified lookup
- ADL
    - additionanly compiler check for function-call syntax like foo(x,y) & x==y
    - rule: also look in the namespaces associated with the types of arguments
    - issue:
        ```cpp
        namespace kraken {
        struct L3Order { /* ... */ };
        bool operator==(const L3Order& a, const L3Order& b) { /* ... */ }
        }
        int main() {
            kraken::L3Order o1{...}, o2{...};
            if (o1 == o2) { ... }  // how does this find kraken::operator==?
        }
        ```
    - friend solves this:
    ```cpp
    namespace kraken {
        struct L3Order { /* ... */ };
    }
    namespace pricing {
        struct Quote { /* ... */ };
    }
    namespace kraken {
        bool operator==(const L3Order& order, const pricing::Quote& q) { /* ... */ }
    }

    int main() {
        kraken::L3Order o{...};
        pricing::Quote q{...};
        if (o == q) { ... }  // works — ADL finds it => checks both kraken & pricing namespaces
    }
    ```
- friend is implicitly declared as `inline`

# std::list


# std::vector
- push_back(x);
    - takes the value of an element by value
    - i.e.
        ```cpp
        // 1: by value
        for (char c : str) { v.push_back(c); }
        // 2: by reference
        for (const& char c : str) { v.push_back(c); }
        ```
        for (1), theres 2 copies
        => read `str[i]` into c is copy #1, copy c into ch parameter in `push_back(c)` is copy #2 
        for (2), theres 1 copy
        => `c` just aliases str[i] directly, copy #1: `push_back(c)` still copies from `c` into `ch` param

        => but `-O2` optimization, compiler just loads a byte from str, & store at `v`'s current write position for both
- push_front
    v.push_front(val);
    auto it = v.begin(); // get new element
- insert => inserts at pos, returns iterator to 1st of new elements
    auto it = v.insert(position, value) // i.e. v.insert(v.begin() + 2, 10)
- delete
    auto it = std::find(v.begin(), v.end(), value)
    if (it != v.end()) { v.erase(it); }
- find => find base on value
    std::find(v.begin(), v.end(), value) => value has to match exactly
- find_if => find base on predicate
    std::find_if(v.begin(), v.end(), [&](const Item& x) { return x.item_id == outside_x.item_id; })
- dereference it to get obj
    1. order_it->qty
    2. (*order_it).qty
- check if empty
    - v.empty() => recco-ed/ standard way (available from c++98)
    - v.size() == 0
    - v.begin() == v.end()
- get the last element
    T& last = v.back()
- calling destructor
    v.~vector()
    * this destroys all elements inside the vector too
- back() - returns last element
    * if no element, this causes UB
- end() - returns iterator pointing to theoretical element 1 past element in the container
- fill vector with same values
    `std::vector v(n, value)` => initialize vector with n elements, all with value
- fill a range of values
    `std::iota(v.begin(), v.end(), start_val)` => create & inserts elements starting with the value `start_val`
    => iota doesnt stand for anything, its the greek symbol `I` (read as iota) => used to represent i

# std::unordered_map
- find if key exists
    it = map.find(key);
    if (it == map.end()) { return; } // couldnt find the key in map
    auto& val = it->second; // val is a struct with price & it
- storing iterators
    - unordered_map<string, list<L3Order>::iterator>
    - generally dont store raw ptr because unsure if its safe to dereference + no next & prev ptrs
- removing key value pairs
    - remove via key name => `map.erase(key_name);`
    - remove via iterator => `auto it = map.find(key_name)` then `map.erase(it)`
    * erase calls the destructor of the mapped value stored at that key (vector's destructor gets called)

# unordered set

# set
set<int> s = {5, 3, 2,  5}
- find (2 ways)
    1. auto it = s.find(val)
        if (it != s.end()) { // found }
    2. s.contains(val) // returns true/ false

# map
- creating ascending & descending maps
    std::map<Key, T, Compare>
    std::map<Price, PriceLevelVector, std::greater<Price>> bids
    std::map<Price, PriceLevelVector, std::less<Price>> asks    => (default)
    - retriving largest element from bids is still `bids.begin()`
    - std::greater & std::less are functors(function objs), not lambdas! => because templates require a type, not instance of an object
- rbegin() is O(1) => pointer to the rightmost (max) node is updated incrementally after each add/ erase
- use the following tools when:
    - `[]` - for write access
    - `.at()` - for read access => throws `std::out_of_range`, or `json::out_of_range` for nlohmann in both debug & release
    - `.find()`/ `.contains()` - to check
    * Assertion `it != m_data.m_value.object->end()' failed. is the equivalent of not being able to find a key

# for loop
- range based => default preferred
    for (auto& elem : v) {...}
- forward iteration in vector (manual iterator) => when `it` is meaningful
    for (auto it = v.begin(); it != v.end(); ++i) {...}
- backward iteration in vector
    for (auto it = v.rbegin(); it != v.rend(); ++it) { // *it gives you elements from last to first }
- index-based loop => when index is meaningful
    for (size_t i{}; i < v.size(); ++i)
- coding jesus's 4 for loops
    for (int i = 0; i < v.size(); i++) // 1
    for (size_t i{}; i < v.size(); ++i) // 2
    for (auto i{0uz}; i < v.size(); ++i) // 3
    for (auto i{v.size()}; i-- > 0;) // 4

# sort
vector<int> v = {1, 2, 3 ...}
std::sort(v.begin(), v.end()); // sorts whole container
std::sort(v.begin(), v.begin() + 2); // sorts 1st 2 element

# arrow operator & asterix
- arrow operator recursively calls till it reaches a raw ptr (rule: -> returns either raw ptr or another obj with -> operator)
- (*) dereference operator => returns reference to data `T& operator*() { return *ptr; }`
    - writing `T opereator*() {..}` is dangerous
    - likely throw `lvalue required error` as left side of `=` needs to be lvalue i.e. `*it = new_value`
    - this however have no compilation error `var = *it` but causes a copy

# T& and T
- returning a reference to a non-ref variable creates a copy
    - `Box& getBox() { return og; }` and `Box b = getBox();`
    - b is a copy of og, and any modifications will not affect og
- returning reference type
    `Box& getBox() { return og; }` or
    ` OrderBook& booksFor(const std::string& symbol) { return book.symbol_to_books_.at(symbol); }`
    - these are good to return as references
    - you want the actual object, not a newly constructed / copied value of the object

# strings
- here are a few ways to define strings in a legacy C fashion:
    ```cpp
    char* arr_data = "hello " // is allocated in data segment
    char buf_stack = "hello" // is allocated on the stack
    char* buf_heap = new char[6]; // allocated on the heap

    // (1) WRONG
    arr_data[0] = 'H'; // UB, writing into read only MEM
    // (2) Ok
    char* p = buf_stack;
    p[0] = 'H' // buf becomes "Hello"
    // (3) Ok
    strcpy(buf_heap. "hello");
    char* p - buf_heap;
    p[0] = 'H' // buf becomes "Hello"
    ```
    * and only the (2)stack and (3)heap strings are mutable

# std::string
- string concatenation
    - in python `res += new_str` in a for loop is bad
        => becpz res CPython's strings is immutable
        => each += allocates a new string & copies both strings into the new string MEM
        => O(n^2)
        => `''.join(string_arr)` is good
        => it goes over each string & sum up `len(word)`
        => allocates a buffer for the new word
        => then memcpy each word into its final position
    - in c++ `res += new_str` in a for loop is fine
        => `std::string` is mutable; holds mutable heap buffer (or inline SSO buffer)
        => `s += word` appends word into s's own buffer
        => if `size() + word.size() <= capacity()`: memcpy word into existing buffer
        => if doesnt fit, allocate new buffer
        => amortized O(1)
        => for a more optimized version, `reserve()` enough space first; improves to only 1 heap allocation
    ```cpp
    // good
    std::string concat_all(const std::vector<std::string>& strs) {
        size_t total = 0;
        for (const auto& s : strs) total += s.size();

        std::string result;
        result.reserve(total);
        for (const auto& s : strs) {
            result.append(s);
            // or
            result += s;
        }
        return result;
    }
    ```

# string_view
- string_view holds 2 things: ptr to text & length
- when using `string_view` to take in a string into a function, dont use `const`
    => `r_type function_name(string_view s) {...}`
    => using `const` means the view becomes read-only
    => cant change where the view starts (slicing)

# parsing using json
```cpp
on_message(std::string_view str) {
    // parse & return a json object
    // dont use auto& because json::parse(...) returns an rvalue (cant bind variable to rvalue object)
    auto parsed = json::parse(str);
    // create output stream
    std::ofstream out_file("file_name.txt", std::ios::app);
    // parsed.dump() returns opposite of json::parse(); converts json back to string
    outfile << parsed.dump() << "\n";
}
```

# const char* vs constexpr std::string_View
- `constexpr std::string_view` is preferred
    - instant length lookup O(1) vs O(n): `const char*` doesnt know how long the string is, `std::string_view` is a container that knows its length
    - full std lib support: `const char*` relies on old C-style functions (i.e. strlen or strcmp); string_view can use .starts_with(), .find(), & substr()
    - safer & easier substrings: creating a substring in `const char*` requires allocating new MEM on the heap; std::string_view can create new temp obj + mutate it easily

# constexprfor constant string_view
- declaring `constexpr` as class members requires using `static` keyword => extend's variable's lifetime to duration of entire program (put data inside data segment of MEM)
    - instance member variable is only allocated during runtime (dynamically allocated obj)
    - hence constexpr members which are static (class members) need to be declared with static
    ```cpp
    class KrakenOrderbookTest : public ::testing::Test {
    protected:
        static constexpr std::string_view delete_ask = R"({"channel": "level3", "type": "update", "data": [{"checksum": 1581522232, "symbol": "BTC/USD", "timestamp": "2026-07-07T22:22:09.435524030Z", "bids": [], "asks": [{"event": "delete", "order_id": "OV3GLF-4ZM7H-TIG7KK", "limit_price": 63430.9, "order_qty": 0.00856536, "timestamp": "2026-07-07T22:22:09.435524030Z"}]}]})"
        ...
    ```

# type alias
- basic type alias (old way): `typedef ExistingType NewTypeName` => did not have builtin support for template
    ```cpp
    // WRONG
    template<typename T>
    typedef ExistingType NewTypeName
    // workaround
    template<template T>
    struct Registry {
        typedef std::vector<T> type; // acceptable
    }
    ```
- basic type alias (new way): `using NewTypeName = ExistingType`
- template type alias:
    ```cpp
    template<typename T>
    using StringMap = std::map<std::string, T>

    // usage
    StringMap<int> myMap; // same as std::map<std::string, int>
    ```

# template metaprogramming
## fold expressions
```cpp
template<typename... Args>
auto sum(Args... args) {
return (args + ...); // right fold expression => expands to (a + (b + (c + d))) with args a, b, c, d
// return (... + args); // left fold epxression => expands to (((a + b) + c) + d)
}
```
## recursive variadic arguments
```cpp
void print() {std::cout << '\n';}
template<typename T, typename... Args>
void print(T first, Args... rest) {
cout << first << " ";
print(rest...);
}
```
## C style variadic functions
```cpp
#include <iostream>
#include <cstdarg>

// need atleast 1 named arg (i.e. count)
void printNumbers(int count, ...) {
    va_list args;
    va_start(args, count); // says to start tracking after 'count'
    for (int i = 0; i < count; ++i) {
        // manually tell compiler that args are int type
        // danger: if accidentally pass a double here during runtime, UB!
        int val = va_arg(args, int);
        cout << val << " ";
    }
    va_end(args); // tell the compiler that end of args
    cout << '\n';
}
```

## return result
```cpp
// Vector template type must be declared
template<... I>
struct Vector {}

// primary template — declaration only
template <typename V>
struct uniq;

// specialization: matches any Vector
// Suppose uniq<Vector<1, 2, 2, 3>> is meant to "return" Vector<1, 2, 3>
template <int... I>
struct uniq<Vector<I...>>
{
    using type = Vector<1, 2, 3>;   // (pretend this was actually computed from I...)
};
```
- template<int... I> struct Vector { }; — I is a pack of compile-time integer values (not types!)

# external / internal linkage misconceptions
- function scenario: if i declare & define a fn in file_A, and forward declare that fn in file_B, can file_B use that fn? YES
    => yes file_B can use that fn
    => functions are code instruction; linker will link the defn over
    * idea is to ensure fn is extern, compile .cc/.cpp files separately (separate TUs), then link them
- class scenario: if SomeClass is declare & defined in file_A, and forward declared in file_B, can file_B use that class? NO
    => classes are blueprints for MEM size => tells compiler how much space the object takes
    => compiler doesnt "link" over the size of a class
    * idea is to #include header files that contain class definitions, but exclude the method definitions

# google style guide (naming variables)
- trailing underscores => used for member variables BUT doesnt apply to structs used as passive data-only types
    - private / protected data members of a class -> `bids_`
    - puvlic members of plain data-holding struct -> `bids`

# output logging
c++ stream obj  stream  FD  
cin             stdin   0
cout            stdout  1   (buffered)
cerr            stderr  2   (not buffered) => gets flushed immediately

- by POSIX convention, every process starts with 3 FDs => auto added into FD table of process
- `./program > out.txt` only redirects FD1 from terminal to `out.txt` file
- `./program > out.txt 2>&1` redirects FD2 to wherever FD1 is pointing to; both gets redirected to out.txt

# cmake
`cmake --preset <preset> --fresh`
`cmake --build <build_dir> --clean-first`
`cmake --build <build_dir> --target <target>`

# ctest
- run test separately:
    - `-R` (regex match) - `ctest -R "TestName"`
        => default looks for partial matches
        => exact match: `ctest -R "^TestName$"` -> (^) forces start + ($) forces end
    - `-I` (test number) - `ctest -I [start],[end]`
        => runs a range of test
        => `ctest -I 5,5` => start & end at test 5
        => `ctest -I 5` => start at test 5, all the way to last test
- find test number: `-N`
    - stands for no execute/ show only
    - `ctest -N`
- exclude other test => `ctest -E "SkipThisTest"`
    - using `-E` with `-R`: `ctest -R "^Test_Auth" -E "Logout$"` => runs all Test_Auth, except the Logout tests
- verbose logging => `ctest -V` shows stdout of single test in real time
    - using `-V` with `-R` => ctest -R "^YourTestName$" -V
- only print the failed tests
    - `--output-on-failure` => only verbosely prints for the tests that fail; unlike -V that prints for ALL tests
    - `--rerun-failed` => reruns only the failed tests

# regex
- Character Matches:
    -  . matches any single character except a new line.
    - \d matches any digit from 0 to 9.
    - \w matches any letter, digit, or underscore.
    - \s matches any whitespace like spaces or tabs.
- Quantifiers (How Many)
    - * matches the previous item 0 or more times.
    - + matches the previous item 1 or more times.
    - ? matches the previous item 0 or 1 time.
    - {n} matches the previous item exactly n times.
- Positions and Logic
    - ^ matches the very start of a line.
    - $ matches the very end of a line.
    - | acts like an OR switch to match this or that.
    - \ escapes a symbol to treat it as regular text.
- Groups and Sets[abc] matches any one character inside the brackets.
    - [^abc] matches any one character NOT inside the brackets.
    - (abc) groups tokens together to capture them as a unit.

# -------------------------------------------------------------------------------------------------
# LOW-LEVEL CONCEPTS
# L1, L2, L3 cache
MESI protocol - cache coherence protocol; ensures all cores see the same data
M(modify) E(exclusive) S(shared) I(invalid)
- write op
    1. core 1 broadcasts invalidation req over shared MEM bus
    2. snooping: all other cores constantly monitor this bus for addresses they have in their cache
    3. when other core sees msg, they intercept it
    4. transition:
        - snooping cores: S -> I
        - write core: S -> M
- exclusive: optimization purpose => eliminate unnecessary bus traffic by giving a single core exclusive acces to a MEM region

# why euclidean algo works? (finding GCD)
- qns: why does repeatedly subtracting smaller number from larger number, eventually produce GCD
- ans:
    - claim: If a > b, then gcd(a, b) = gcd(a-b, b).
    - This is because any number that divides both a and b must also divide (a-b)
    - so conversely, any number dividing both (a-b) and b must also divide a (since a = (a-b) + b).
    - hence, subtracting doesn't change the set of common divisors —> it just shrinks the numbers while preserving the gcd
    - keep doing this until two numbers are equal (or one hits 0) and that final value is the gcd
    * greatest divisor is never broken apart
    * visualization: https://www.youtube.com/watch?v=Jwf6ncRmhPg&t=520s
