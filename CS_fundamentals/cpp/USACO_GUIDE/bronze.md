# Time complexity

Q. how to best calculate how many operations it takes to run each algo in terms of the input size
Ans. Big O notation - expresses worst-case time/ space complexity as a function of n as n gets arbitrarily large

# Intro to Data structures

Cpp standard lib data structures are designed to store any type of data. put the desired type within <> brackets

- Arrays & Dynamic arrays
    - arrays
    - dynamic arrays
    - iterating
    - inserting & erasing
- strings
- pairs & tuples
- MEM allocation

## Arrays & Dynamic arrays

### Arrays

```cpp
std::array<int, 25> arr; // array of 25 int elements initialized; default initialized (garbage values)
arr[5]; // access 5th element

// intializing an array of 0s
    // for loop
    // declare in global scope
    // value initializer
    // built-in function
```

### Dynamic arrays

dynamic arrays support same operations as static array, but is able to resize itself. it cam add & delete elemets at the end in O(1) time

```cpp
// create vector with initial size + have elements
std::vector<int> vec(10); // creates a vector of 10 ints, all initialized to 0
std::vector<int> vec(5, 99); // creates a vector of 5 ints, all initialized to 99

// create vector with initial size + no elements
std::vector<int> vec; // creates a vector of 0 ints
vec.reserve(10); // only allocates MEM, no ints / objects initialized

// resize vector
std::vector<int> vec; // creates a vector of 0 ints
vec.resize(10); // resized to 10 with default values (0) in the allocated MEM
vec.resize(15, 7); // resize to 15, with the 5 new elements being 7
```

### iterating

```cpp
// (1) regular for loop
vector<int> v{1,2,3,4};
for (int i = 0; i < int(size(v)); i++) { std::cout << v[i] << " "; }

// (2) iterators: begin() & end()
for (vector<int>::iterator it = v.begin(); it != v.end(); ++it) { ... }
for (auto it = begin(v); it != end(v); next(it)) { ... } // use auto & vector itself
for (auto it = v.begin(); it != v.end(); ++it) { ... } // use auto & vector itself
for (auto& element : v) { ... } // range-based loops

// *(3) coding jesus's 4 for loops
for (int i = 0; i < v.size(); i++) // 1
for (size_t i{}; i < v.size(); ++i) // 2
for (auto i{0uz}; i < v.size(); ++i) // 3
for (auto i{v.size()}; i-- > 0;) // 4
```

*(3)
2. need to value-initialize i, if not it will contain garbage value
3. `uz` is a suffix which tells the compiler that the literal `0` is of type `size_t`, so u can just auto it
4. 2 main advantages: avoid int underflow && speed + MEM optimization
- speed + MEM optimization
    - in a standard i < v.size(), CPU needs 2 separate variables to compare
        => i in 1 register
        => v.size() in another register
        => runs CMP assembly instruction
    - when using i-- >0
        => during subtraction operations of a register, the CPU uses ZF (zero flag) or SF (sign flag) -- a special flag that tells you when a result becomes 0
        => flag is flipped when a result hits zero or goes negative
        => this is part of CPU's HW optimization
        => `i-- > 0` uses 1 assembly instruction & 1 register
        ```asm
        DEC RCX      ; Decrement the loop counter in register RCX
        JG  loop_top ; Jump back to top if the result was Greater than zero
        ```
- avoid int underflow
    - size_t is unsigned & can never be -ve, so if u try to write a standard backward loop, u might accidentally trigger an infinite loop due to int underflow
    what about reaching 0th index?
    - value of i is checked first
    - decrement happens
    - then new decremented value of i is used in the body
    * so DONT use pre-increment(`--i`) if not the decrement happens before the check & index 0 is never reached!

### inserting & erasing

```cpp
	vector<int> v;
v.push_back(2);          // [2]
v.push_back(3);          // [2, 3]
v.push_back(7);          // [2, 3, 7]
v.push_back(5);          // [2, 3, 7, 5]
v[1] = 4;                // sets element at index 1 to 4 -> [2, 4, 7, 5]
v.erase(v.begin() + 1);  // removes element at index 1 -> [2, 7, 5]
// this remove method is O(n); to be avoided
v.push_back(8);        // [2, 7, 5, 8]
v.erase(v.end() - 1);  // [2, 7, 5]
// here, we remove the element from the end of the list; this is O(1).
v.push_back(4);                     // [2, 7, 5, 4]
v.push_back(4);                     // [2, 7, 5, 4, 4]
v.push_back(9);                     // [2, 7, 5, 4, 4, 9]
cout << v[2];                       // 5
v.erase(v.begin(), v.begin() + 3); // [4 ,4 9]
// this erases 1st 3 elements, O(n) time
```

## strings

refer to [chapter_5 of LearnCpp](../LearnCpp/chapter_5/chapter_5.md)

- read strings from `std::cin`
    - know `getline()` & `cin`
- know how to sort, concatenate, loop through string's characters
- get ith character
- get substrings using `string::substr`

## pairs & tuples

### pairs

pairs - store 2 elements of different types

- pair<type1, type2> p;
- creating a pair:
    - older: make_pair(a,b)
    - cpp11 & above: {a, b}
- pair values
    - pair.first
    - pair.second

### tuples

tuples - hold more than 2 values of different types

tuple<type1, type2, ... typeN> t;
make_tuple(a,b, ...)
get<i>(t) - returns the ith element of the tuple t, can be used to change the element of a tuple; REQUIRES `const i`

```cpp
tuple<int, int, int> t{3, 4, 5};
int i = 1;
cout << get<i>(t) << endl;  // not allowed! (i need to be const)
```

```cpp
// changing values 
```

## MEM allocation

- biggest concern when using arrays is the MEM limit: USACO limit is 256MB
- total bytes = 256 * 10^6 bytes
    - divide by ints (4 bytes) = 64 * 10^6
    - divide by long long (8 bytes) = 16 * 10^6
- note that `program overhead` due to recursion will reduce available MEM