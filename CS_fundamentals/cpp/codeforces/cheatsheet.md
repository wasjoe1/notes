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

# rounding error
- always
    (1st) `std::llround(floating_type)`,
    then (2nd) static_cast<to_cast_type>(val)
- 0.5 & above will round up, else round down

# arithmetic operation (implicit conversion)
- c++ decides result type base on operand's type => need to explicitly cast first
- i.e. int * int => returns int (will overflow)
- i.e. int * long long => returns long long
- i.e. int * (long long)int => returns long long (explicit cast)

# std::list


# std::vector
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
